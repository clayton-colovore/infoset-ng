#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import sys
import os
import getpass
from pwd import getpwnam
import grp
import copy
import re

# PIP3 imports
try:
    import yaml
    from sqlalchemy import create_engine
except ImportError:
    import pip
    packages = ['yaml', 'sqlalchemy']
    for package in packages:
        pip.main(['install', '--user', package])
    import yaml
    from sqlalchemy import create_engine

# Try to create a working PYTHONPATH
_lib_directory = os.path.dirname(os.path.realpath(__file__))
_infoset_directory = os.path.abspath(os.path.join(_lib_directory, os.pardir))
_root_directory = os.path.abspath(os.path.join(_infoset_directory, os.pardir))
if _root_directory.endswith('/infoset-ng') is True:
    sys.path.append(_root_directory)
else:
    print(
        'Infoset-NG is not installed in a "infoset-ng/" directory. '
        'Please fix.')
    sys.exit(2)

# Infoset libraries
try:
    from infoset.utils import log
except:
    print(
        'You need to set your PYTHONPATH to include the '
        'infoset-ng root directory')
    sys.exit(2)
from infoset.utils import configuration
from infoset.utils import general
from infoset.db.db_orm import BASE, Agent, Department, Device, Billcode
from infoset.db.db_orm import Configuration, DeviceAgent, Datapoint, AgentName
from infoset.db import URL
from infoset.db import db_configuration
from infoset.db import db_billcode
from infoset.db import db_department
from infoset.db import db_device
from infoset.db import db_agent
from infoset.db import db_agentname
from infoset.db import db_deviceagent
from infoset.db import db_datapoint
from infoset.db import db


class _DatabaseSetup(object):
    """Class to setup database."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.reserved = '_SYSTEM_RESERVED_'
        self.config = configuration.Config()

    def _insert_datapoint(self):
        """Insert first datapoint in the database.

        Args:
            None

        Returns:
            None

        """
        # Insert
        if db_datapoint.idx_datapoint_exists(1) is False:
            record = Datapoint(
                id_datapoint=general.encode(self.reserved),
                agent_label=general.encode(self.reserved),
                agent_source=general.encode(self.reserved)
            )
            database = db.Database()
            database.add(record, 1047)

    def _insert_department(self):
        """Insert first department in the database.

        Args:
            None

        Returns:
            None

        """
        # Insert
        if db_department.idx_department_exists(1) is False:
            record = Department(
                code=general.encode(self.reserved),
                name=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1102)

    def _insert_billcode(self):
        """Insert first billcode in the database.

        Args:
            None

        Returns:
            None

        """
        # Insert
        if db_billcode.idx_billcode_exists(1) is False:
            record = Billcode(
                code=general.encode(self.reserved),
                name=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1104)

    def _insert_agent_device(self):
        """Insert first agent and device in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        idx_agentname = 1
        idx_agent = 1
        idx_device = 1

        # Add agent name
        if db_agentname.idx_agentname_exists(idx_agentname) is False:
            # Generate a name add a record in the database
            record = AgentName(
                name=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1019)

        # Add agent
        if db_agent.idx_agent_exists(idx_agent) is False:
            # Generate an Agent ID and add a record in the database
            record = Agent(id_agent=general.encode(self.reserved))
            database = db.Database()
            database.add(record, 1109)

        # Add device
        if db_device.idx_device_exists(idx_device) is False:
            record = Device(
                description=general.encode(self.reserved),
                devicename=general.encode(self.reserved)
            )
            database = db.Database()
            database.add(record, 1106)

        # Add to Agent / Device table
        if db_deviceagent.device_agent_exists(idx_device, idx_agent) is False:
            record = DeviceAgent(idx_device=idx_device, idx_agent=idx_agent)
            database = db.Database()
            database.add(record, 1107)

    def _insert_config(self):
        """Insert first config in the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        key_values = [('version', '0.0.0.0')]

        # Cycle through all the key value pairs
        for item in key_values:
            key = item[0]
            value = item[1]

            # Check if value exists and insert if not
            if db_configuration.config_key_exists(key) is False:
                record = Configuration(
                    config_key=general.encode(key),
                    config_value=general.encode(value))
                database = db.Database()
                database.add(record, 1108)

    def run(self):
        """Setup database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        use_mysql = True
        pool_size = 25
        max_overflow = 25
        config = self.config

        # Create DB connection pool
        if use_mysql is True:
            # Add MySQL to the pool
            engine = create_engine(
                URL, echo=True,
                encoding='utf8',
                max_overflow=max_overflow,
                pool_size=pool_size, pool_recycle=3600)

            # Try to create the database
            print_ok('Attempting to create database tables')
            try:
                sql_string = (
                    'ALTER DATABASE %s CHARACTER SET utf8mb4 '
                    'COLLATE utf8mb4_general_ci') % (config.db_name())
                engine.execute(sql_string)
            except:
                log_message = (
                    'Cannot connect to database %s. '
                    'Verify database server is started. '
                    'Verify database is created. '
                    'Verify that the configured database authentication '
                    'is correct.') % (config.db_name())
                log.log2die(1036, log_message)

            # Apply schemas
            print_ok('Applying Schemas.')
            BASE.metadata.create_all(engine)

            # Insert database entries
            self._insert_agent_device()
            self._insert_billcode()
            self._insert_department()
            self._insert_datapoint()
            self._insert_config()


class _ConfigSetup(object):
    """Class to setup configuration.

    NOTE! We cannot use the configuration.Config class here. The aim
    of this class is to read in the configuration found in etc/ or
    $INFOSET_CONFIGDIR and set any missing values to values that are
    known to work in most cases.

    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Read configuration into dictionary
        self.directories = general.config_directories()
        self.config = general.read_yaml_files(self.directories)

    def run(self):
        """Update the configuration with good defaults.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        updated_list = []
        config = copy.deepcopy(self.config)
        directory = self.directories[0]

        # Update log_directory and ingest_cache_directory
        if isinstance(config, dict) is True:
            if 'main' in config:
                # Setup the log_directory to a known good default
                (updated, config) = self._create_directory_entries(
                    'log_directory', config)
                updated_list.append(updated)

                # Setup the ingest_cache_directory to a known good default
                (updated, config) = self._create_directory_entries(
                    'ingest_cache_directory', config)
                updated_list.append(updated)

            else:
                valid = False
        else:
            valid = False

        # Gracefully exit if things are not OK
        if valid is False:
            log_message = (
                'Configuration files found in {} is invalid'
                ''.format(self.directories))
            log.log2die_safe(1101, log_message)

        # Update configuration file if required
        if len(updated_list) == updated_list.count(True):
            for next_directory in self.directories:
                # Delete all YAML files in the directory
                general.delete_yaml_files(next_directory)

            # Write config back to directory
            filepath = ('%s/config.yaml') % (directory)
            with open(filepath, 'w') as outfile:
                yaml.dump(config, outfile, default_flow_style=False)

    def _create_directory_entries(self, key, config):
        """Update the configuration with good defaults for directories.

        Args:
            key: Configuration key related to a directory.
            config: Configuration dictionary

        Returns:
            updated: True if we have to update a value

        """
        # Initialize key variables
        updated = False
        dir_dict = {
            'log_directory': 'log',
            'ingest_cache_directory': 'cache',
        }
        directory = general.root_directory()

        # Setup the key value to a known good default
        if key in config['main']:
            # Verify whether key value is empty
            if config['main'][key] is not None:
                # Create
                if os.path.isdir(config['main'][key]) is False:
                    config['main'][key] = ('%s/%s') % (
                        directory, dir_dict[key])
                    updated = True
            else:
                config['main'][key] = ('%s/%s') % (directory, dir_dict[key])
                updated = True
        else:
            config['main'][key] = ('%s/%s') % (directory, dir_dict[key])
            updated = True

        # Return
        return (updated, config)


class _PythonSetup(object):
    """Class to setup Python."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        self.username = getpass.getuser()
        valid = True
        major = 3
        minor = 5
        major_installed = sys.version_info[0]
        minor_installed = sys.version_info[1]

        # Exit if python version is too low
        if major_installed < major:
            valid = False
        elif major_installed == major and minor_installed < minor:
            valid = False
        if valid is False:
            log_message = (
                'Required python version must be >= {}.{}. '
                'Python version {}.{} installed'
                ''.format(major, minor, major_installed, minor_installed))
            log.log2die_safe(1018, log_message)

    def run(self):
        """Setup Python.

        Args:
            None

        Returns:
            None

        """
        # Run
        self._install_pip3_packages()

    def _install_pip3_packages(self):
        """Install PIP3 packages.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = self.username

        # Don't attempt to install packages if running in the Travis CI
        # environment
        if 'TRAVIS' in os.environ and 'CI' in os.environ:
            return

        # Determine whether PIP3 exists
        print_ok('Installing required pip3 packages')
        pip3 = general.search_file('pip3')
        if pip3 is None:
            log_message = ('Cannot find python "pip3". Please install.')
            log.log2die_safe(1052, log_message)

        # Install required PIP packages
        requirements_file = (
            '%s/requirements.txt') % (general.root_directory())

        if username == 'root':
            script_name = (
                'pip3 install --upgrade --requirement %s'
                '') % (requirements_file)
        else:
            script_name = (
                'pip3 install --user --upgrade --requirement %s'
                '') % (requirements_file)
        general.run_script(script_name)


class _DaemonSetup(object):
    """Class to setup infoset-ng daemon."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = getpass.getuser()
        self.root_directory = general.root_directory()
        self.infoset_user_exists = True
        self.infoset_user = None
        self.running_as_root = False

        # If running as the root user, then the infoset user needs to exist
        if username == 'root':
            self.running_as_root = True
            try:
                self.infoset_user = input(
                    'Please enter the username under which '
                    'infoset-ng will run: ')

                # Get GID and UID for user
                self.gid = getpwnam(self.infoset_user).pw_gid
                self.uid = getpwnam(self.infoset_user).pw_uid
            except KeyError:
                self.infoset_user_exists = False
            return

        # Die if user doesn't exist
        if self.infoset_user_exists is False:
            log_message = (
                'User {} not found. Please try again.'
                ''.format(self.infoset_user))
            log.log2die_safe(1049, log_message)

    def run(self):
        """Setup daemon scripts and file permissions.

        Args:
            None

        Returns:
            None

        """
        # Return if not running script as root user
        if self.running_as_root is False:
            return

        # Return if user prompted doesn't exist
        if self.infoset_user_exists is False:
            return

        # Set file permissions
        self._file_permissions()

        # Setup systemd
        self._systemd()

    def _file_permissions(self):
        """Set file permissions.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        infoset_user = self.infoset_user
        root_directory = self.root_directory

        # Prompt to change ownership of root_directory
        groupname = grp.getgrgid(self.gid).gr_name
        response = input(
            'Change ownership of {} directory to user:{} group:{} (y,N) ?: '
            ''.format(root_directory, infoset_user, groupname))

        # Abort if necessary
        if response.lower() != 'y':
            log_message = ('Aborting as per user request.')
            log.log2die_safe(1050, log_message)

        # Change ownership of files under root_directory
        for parent_directory, directories, files in os.walk(root_directory):
            for directory in directories:
                os.chown(os.path.join(
                    parent_directory, directory), self.uid, self.gid)
            for next_file in files:
                os.chown(os.path.join(
                    parent_directory, next_file), self.uid, self.gid)

        # Change ownership of root_directory
        os.chown(root_directory, self.uid, self.gid)

    def _systemd(self):
        """Setup systemd configuration.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        username = self.infoset_user
        groupname = grp.getgrgid(self.gid).gr_name
        system_directory = '/etc/systemd/system'
        system_command = '/bin/systemctl daemon-reload'

        # Copy system files to systemd directory and activate
        service_ingester = (
            '{}/examples/linux/systemd/infoset-ng-ingester.service'
            ''.format(self.root_directory))
        service_api = (
            '{}/examples/linux/systemd/infoset-ng-api.service'
            ''.format(self.root_directory))

        # Read in file
        # 1) Convert home directory to that of user
        # 2) Convert username in file
        # 3) Convert group in file
        filenames = [service_ingester, service_api]
        for filename in filenames:
            # Read next file
            with open(filename, 'r') as f_handle:
                contents = f_handle.read()

            # Substitute home directory
            contents = re.sub(
                r'/home/infoset-ng',
                self.root_directory,
                contents)

            # Substitute username
            contents = re.sub(
                'User=infoset-ng',
                'User={}'.format(username),
                contents)

            # Substitute group
            contents = re.sub(
                'Group=infoset-ng',
                'Group={}'.format(groupname),
                contents)

            # Write contents
            filepath = (
                '{}/{}'.format(system_directory, os.path.basename(filename)))
            if os.path.isdir(system_directory):
                with open(filepath, 'w') as f_handle:
                    f_handle.write(contents)

        # Make systemd recognize new files
        if os.path.isdir(system_directory):
            general.run_script(system_command)


def print_ok(message):
    """Install python module using pip3.

    Args:
        module: module to install

    Returns:
        None

    """
    # Print message
    print('OK - {}'.format(message))


def run():
    """Setup infoset-ng.

    Args:
        None

    Returns:
        None

    """
    # Prevent running as sudo user
    if 'SUDO_UID' in os.environ:
        MESSAGE = (
            'Cannot run setup using "sudo". Run as a regular user to '
            'install in this directory or as user "root".')
        log.log2die_safe(1078, MESSAGE)

    # Initialize key variables
    username = getpass.getuser()

    # Determine whether version of python is valid
    _PythonSetup().run()

    # Do specific setups for root user
    _DaemonSetup().run()

    # Update configuration if required
    _ConfigSetup().run()

    # Run server setup
    _DatabaseSetup().run()

    # Give suggestions as to what to do
    if username == 'root':
        suggestions = """\

You can start infoset-ng daemons with these commands:

    # systemctl start infoset-ng-api.service
    # systemctl start infoset-ng-ingester.service

You can enable infoset-ng daemons to start on system boot with these commands:

    # systemctl enable infoset-ng-api.service
    # systemctl enable infoset-ng-ingester.service

"""
        print(suggestions)

    # All done
    print_ok('Installation successful.')


if __name__ == '__main__':
    # Run setup
    run()
