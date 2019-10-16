#!/usr/bin/env python3
"""Infoset ORM classes.

Manages connection pooling among other things.

"""

# Main python libraries
import sys
import os
import getpass
from pwd import getpwnam
import copy
from collections import defaultdict

# PIP3 imports
try:
    import yaml
    from sqlalchemy import create_engine
    import pymysql
except ImportError:
    import pip
    _PACKAGES = ['PyYAML', 'sqlalchemy', 'pymysql']
    for _PACKAGE in _PACKAGES:
        pip.main(['install', '--user', _PACKAGE])
    print(
        'New Python packages installed. Please run this script again to '
        'complete the Infoset-NG installation.')
    # Must exit abnormally as the script didn't complete
    sys.exit(2)

# Try to create a working PYTHONPATH
_MAINT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_ROOT_DIRECTORY = os.path.abspath(
    os.path.join(_MAINT_DIRECTORY, os.pardir))
if _ROOT_DIRECTORY.endswith('/infoset-ng') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'Infoset-NG is not installed in a "infoset-ng/" directory. '
        'Please fix.')
    sys.exit(2)

# Infoset libraries
from infoset.utils import log
from infoset.utils import configuration
from infoset.utils import general
from maintenance import shared


class _ConfigCreate(object):
    """Class to test setup."""

    def __init__(self, daemon_username):
        """Function for intializing the class.

        Args:
            daemon_username: Username to run scripts as

        Returns:
            None

        """
        # Initialize key variables
        valid_directories = []
        config = ("""\
main:
    log_directory:
    log_level: debug
    ingest_cache_directory:
    ingest_pool_size: 20
    listen_address: 0.0.0.0
    bind_port: 6000
    interval: 300
    memcached_hostname: localhost
    memcached_port: 11211
    sqlalchemy_pool_size: 10
    sqlalchemy_max_overflow: 10
    db_hostname: localhost
    db_username: infoset_ng
    db_password:
    db_name: infoset_ng
    username: {}
""").format(daemon_username)

        self.config_dict = yaml.safe_load(config)
        directory_dict = defaultdict(lambda: defaultdict(dict))

        # Read yaml files from configuration directory
        self.directories = general.config_directories()

        # Check each directory in sequence
        for config_directory in self.directories:
            # Check if config_directory exists
            if os.path.isdir(config_directory) is False:
                continue

            # Cycle through list of files in directory
            for filename in os.listdir(config_directory):
                # Examine all the '.yaml' files in directory
                if filename.endswith('.yaml'):
                    # YAML files found
                    valid_directories.append(config_directory)

        if bool(valid_directories) is True:
            directory_dict = general.read_yaml_files(
                valid_directories, die=False)

        # Populate config_dict with any values found in directory_dict
        # Only if the directory has valid files in it.
        if bool(directory_dict) is True:
            for _main, data_dict in directory_dict.items():
                if _main != 'main':
                    log_message = (
                        'Invalid files found in configuration directory')
                    log.log2die_safe(1033, log_message)

                for key, value in data_dict.items():
                    if value is not None:
                        self.config_dict[_main][key] = value

    def validate(self):
        """Validate all pre-requisites are OK.

        Args:
            None

        Returns:
            None

        """
        # Verify db credentials
        self._db_credentials()

        # Attempt to connect to the MySQL database
        self._db_connectivity()

    def write(self):
        """Write the config to file.

        Args:
            None


        Returns:
            None
        """
        # Initialize key variables
        directory = self.directories[0]

        # Update configuration file if required
        for next_directory in self.directories:
            # Delete all YAML files in the configuration directory
            general.delete_yaml_files(next_directory)

        # Write config back to directory
        filepath = ('%s/config.yaml') % (directory)
        with open(filepath, 'w') as outfile:
            yaml.dump(self.config_dict, outfile, default_flow_style=False)

            # Write status Update
            shared.print_ok('Created configuration file {}.'.format(filepath))

    def _db_credentials(self):
        """Validate database credentials.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        missing = False
        parameters = [
            'db_hostname', 'db_password', 'db_username', 'db_password']

        # Give warning message if no parameters found
        for parameter in parameters:
            if bool(self.config_dict['main'][parameter]) is False:
                missing = True
        if missing is True:
            print('\nMISSING - Database parameters need to be updated.')

        # Prompt for any missing database parameters
        for parameter in sorted(parameters):
            if bool(self.config_dict['main'][parameter]) is False:
                if parameter != 'db_password':
                    self.config_dict['main'][parameter] = input(
                        'Input database {}: '.format(parameter[3:]))
                else:
                    self.config_dict['main'][parameter] = getpass.getpass(
                        'Input database password: ')

        # Print a space
        if missing is True:
            print('')

    def _db_connectivity(self):
        """Validate we can connect to the database.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = False
        db_hostname = self.config_dict['main']['db_hostname']
        db_password = self.config_dict['main']['db_password']
        db_username = self.config_dict['main']['db_username']
        db_name = self.config_dict['main']['db_name']

        # Do test
        try:
            # Open database connection. Prepare cursor
            database = pymysql.connect(
                host=db_hostname,
                user=db_username,
                passwd=db_password,
                db=db_name)
            cursor = database.cursor()

            # Do a basic check
            cursor.execute('SELECT VERSION()')
            results = cursor.fetchone()

            # Check result
            valid = bool(results)

            # disconnect from server
            database.close()

        except Exception as _:
            valid = False

        except:
            valid = False

        # Process validity
        if valid is True:
            log_message = 'Database connectivity successfully verified.'
            shared.print_ok(log_message)
        else:
            log_message = (
                'Cannot connect to the database. Verify your credentials. '
                'Database Hostname: "{}", Database Username: "{}", '
                'Database Name: "{}", Database Password: "******"'
                ''.format(db_hostname, db_username, db_name))
            log.log2die_safe(1067, log_message)


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

        # Print status
        shared.print_ok(
            'Configuration setup complete.')

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


class _PythonSetupPackages(object):
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
            log.log2die_safe(1135, log_message)

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
        shared.print_ok(
            'Installing required pip3 packages from requirements.txt file.')
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

        # Status message
        shared.print_ok(
            'pip3 packages installation complete.')


def run():
    """Setup infoset-ng.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    username = getpass.getuser()

    # Prevent running as sudo user
    if 'SUDO_UID' in os.environ:
        log_message = (
            'Cannot run setup using "sudo". Run as a regular user to '
            'install in this directory or as user "root".')
        log.log2die_safe(1032, log_message)

    # If running as the root user, then the infoset user needs to exist
    if username == 'root':
        try:
            daemon_username = input(
                'Please enter the username under which '
                'infoset-ng will run: ')

            # Get GID and UID for user
            _ = getpwnam(daemon_username).pw_gid
        except:
            log_message = (
                'User {} not found. Please try again.'
                ''.format(daemon_username))
            log.log2die_safe(1105, log_message)
    else:
        daemon_username = username

    # Create a configuration only if unittests are not being run
    if 'INFOSET_CONFIGDIR' not in os.environ:
        config = _ConfigCreate(daemon_username)
        config.validate()
        config.write()

    # Determine whether version of python is valid
    _PythonSetupPackages().run()

    # Update configuration if required
    _ConfigSetup().run()

    ###########################################################################
    # Create database with newly created configuration
    # The database libraries cannot be imported if there
    # isn't a valid configuration
    ###########################################################################
    executable = 'python3 {}/{}'.format(_MAINT_DIRECTORY, 'database.py')
    returncode = os.system(executable)
    if bool(returncode) is True:
        sys.exit(2)


if __name__ == '__main__':
    # Run setup
    run()
