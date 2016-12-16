#!/usr/bin/env python3
"""Classes and functions to insert cache file data into the database."""

# Standard libraries
import os
import time
import shutil
from collections import defaultdict
from multiprocessing import Pool
import re

# PIP libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.db import db
from infoset.db.db_orm import Data, Datapoint, Agent, Device, DeviceAgent
from infoset.db import db_agent as agent
from infoset.db import db_device as ddevice
from infoset.db import db_deviceagent as hagent
from infoset.utils import configuration
from infoset.utils import general
from infoset.utils import log
from infoset.cache import drain
from infoset.utils import daemon


class _ProcessAgentCache(object):
    """Processes cache files from a single agent.

    The ingester daemon periodically runs methods in this class.

    Methodology:

    1)  JSON data from each successive cache file is converted to a series
        of dicts using the Drain class in infoset.cache.drain

    2)  Data from invalid files are discarded and moved to a failure
        directory for future analysis.

    3)  The timestamp of the ingester's PID file is updated with each valid
        file found.

        The ingester normally updates the PID file periodically while it
        waits for new data. It is automatically restarted if there is no
        PID file activity as it is assumed the ingester is hung.

        The ingester therefore needs to continue updating its PID file while
        it is processing data to reduce this risk.

    4)  Newly discovered agents, devices and datapoints are added to
        the database. The AgentDevice table is also updated to track the
        devices each agent is tracking.

    5)  The actual datapoint values are added to the database.

    6)  Database table rows are updated with the timestamp of this most
        recent update.

    """

    def __init__(self, config, metadata, ingester_agent_name):
        """Initialize the class.

        args:
            config: Config object
            metadata: Metadata
            ingester_agent_name: Ingester's agent name

        """
        self.config = config
        self.metadata = metadata
        self.ingester_agent_name = ingester_agent_name

    def process(self):
        """Update the database using threads."""
        # Initialize key variables
        do_update = False
        success = None
        ingests = []
        agent_data = {
            'devicename': None,
            'id_agent': None,
            'sources': [],
            'timeseries': [],
            'timefixed': []
        }

        # Get the directory to which failed files will be moved
        failure_directory = self.config.ingest_failures_directory()

        # Initialize other values
        max_timestamp = 0

        # Get start time for activity
        start_ts = time.time()

        # Process file for each timestamp, starting from the oldes file
        for data_dict in self.metadata:
            # Initialize key variables
            timestamp = data_dict['timestamp']
            filepath = data_dict['filepath']

            # Read in data
            ingest = drain.Drain(filepath)

            # Make sure file is OK
            # Move it to a directory for further analysis
            # by administrators
            if ingest.valid() is False:
                log_message = (
                    'Cache ingest file %s is invalid. Moving.'
                    '') % (filepath)
                log.log2warning(1054, log_message)
                shutil.copy(filepath, failure_directory)
                os.remove(filepath)
                continue

            # Append data
            agent_data['timeseries'].extend(ingest.timeseries())
            agent_data['timefixed'].extend(ingest.timefixed())
            agent_data['sources'].extend(ingest.sources())

            # Append ingest object to a list for later processing
            ingests.append(ingest)

            # Get the max timestamp
            max_timestamp = max(timestamp, max_timestamp)

            # Update information that doesn't change
            if do_update is False:
                agent_data['devicename'] = ingest.devicename()
                agent_data['id_agent'] = ingest.id_agent()
                agent_data['agent_name'] = ingest.agent()

                # Get the PID file for the agent
                pid_file = daemon.pid_file(self.ingester_agent_name)

            # Update the PID file for the agent to ensure agentd.py
            # doesn't kill the ingest while processing a long stream
            # of files. If we are running this using __main__ = process()
            # then the pid file wouldn't have been created, hence the logic.
            if os.path.isfile(pid_file) is True:
                daemon.update_pid(self.ingester_agent_name)

            # Update update flag
            do_update = True

        # Process the rest
        if do_update is True:
            # Update remaining agent data
            agent_data['max_timestamp'] = max_timestamp

            # Add datapoints to the database
            db_prepare = _PrepareDatabase(agent_data)
            db_prepare.add_datapoints()

            # Get the latest datapoints
            datapoints = db_prepare.get_datapoints()

            # Get the assigned index values for the device and agent
            idx_device = db_prepare.idx_device()
            idx_agent = db_prepare.idx_agent()

            # Update database with data
            db_update = _UpdateDB(agent_data, datapoints)
            success = db_update.update()

            # Update database table timestamps
            update_timestamps = _UpdateLastTimestamp(
                idx_device, idx_agent, max_timestamp)
            update_timestamps.agent()
            update_timestamps.deviceagent()
            update_timestamps.datapoint()

            # Purge source files. Only done after complete
            # success of database updates. If not we could lose data in the
            # event of an ingester crash. Ingester would re-read the files
            # and process the non-duplicates, while deleting the duplicates.
            for ingest in ingests:
                ingest.purge()

            # Log duration of activity
            duration = time.time() - start_ts
            if success is True:
                log_message = (
                    'Agent %s was processed from %s cache files in %s '
                    'seconds (%s seconds/file, %s seconds/datapoint)'
                    '') % (
                        agent_data['id_agent'],
                        len(ingests),
                        round(duration, 4),
                        round(duration / len(ingests), 4),
                        round(duration / len(datapoints), 6))
                log.log2info(1007, log_message)
            else:
                log_message = (
                    'Failed to process all cache files for agent %s. '
                    'Investigate.') % (
                        agent_data['id_agent'])
                log.log2info(1008, log_message)


class _PrepareDatabase(object):
    """Prepare database for insertion of new datapoint values.

    Newly discovered agents, devices and datapoints are added to
    the database.

    The AgentDevice table is also updated to track the devices
    each agent is tracking.

    """

    def __init__(self, agent_data):
        """Instantiate the class.

        Args:
            agent_data: Agent data from successive Drains

        Returns:
            None

        """
        # Initialize key variables
        self.agent_data = agent_data

        # Update Agent, Device and DeviceAgent database tables if
        # Device and agent are not already there
        self._idx_agent = self.idx_agent()
        self._idx_device = self.idx_device()

    def idx_agent(self):
        """Insert new agent into database if necessary.

        Args:
            None

        Returns:
            idx_agent: IDX value of agent from database

        """
        # Initialize key variables
        agent_name = self.agent_data['agent_name']
        id_agent = self.agent_data['id_agent']

        # Get information on agent from database
        data = agent.GetIDAgent(id_agent)

        # Return if agent already exists in the table
        if data.exists() is True:
            idx_agent = data.idx_agent()
            return idx_agent

        # Add record to the database
        record = Agent(
            id_agent=general.encode(id_agent),
            name=general.encode(agent_name))
        database = db.Database()
        database.add(record, 1081)

        # Get idx_agent value from database
        data = agent.GetIDAgent(id_agent)
        idx_agent = data.idx_agent()
        return idx_agent

    def idx_device(self):
        """Insert new device into database if necessary.

        Args:
            None

        Returns:
            idx_device: Index value for device record

        """
        # Initialize key variables
        devicename = self.agent_data['devicename']

        # Get information on agent from database
        device = ddevice.GetDevice(devicename)

        # Determine index value for device
        if device.exists() is True:
            idx_device = device.idx_device()
        else:
            # Add record to the database
            record = Device(devicename=general.encode(devicename))
            database = db.Database()
            database.add(record, 1080)

            # Get idx of newly added device
            device_info = ddevice.GetDevice(devicename)
            idx_device = device_info.idx_device()

        # Update DeviceAgent table
        idx_agent = self._idx_agent
        if hagent.device_agent_exists(idx_device, idx_agent) is False:
            # Add to DeviceAgent table
            record = DeviceAgent(idx_device=idx_device, idx_agent=idx_agent)
            database = db.Database()
            database.add(record, 1038)

        # Return
        return idx_device

    def add_datapoints(self):
        """Add new datapoints to the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        new_datapoint_ids = []

        # Add newly found datapoints to database if agent is enabled
        agent_object = agent.GetIDXAgent(self._idx_agent)
        if agent_object.enabled() is True:
            # Create map of DIDs to database row index values
            dp_metadata = self.get_datapoints()

            # Update datapoint metadata if not there
            # Use a dictionary query versus individual database calls
            # which was slow.
            for source in self.agent_data['sources']:
                id_datapoint = source['id_datapoint']
                if id_datapoint not in dp_metadata:
                    # This is a protection against the scenario where
                    # the very first contact from an agent is a result
                    # of a stream of data postings of cached data.
                    # The datapoints are not originally in the database
                    # and so there is the risk of duplicate insertions
                    if id_datapoint not in new_datapoint_ids:
                        self._add_datapoint(source)

                        # Note the datapoint that was added
                        new_datapoint_ids.append(id_datapoint)

    def get_datapoints(self):
        """Create dict of enabled datapoints and their corresponding indices.

        Args:
            None

        Returns:
            data: Dict keyed by datapoint ID,
                with a tuple as its value (idx, idx_agent)
                idx: Datapoint index
                idx_agent: Agent index
                last_timestamp: The last time the timestamp was updated

        """
        # Initialize key variables
        idx_agent = self._idx_agent
        data = {}

        # Update database
        database = db.Database()
        session = database.session()
        result = session.query(
            Datapoint.id_datapoint, Datapoint.idx_datapoint,
            Datapoint.idx_agent, Datapoint.last_timestamp).filter(
                and_(Datapoint.enabled == 1,
                     Datapoint.idx_agent == idx_agent))

        # Massage data
        for instance in result:
            id_datapoint = instance.id_datapoint.decode('utf-8')
            idx_datapoint = instance.idx_datapoint
            idx_agent = instance.idx_agent
            last_timestamp = instance.last_timestamp
            data[id_datapoint] = {
                'idx_datapoint': idx_datapoint,
                'idx_agent': idx_agent,
                'last_timestamp': last_timestamp
            }

        # Return the session to the database pool after processing
        database.close()

        # Return
        return data

    def _add_datapoint(self, source):
        """Insert new datapoint into database.

        Args:
            source: Dict of datapoint source information
                {'id_agent': id_agent,
                 'id_datapoint': id_datapoint,
                 'agent_label': agent_label,
                 'agent_source': source,
                 'description': description,
                 'base_type': base_type}

                id_agent: Agent Identifier
                id_datapoint: Datapoint ID
                label: Datapoint label created by agent
                source: Source of the data (subsystem being tracked)
                description: Description provided by agent config file
                base_type = SNMP base type (Counter32, Counter64, Gauge etc.)

        Returns:
            None

        """
        # Initialize key variables
        idx_agent = self._idx_agent
        idx_device = self._idx_device
        id_datapoint = source['id_datapoint']
        agent_label = source['agent_label']
        agent_source = source['agent_source']
        base_type = source['base_type']

        # Insert record
        record = Datapoint(
            id_datapoint=general.encode(id_datapoint),
            idx_agent=idx_agent,
            idx_device=idx_device,
            agent_label=general.encode(agent_label),
            agent_source=general.encode(agent_source),
            base_type=base_type)
        database = db.Database()
        database.add(record, 1082)


class _UpdateDB(object):
    """Update database with agent data.

    The actual datapoint values are added to the database.

    """

    def __init__(self, agent_data, datapoints):
        """Instantiate the class.

        Args:
            agent_data: Agent data obtained from Drain object
            datapoints: Dict of datapoint data

        Returns:
            None

        """
        self.agent_data = agent_data
        self.datapoints = datapoints

    def update(self):
        """Update the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        success = True
        outcomes = []

        # Update timeseries data
        outcomes.append(self._update_timeseries())

        # Update timefixed data
        outcomes.append(self._update_timefixed())

        # Determine success
        if False in outcomes:
            success = False

        # Return
        return success

    def _update_timeseries(self):
        """Insert data into the database "iset_data" table.

        Args:
            mapping: Map of DIDs to database row index values

        Returns:
            success: True if successful

        """
        # Initialize key variables
        success = False
        data = self.agent_data['timeseries']
        datapoints = self.datapoints
        data_list = []
        timestamp_tracker = {}

        # Update data
        for item in data:
            # Process datapoint values
            id_datapoint = item['id_datapoint']
            value = item['value']
            timestamp = item['timestamp']

            # Get data on datapoints
            idx_datapoint = datapoints[id_datapoint]['idx_datapoint']
            last_timestamp = datapoints[id_datapoint]['last_timestamp']

            # Only update with data collected after
            # the most recent DID update. Don't do anything more
            if timestamp > last_timestamp:
                data_list.append(
                    Data(
                        idx_datapoint=idx_datapoint,
                        value=value,
                        timestamp=timestamp
                    )
                )

                # Update DID's last updated timestamp
                if idx_datapoint in timestamp_tracker:
                    timestamp_tracker[idx_datapoint] = max(
                        timestamp, timestamp_tracker[idx_datapoint])
                else:
                    timestamp_tracker[idx_datapoint] = timestamp

        # Update if there is data
        if bool(data_list) is True:
            # Do performance data update
            database = db.Database()
            success = database.add_all(data_list, 1056, die=False)
            success = True

        # Return
        return success

    def _update_timefixed(self):
        """Update timefixed data into the database "iset_datapoint" table.

        Args:
            mapping: Map of DIDs to database row index values

        Returns:
            success: True if successful

        """
        # Initialize key variables
        success = True
        data = self.agent_data['timefixed']
        datapoints = self.datapoints
        data_list = []
        timestamp_tracker = {}

        # Update data
        for item in data:
            # Process datapoint values
            id_datapoint = item['id_datapoint']
            value = item['value']
            timestamp = item['timestamp']

            # Get data on datapoints
            idx_datapoint = datapoints[id_datapoint]['idx_datapoint']
            last_timestamp = datapoints[id_datapoint]['last_timestamp']

            # Only update with data collected after
            # the most recent update. Don't do anything more
            if timestamp > last_timestamp:
                data_list.append(
                    (idx_datapoint, value)
                )

                # Update DID's last updated timestamp
                if idx_datapoint in timestamp_tracker:
                    timestamp_tracker[idx_datapoint] = max(
                        timestamp, timestamp_tracker[idx_datapoint])
                else:
                    timestamp_tracker[idx_datapoint] = timestamp

        # Update if there is data
        if bool(data_list) is True:
            # Create a database session
            # NOTE: We only do a single commit on the session.
            # This is much faster (20x based on testing) than
            # instantiating the database, updating records, and committing
            # after every iteration of the "for loop"
            database = db.Database()
            session = database.session()

            # Update timefixed data
            for item in data_list:
                (idx_datapoint, value) = item
                data_dict = {'timefixed_value': general.encode(value)}
                session.query(Datapoint).filter(
                    Datapoint.idx_datapoint == idx_datapoint).update(
                        data_dict)

            # Commit data
            database.commit(session, 1037)

            # Return
            return success


class _UpdateLastTimestamp(object):
    """Update the last_timestamp values for updated tables.

    1)  DeviceAgent
    2)  Agent
    3)  Device

    """

    def __init__(self, idx_device, idx_agent, last_timestamp):
        """Instantiate the class.

        Args:
            idx_device: Index of device in database
            idx_agent: Index of agent in database
            last_timestamp: Timestamp to be used in updating the tables

        Returns:
            None

        """
        # Initialize key variables
        self.idx_device = idx_device
        self.idx_agent = idx_agent
        self.last_timestamp = last_timestamp

    def deviceagent(self):
        """Update the deviceagent last_timestamp value.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        idx_agent = self.idx_agent
        idx_device = self.idx_device
        last_timestamp = self.last_timestamp

        # Update database
        database = db.Database()
        session = database.session()
        record = session.query(DeviceAgent).filter(
            and_(
                DeviceAgent.idx_device == idx_device,
                DeviceAgent.idx_agent == idx_agent)).one()
        record.last_timestamp = last_timestamp
        database.commit(session, 1124)

    def agent(self):
        """Update the database timestamp for the agent.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        idx_agent = self.idx_agent
        last_timestamp = self.last_timestamp

        # Update the database
        database = db.Database()
        session = database.session()
        record = session.query(
            Agent).filter(Agent.idx_agent == idx_agent).one()
        record.last_timestamp = last_timestamp
        database.commit(session, 1055)

    def datapoint(self):
        """Update the database timestamp for the datapoint.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        idx_agent = self.idx_agent
        idx_device = self.idx_device
        last_timestamp = self.last_timestamp
        data_dict = {'last_timestamp': last_timestamp}

        # Access the database
        database = db.Database()
        session = database.session()

        # Update
        session.query(Datapoint).filter(
            and_(Datapoint.idx_device == idx_device,
                 Datapoint.idx_agent == idx_agent,
                 Datapoint.enabled == 1)).update(data_dict)
        database.commit(session, 1057)


def validate_cache_files():
    """Create metadata for cache files with valid names.

    Args:
        None

    Returns:
        id_agent_metadata: Dict keyed by
            devicehash: A hash of the devicename
            id_agent: The agent's ID

            The contents of each key pair is a list of dicts with these keys
                timestamp: Timestamp of the data received
                filepath: The path to the file to be read

    """
    # Initialize key variables
    id_agent_metadata = defaultdict(lambda: defaultdict(dict))

    # Configuration setup
    config = configuration.Config()
    cache_dir = config.ingest_cache_directory()

    # Filenames must start with a numeric timestamp and #
    # end with a hex string. This will be tested later
    regex = re.compile(r'^\d+_[0-9a-f]+_[0-9a-f]+.json')

    # Add files in cache directory to list
    all_filenames = [filename for filename in os.listdir(
        cache_dir) if os.path.isfile(
            os.path.join(cache_dir, filename))]

    ######################################################################
    # Create threads
    ######################################################################

    # Process only valid agent filenames
    for filename in all_filenames:
        # Add valid data to lists
        if bool(regex.match(filename)) is True:
            # Create a complete filepath
            filepath = os.path.join(cache_dir, filename)

            # Only read files that are 15 seconds or older
            # to prevent corruption caused by reading a file that could be
            # updating simultaneously
            if time.time() - os.path.getmtime(filepath) < 15:
                continue

            # Create a dict of Identifiers, timestamps and filepaths
            (name, _) = filename.split('.')
            (tstamp, id_agent, devicehash) = name.split('_')
            timestamp = int(tstamp)

            # Create data dictionary
            data_dict = {
                'timestamp': timestamp,
                'filepath': filepath
            }

            # Keep track of devices and the Identifiers that track them
            # Create a list of timestamp, device filepath
            # tuples for each id_agent
            if bool(id_agent_metadata[devicehash][id_agent]) is True:
                id_agent_metadata[
                    devicehash][id_agent].append(data_dict)
            else:
                id_agent_metadata[
                    devicehash][id_agent] = [data_dict]

    # Return
    return id_agent_metadata


def _wrapper_process(argument_list):
    """Wrapper function to unpack arguments before calling the real function.

    Args:
        argument_list: A list of tuples of arguments to be provided to
            lib_process_devices.process_device

    Returns:
        Nothing

    """
    return _process(*argument_list)


def _process(config, metadata, ingester_agent_name):
    """Process metadata.

    Args:
        config: Config object
        metadata: metadata
        ingester_agent_name: Ingester's agent name

    Returns:
        Nothing

    """
    # Start processing
    data = _ProcessAgentCache(config, metadata, ingester_agent_name)
    data.process()


def process(ingester_agent_name):
    """Process cache data by adding it to the database using subprocesses.

    Args:
        ingester_agent_name: Ingester agent name

    Returns:
        None

    """
    # Initialize key variables
    argument_list = []
    id_agent_metadata = defaultdict(lambda: defaultdict(dict))

    # Configuration setup
    config = configuration.Config()
    configured_pool_size = config.ingest_pool_size()

    # Make sure we have database connectivity
    if db.connectivity() is False:
        log_message = (
            'No connectivity to database. Check if running. '
            'Check database authentication parameters.'
            '')
        log.log2warning(1053, log_message)
        return

    # Get meta data on files
    id_agent_metadata = validate_cache_files()

    # Spawn processes only if we have files to process
    if bool(id_agent_metadata.keys()) is True:
        # Process lock file
        lockfile = daemon.lock_file(ingester_agent_name)
        if os.path.exists(lockfile) is True:
            # Return if lock file is present
            log_message = (
                'Ingest lock file %s exists. Multiple ingest daemons running '
                'or lots of cache files to ingest. Ingester may have died '
                'catastrophically in the past, in which case the lockfile '
                'should be deleted. Exiting ingest process. '
                'Will try again later.'
                '') % (lockfile)
            log.log2warning(1069, log_message)
            return
        else:
            # Create lockfile
            open(lockfile, 'a').close()

        # Read each cache file
        for devicehash in id_agent_metadata.keys():
            for id_agent in id_agent_metadata[devicehash].keys():
                # Create a list of arguments to process
                argument_list.append(
                    (config,
                     id_agent_metadata[devicehash][id_agent],
                     ingester_agent_name)
                )

        # Create a pool of sub process resources
        pool_size = int(min(configured_pool_size, len(id_agent_metadata)))
        with Pool(processes=pool_size) as pool:

            # Create sub processes from the pool
            pool.map(_wrapper_process, argument_list)

        # Wait for all the processes to end
        # pool.join()

        # Return if lock file is present
        if os.path.exists(lockfile) is True:
            os.remove(lockfile)

if __name__ == "__main__":
    process('ingestd')
