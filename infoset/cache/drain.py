#!/usr/bin/env python3

"""Demonstration Script that extracts agent data from cache directory files.

This could be a modified to be a daemon

"""

# Standard libraries
import os
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.utils import general
from infoset.cache import validate


class Drain(object):
    """Infoset class that ingests agent data.

    Args:
        None

    Returns:
        None

    Methods:
        __init__:
        populate:
        post:
    """

    def __init__(self, filename):
        """Method initializing the class.

        Args:
            filename: Cache filename

        Returns:
            None

        """
        # Initialize key variables
        self.filename = filename
        self._information = defaultdict(lambda: defaultdict(dict))
        self._sources = []
        self.validated = False
        self.agent_meta = {}
        data_types = ['timeseries', 'timefixed']

        # Ingest data
        validator = validate.ValidateCache(filename)
        information = validator.getinfo()

        # Log if data is bad
        if information is False:
            log_message = (
                'Cache ingest file %s is invalid.') % (filename)
            log.log2warning(1051, log_message)
            return
        else:
            self.validated = True

        # Process validated data
        if self.validated is True:
            # Get main keys
            self.agent_meta = _main_keys(information)
            timestamp = self.agent_meta['timestamp']
            id_agent = self.agent_meta['id_agent']

            # Process timeseries data
            for data_type in data_types:
                # Skip if data type isn't in the data
                if data_type not in information:
                    continue

                # Process the data type
                for agent_label, label_dict in sorted(
                        information[data_type].items()):
                    # Get universal parameters for label_dict
                    base_type = _base_type(label_dict['base_type'])
                    description = label_dict['description']

                    # Create a key in the data based on the base_type
                    if base_type not in self._information[data_type]:
                        self._information[data_type][base_type] = []

                    # Process the data associated with the agent_label
                    for datapoint in label_dict['data']:
                        # Create a unique, unchangeable id_datapoint for data
                        index = datapoint[0]
                        value = datapoint[1]
                        source = datapoint[2]
                        id_datapoint = _id_datapoint(
                            id_agent, agent_label, index,
                            self.agent_meta['agent'],
                            self.agent_meta['devicename'])

                        # Convert values to float if this is
                        # data that could be charted
                        if base_type != 0:
                            value = float(value)

                        # Update the data
                        self._information[data_type][base_type].append(
                            {'id_agent': id_agent,
                             'id_datapoint': id_datapoint,
                             'value': value,
                             'timestamp': timestamp}
                        )

                        # Update sources after fixing encoding
                        self._sources.append(
                            {'id_agent': id_agent,
                             'id_datapoint': id_datapoint,
                             'agent_label': agent_label,
                             'agent_source': source,
                             'description': description,
                             'base_type': base_type}
                        )

    def valid(self):
        """Determine whether data is valid.

        Args:
            None

        Returns:
            isvalid: Valid if true

        """
        # Initialize key variables
        isvalid = self.validated

        # Return
        return isvalid

    def id_agent(self):
        """Return id_agent.

        Args:
            None

        Returns:
            data: Agent Identifier

        """
        # Initialize key variables
        data = self.agent_meta['id_agent']

        # Return
        return data

    def timestamp(self):
        """Return timestamp.

        Args:
            None

        Returns:
            data: Agent timestamp

        """
        # Initialize key variables
        data = int(self.agent_meta['timestamp'])

        # Return
        return data

    def agent(self):
        """Return agent.

        Args:
            None

        Returns:
            data: Agent agent_name

        """
        # Initialize key variables
        data = self.agent_meta['agent']

        # Return
        return data

    def devicename(self):
        """Return devicename.

        Args:
            None

        Returns:
            data: Agent devicename

        """
        # Initialize key variables
        data = self.agent_meta['devicename']

        # Return
        return data

    def counter32(self):
        """Return counter32 timeseries data from file.

        Args:
            None

        Returns:
            data: List of tuples (id_agent, id_datapoint, value, timestamp)
                id_agent = Identifier of device providing data
                id_datapoint = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        data = []

        # Get data
        if 'timeseries' in self._information:
            if 32 in self._information['timeseries']:
                data = self._information['timeseries'][32]

        # Return
        return data

    def counter64(self):
        """Return counter64 timeseries data from file.

        Args:
            None

        Returns:
            data: List of tuples (id_agent, id_datapoint, value, timestamp)
                id_agent = Identifier of device providing data
                id_datapoint = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        data = []

        # Get data
        if 'timeseries' in self._information:
            if 64 in self._information['timeseries']:
                data = self._information['timeseries'][64]

        # Return
        return data

    def floating(self):
        """Return floating timeseries data from file.

        Args:
            None

        Returns:
            data: List of tuples (id_agent, id_datapoint, value, timestamp)
                id_agent = Identifier of device providing data
                id_datapoint = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        data = []

        # Get data
        if 'timeseries' in self._information:
            if 1 in self._information['timeseries']:
                data = self._information['timeseries'][1]

        # Return
        return data

    def timeseries(self):
        """Return all timeseries data from file.

        Args:
            None

        Returns:
            data: List of tuples (id_agent, id_datapoint, value, timestamp)
                id_agent = Identifier of device providing data
                id_datapoint = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        data = []

        # Initialize key variables
        data.extend(self.floating())
        data.extend(self.counter32())
        data.extend(self.counter64())

        # Return
        return data

    def timefixed(self):
        """Return other non-timeseries data from file.

        Args:
            None

        Returns:
            data: List of tuples (id_agent, id_datapoint, value, timestamp)
                id_agent = Identifier of device providing data
                id_datapoint = Datapoint ID
                value = Value of datapoint
                timestamp = Timestamp when data was collected by the agent

        """
        # Initialize key variables
        data = []

        # Return (Ignore whether floating or counter)
        if 'timefixed' in self._information:
            for _, value in self._information['timefixed'].items():
                data.extend(value)
        return data

    def sources(self):
        """Return sources data from file.

        Args:
            None

        Returns:
            data: List of tuples (id_agent, id_datapoint,
                    label, source, description)
                id_agent = Identifier of device providing data
                id_datapoint = Datapoint ID
                label = Label that the agent gave the category of datapoint
                source = Subsystem that provided the data in the datapoint
                description = Description of the label
                base_type = SNMP base type code (Counter32, Gauge etc.)

        """
        # Initialize key variables
        data = self._sources

        # Return
        return data

    def purge(self):
        """Purge cache file that was read.

        Args:
            None

        Returns:
            success: "True" if successful

        """
        # Initialize key variables
        success = True

        try:
            os.remove(self.filename)
        except:
            success = False

        # Report success
        if success is True:
            log_message = (
                'Ingest cache file %s deleted') % (self.filename)
            log.log2debug(1046, log_message)
        else:
            log_message = (
                'Failed to delete ingest cache file %s') % (self.filename)
            log.log2debug(1087, log_message)

        # Return
        return success


def _id_datapoint(id_agent, label, index, agent_name, devicename):
    """Create a unique DID from ingested data.

    Args:
        id_agent: Identifier of device that created the cache data file
        label: Label of the data
        index: Index of the data
        agent_name: Name of agent
        devicename: Devicename

    Returns:
        id_datapoint: Datapoint ID

    """
    # Initialize key variables
    prehash = ('%s%s%s%s%s') % (id_agent, label, index, agent_name, devicename)
    result = general.hashstring(prehash)
    id_datapoint = result

    # Return
    return id_datapoint


def _main_keys(information):
    """Properly format the keys of information received from the validator.

    Args:
        information: Dict of data received from validator

    Returns:
        agent_meta: Dict of data with properly formatted main keys.

    """
    # Initialize key variables
    agent_meta = {}
    agent_meta_keys = [
        'timestamp', 'id_agent', 'agent', 'devicename']

    # Get universal parameters from file. Convert to unicode
    for key in agent_meta_keys:
        if key == 'timestamp':
            agent_meta[key] = int(information[key])
        else:
            agent_meta[key] = information[key]

    # Return
    return agent_meta


def _base_type(data):
    """Create a base_type integer value from the string sent by agents.

    Args:
        data: base_type value as string

    Returns:
        base_type: Base type value as integer

    """
    # Initialize key variables
    if bool(data) is False:
        value = 'NULL'
    else:
        value = data

    # Assign base type code
    if value == 1:
        base_type = 1
    elif value == 32:
        base_type = 32
    elif value == 64:
        base_type = 64
    else:
        base_type = 0

    # Return
    return base_type
