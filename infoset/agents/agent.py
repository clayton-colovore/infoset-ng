#!/usr/bin/env python3
"""infoset Agent class.

Description:

    This script:
        1) Processes a variety of information from agents
        2) Posts the data using HTTP to a server listed
           in the configuration file

"""
# Standard libraries
import os
import textwrap
import tempfile
import sys
import time
import argparse
from collections import defaultdict
from copy import deepcopy
import json
import multiprocessing

# pip3 libraries
import requests
from gunicorn.app.base import BaseApplication
from gunicorn.six import iteritems

# infoset libraries
from infoset.utils import log
from infoset.utils import general
from infoset.utils import daemon
from infoset.utils import configuration
from infoset.utils.daemon import Daemon
from infoset.api import API


class Agent(object):
    """Agent class for daemons."""

    def __init__(self, parent, child=None):
        """Method initializing the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon

        Returns:
            None

        """
        # Initialize key variables (Parent)
        self.parent = parent
        self.pidfile_parent = daemon.pid_file(parent)
        self.lockfile_parent = daemon.lock_file(parent)

        # Initialize key variables (Child)
        if bool(child) is None:
            self.pidfile_child = None
        else:
            self.pidfile_child = daemon.pid_file(child)

    def name(self):
        """Return agent name.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self.parent
        return value

    def query(self):
        """Placeholder method."""
        # Do nothing
        pass


class AgentAPI(Agent):
    """infoset-ng API agent that serves web pages.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        populate:
        post:
    """

    def __init__(self, parent, child):
        """Method initializing the class.

        Args:
            parent: Name of parent daemon
            child: Name of child daemon

        Returns:
            None

        """
        # Initialize key variables
        Agent.__init__(self, parent, child)
        self.config = configuration.Config()

    def query(self):
        """Query all remote devices for data.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        config = self.config

        # Check for lock and pid files
        if os.path.exists(self.lockfile_parent) is True:
            log_message = (
                'Lock file %s exists. Multiple API daemons running '
                'API may have died '
                'catastrophically in the past, in which case the lockfile '
                'should be deleted. '
                '') % (self.lockfile_parent)
            log.log2see(1083, log_message)

        if os.path.exists(self.pidfile_parent) is True:
            log_message = (
                'PID file: %s already exists. Daemon already running? '
                'If not, it may have died catastrophically in the past '
                'in which case you should use --stop --force to fix.'
                '') % (self.pidfile_parent)
            log.log2see(1084, log_message)

        ######################################################################
        #
        # Assign options in format that the Gunicorn WSGI will accept
        #
        # NOTE! to get a full set of valid options pprint(self.cfg.settings)
        # in the instantiation of StandaloneApplication. The option names
        # do not exactly match the CLI options found at
        # http://docs.gunicorn.org/en/stable/settings.html
        #
        ######################################################################
        options = {
            'bind': '%s:%s' % (config.listen_address(), config.bind_port()),
            'accesslog': config.web_log_file(),
            'errorlog': config.web_log_file(),
            'capture_output': True,
            'pidfile': self.pidfile_child,
            'loglevel': config.log_level(),
            'workers': _number_of_workers(),
        }

        # Log so that user running the script from the CLI knows that something
        # is happening
        log_message = (
            'Infoset API running on %s:%s and logging to file %s.'
            '') % (
                config.listen_address(),
                config.bind_port(),
                config.web_log_file())
        log.log2info(1022, log_message)

        # Run
        StandaloneApplication(API, options).run()


class AgentReferenceSample(object):
    """Infoset reference agent class for posting data.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        populate:
        post:
    """

    def __init__(self, config, devicename):
        """Method initializing the class.

        Args:
            config: ConfigAgent configuration object
            agent_name: Name of agent
            devicename: Devicename that the agent applies to

        Returns:
            None

        """
        # Initialize key variables
        self.data = defaultdict(lambda: defaultdict(dict))
        agent_name = config.agent_name()
        id_agent = get_id_agent(config)

        # Add timestamp
        self.data['timestamp'] = general.normalized_timestamp()
        self.data['id_agent'] = id_agent
        self.data['agent'] = agent_name
        self.data['devicename'] = devicename

        # Construct URL for server
        if config.api_server_https() is True:
            prefix = 'https://'
        else:
            prefix = 'http://'
        self.url = (
            '%s%s:%s/%s/receive/%s') % (
                prefix, config.api_server_name(),
                config.api_server_port(), config.api_server_uri(), id_agent)

        # Create the cache directory
        self.cache_dir = config.agent_cache_directory()
        if os.path.exists(self.cache_dir) is False:
            os.mkdir(self.cache_dir)

    def name(self):
        """Return the name of the agent.

        Args:
            None

        Returns:
            value: Name of agent

        """
        # Return
        value = self.data['agent']
        return value

    def populate(self, data_in):
        """Populate data for agent to eventually send to server.

        Args:
            data_in: dict of datapoint values from agent
            timeseries: TimeSeries data if True

        Returns:
            None

        """
        # Initialize data
        data = deepcopy(data_in)

        # Validate base_type
        if len(data) != 1 or isinstance(data, defaultdict) is False:
            log_message = ('Agent data "%s" is invalid') % (data)
            log.log2die(1025, log_message)

        ######################################################################
        # Get a description to use for label value. You could do a lookup in
        # a table based on the spoken language of the environment based on the
        # label and assign the translated result to data[label]['description']
        ######################################################################
        for label in data.keys():
            data[label]['description'] = label
            break

        # Add data to appropriate self.data key
        if data[label]['base_type'] is not None:
            self.data['timeseries'].update(data)
        else:
            self.data['timefixed'].update(data)

    def populate_single(self, label, value, base_type=None, source=None):
        """Populate a single value in the agent.

        Args:
            label: Agent label for data
            value: Value of data
            source: Source of the data
            base_type: Base type of data

        Returns:
            None

        """
        # Initialize key variables
        data = defaultdict(lambda: defaultdict(dict))
        data[label]['base_type'] = base_type
        data[label]['data'] = [[0, value, source]]

        # Update
        self.populate(data)

    def populate_named_tuple(self, named_tuple, prefix='', base_type=1):
        """Post system data to the central server.

        Args:
            named_tuple: Named tuple with data values
            prefix: Prefix to append to data keys when populating the agent
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Get data
        system_dict = named_tuple._asdict()
        for label, value in system_dict.items():
            # Convert the dict to two dimensional dict keyed by [label][source]
            # for use by self.populate_dict
            new_label = ('%s_%s') % (prefix, label)

            # Initialize data
            data = defaultdict(lambda: defaultdict(dict))

            # Add data
            data[new_label]['data'] = [[0, value, None]]
            data[new_label]['base_type'] = base_type

            # Update
            self.populate(data)

    def populate_dict(self, data_in, prefix='', base_type=1):
        """Populate agent with data that's a dict keyed by [label][source].

        Args:
            data_in: Dict of data to post "X[label][source] = value"
            prefix: Prefix to append to data keys when populating the agent
            base_type: SNMP style base_type (integer, counter32, etc.)

        Returns:
            None

        """
        # Initialize data
        data_input = deepcopy(data_in)

        # Iterate over labels
        for label in data_input.keys():
            # Initialize tuple list to use by agent.populate
            value_sources = []
            new_label = ('%s_%s') % (prefix, label)

            # Initialize data
            data = defaultdict(lambda: defaultdict(dict))
            data[new_label]['base_type'] = base_type

            # Append to tuple list
            # (Sorting is important to keep consistent ordering)
            for source, value in sorted(data_input[label].items()):
                value_sources.append(
                    [source, value, source]
                )
            data[new_label]['data'] = value_sources

            # Update
            self.populate(data)

    def polled_data(self):
        """Return that that should be posted.

        Args:
            None

        Returns:
            None

        """
        # Return
        return self.data

    def post(self, save=True, data=None):
        """Post data to central server.

        Args:
            save: When True, save data to cache directory if postinf fails
            data: Data to post. If None, then uses self.data

        Returns:
            success: "True: if successful

        """
        # Initialize key variables
        success = False
        response = False
        timestamp = self.data['timestamp']
        id_agent = self.data['id_agent']

        # Create data to post
        if data is None:
            data = self.data

        # Post data save to cache if this fails
        try:
            result = requests.post(self.url, json=data)
            response = True
        except:
            if save is True:
                # Create a unique very long filename to reduce risk of
                devicehash = general.hashstring(self.data['devicename'], sha=1)
                filename = ('%s/%s_%s_%s.json') % (
                    self.cache_dir, timestamp, id_agent, devicehash)

                # Save data
                with open(filename, 'w') as f_handle:
                    json.dump(data, f_handle)

        # Define success
        if response is True:
            if result.status_code == 200:
                success = True

        # Log message
        if success is True:
            log_message = (
                'Agent "%s" successfully contacted server %s'
                '') % (self.name(), self.url)
            log.log2info(1027, log_message)
        else:
            log_message = (
                'Agent "%s" failed to contact server %s'
                '') % (self.name(), self.url)
            log.log2warning(1028, log_message)

        # Return
        return success

    def purge(self):
        """Purge data from cache by posting to central server.

        Args:
            None

        Returns:
            success: "True: if successful

        """
        # Initialize key variables
        id_agent = self.data['id_agent']

        # Add files in cache directory to list
        filenames = [filename for filename in os.listdir(
            self.cache_dir) if os.path.isfile(
                os.path.join(self.cache_dir, filename))]

        # Read cache file
        for filename in filenames:
            # Only post files for our own UID value
            if id_agent not in filename:
                continue

            # Get the full filepath for the cache file and post
            filepath = os.path.join(self.cache_dir, filename)
            with open(filepath, 'r') as f_handle:
                try:
                    data = json.load(f_handle)
                except:
                    # Log removal
                    log_message = (
                        'Error reading previously cached agent data file %s '
                        'for agent %s. May be corrupted.'
                        '') % (filepath, self.name())
                    log.log2die(1064, log_message)

            # Post file
            success = self.post(save=False, data=data)

            # Delete file if successful
            if success is True:
                os.remove(filepath)

                # Log removal
                log_message = (
                    'Purging cache file %s after successfully '
                    'contacting server %s'
                    '') % (filepath, self.url)
                log.log2info(1029, log_message)


def get_id_agent(config):
    """SAMPLE - Create a permanent UID for the agent.

    Args:
        config: ConfigAgent configuration object

    Returns:
        id_agent: UID for agent

    """
    # Initialize key variables
    agent_name = config.agent_name()
    prefix = ('_INFOSET_TEST_%s') % (agent_name)

    #########################################################################
    #########################################################################
    # You would need to find a way to create a permanent filename for
    # the id_agent based on the agent_name
    #########################################################################
    #########################################################################
    temp = tempfile.NamedTemporaryFile(delete=False, prefix=prefix)
    filename = temp.name

    # Read environment file with UID if it exists
    if os.path.isfile(filename):
        with open(filename) as f_handle:
            id_agent = f_handle.readline()
    else:
        # Create a UID and save
        id_agent = generate_id_agent()
        with open(filename, 'w+') as env:
            env.write(str(id_agent))

    # Return
    return id_agent


def generate_id_agent():
    """SAMPLE - Generate an id_agent.

    Args:
        None

    Returns:
        id_agent: the UID

    """
    #########################################################################
    #########################################################################
    # NOTE: In production you'd need to generate the id_agent value from
    # a random string
    #########################################################################
    #########################################################################
    id_agent = general.hashstring('_INFOSET_TEST_')

    # Return
    return id_agent


class AgentDaemon(Daemon):
    """Class that manages polling.

    Args:
        None

    Returns:
        None

    """

    def __init__(self, poller):
        """Method initializing the class.

        Args:
            poller: PollingAgent object

        Returns:
            None

        """
        # Instantiate poller
        self.poller = poller

        # Get PID filename
        agent_name = self.poller.name()
        pidfile = daemon.pid_file(agent_name)
        lockfile = daemon.lock_file(agent_name)

        # Call up the base daemon
        Daemon.__init__(self, pidfile, lockfile=lockfile)

    def run(self):
        """Start polling.

        Args:
            None

        Returns:
            None

        """
        # Start polling. (Poller decides frequency)
        while True:
            self.poller.query()


class AgentCLI(object):
    """Class that manages the agent CLI.

    Args:
        None

    Returns:
        None

    """

    def __init__(self):
        """Method initializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.parser = None

    def process(self, additional_help=None):
        """Return all the CLI options.

        Args:
            None

        Returns:
            args: Namespace() containing all of our CLI arguments as objects
                - filename: Path to the configuration file

        """
        # Header for the help menu of the application
        parser = argparse.ArgumentParser(
            description=additional_help,
            formatter_class=argparse.RawTextHelpFormatter)

        # CLI argument for starting
        parser.add_argument(
            '--start',
            required=False,
            default=False,
            action='store_true',
            help='Start the agent daemon.'
        )

        # CLI argument for stopping
        parser.add_argument(
            '--stop',
            required=False,
            default=False,
            action='store_true',
            help='Stop the agent daemon.'
        )

        # CLI argument for getting the status of the daemon
        parser.add_argument(
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Get daemon daemon status.'
        )

        # CLI argument for restarting
        parser.add_argument(
            '--restart',
            required=False,
            default=False,
            action='store_true',
            help='Restart the agent daemon.'
        )

        # CLI argument for stopping
        parser.add_argument(
            '--force',
            required=False,
            default=False,
            action='store_true',
            help=textwrap.fill(
                'Stops or restarts the agent daemon ungracefully when '
                'used with --stop or --restart.', width=80)
        )

        # Get the parser value
        self.parser = parser

    def control(self, poller):
        """Start the infoset agent.

        Args:
            poller: PollingAgent object

        Returns:
            None

        """
        # Get the CLI arguments
        self.process()
        parser = self.parser
        args = parser.parse_args()

        # Run daemon
        service = AgentDaemon(poller)
        if args.start is True:
            service.start()
        elif args.stop is True:
            if args.force is True:
                service.force()
            else:
                service.stop()
        elif args.restart is True:
            if args.force is True:
                service.force()
                service.start()
            else:
                service.restart()
        elif args.status is True:
            service.status()
        else:
            parser.print_help()
            sys.exit(2)


class StandaloneApplication(BaseApplication):
    """Class to integrate the Gunicorn WSGI with the Infoset Flask application.

    Modified from: http://docs.gunicorn.org/en/latest/custom.html

    """

    def __init__(self, app, options=None):
        """Method initializing the class.

        args:
            app: Flask application object of type Flask(__name__)
            options: Gunicorn CLI options

        """
        # Initialize key variables
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        """Load the configuration."""
        # Initialize key variables
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])

        # Assign configuration parameters
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        """Run the Flask application throught the Gunicorn WSGI."""
        return self.application


def _number_of_workers():
    """Get the number of CPU cores on this server."""
    return (multiprocessing.cpu_count() * 2) + 1


def agent_sleep(agent_name, seconds=300):
    """Make agent sleep for a specified time, while updating PID every 300s.

    Args:
        agent_name: Name of agent
        seconds: number of seconds to sleep

    Returns:
        id_agent: identifier for agent

    """
    # Initialize key variables
    interval = 300
    remaining = seconds

    # Start processing
    while True:
        # Update the PID file timestamp (important)
        daemon.update_pid(agent_name)

        # Sleep for at least "interval" number of seconds
        if remaining < interval:
            time.sleep(remaining)
            break
        else:
            time.sleep(interval)

        # Decrement remaining time
        remaining = remaining - interval
