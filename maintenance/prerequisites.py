#!/usr/bin/env python3
"""infoset  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys
import getpass
import os
from collections import defaultdict
from pwd import getpwnam


# PIP3 libraries
###############################################################################
# YAML needs to be installed for the general library to be used
###############################################################################
try:
    import yaml
    from sqlalchemy import create_engine
except ImportError:
    import pip
    _username = getpass.getuser()
    _PACKAGES = ['PyYAML', 'sqlalchemy', 'setuptools']
    for _PACKAGE in _PACKAGES:
        # Install package globally if user 'root'
        if _username == 'root':
            pip.main(['install', _PACKAGE])
        else:
            pip.main(['install', '--user', _PACKAGE])
    print(
        'New Python packages installed. Please run this script again to '
        'complete the Infoset-NG installation.')
    sys.exit(0)

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

# Do infoset-ng imports
from infoset.utils import log
from infoset.utils import general
from maintenance import misc


def run():
    """Do the installation.

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
            'Cannot run installation using "sudo". Run as a regular user to '
            'install in this directory or as user "root".')
        log.log2die_safe(1029, log_message)

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
            log.log2die_safe(1022, log_message)
    else:
        daemon_username = username

    # Do precheck
    precheck = _PreCheck()
    precheck.validate()

    # Create a configuration
    config = _Config(daemon_username)
    config.validate()
    config.write()


class _Config(object):
    """Class to test setup."""

    def __init__(self, username):
        """Function for intializing the class.

        Args:
            username: Username to run scripts as

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
""").format(username)

        self.config_dict = yaml.load(config)
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
        for _main, data_dict in directory_dict.items():
            if _main != 'main':
                log_message = (
                    'Invalid files found in configuration directory')
                log.log2die_safe(1033, log_message)

            for key, value in data_dict.items():
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
            misc.print_ok('Created configuration file {}.'.format(filepath))

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
        # Do key imports
        import pymysql

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
            misc.print_ok(log_message)
        else:
            log_message = (
                'Cannot connect to the database. Verify your credentials. '
                'Database Hostname: "{}", Database Username: "{}", '
                'Database Name: "{}", Database Password: "******"'
                ''.format(db_hostname, db_username, db_name))
            log.log2die_safe(1067, log_message)


class _PreCheck(object):
    """Class to test setup."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """

    def validate(self):
        """Validate all pre-requisites are OK.

        Args:
            None

        Returns:
            None

        """
        # Test systemd exists
        self._systemd()

        # Test Python version
        self._python()

        # Test Python pip version
        self._pip()

        # Test MySQL version
        self._mysql()

        # Test MySQL version
        self._memcached()

    def _systemd(self):
        """Determine if systemd is installed.

        Args:
            None

        Returns:
            None

        """
        # install pip3 modules
        username = getpass.getuser()
        system_directory = '/etc/systemd/system'
        if username == 'root':
            if os.path.isdir(system_directory) is False:
                log_message = (
                    'The systemd package isn\'t installed on this system.')
                log.log2die_safe(1048, log_message)
            else:
                log_message = ('systemd installed')
                misc.print_ok(log_message)        

    def _pip(self):
        """Determine pip3 version.

        Args:
            None

        Returns:
            None

        """
        # install pip3 modules
        modules = ['setuptools']
        for module in modules:
            _pip3_install(module)

    def _python(self):
        """Determine Python version.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        major = 3
        minor = 5
        major_installed = sys.version_info[0]
        minor_installed = sys.version_info[1]

        # Determine whether python version is too low
        if major_installed < major:
            valid = False
        elif major_installed == major and minor_installed < minor:
            valid = False

        # Process validity
        if valid is False:
            log_message = (
                'Required python version must be >= {}.{}. '
                'Python version {}.{} installed'
                ''.format(major, minor, major_installed, minor_installed))
            log.log2die_safe(1095, log_message)
        else:
            log_message = (
                'Python version {}.{}.'
                ''.format(major_installed, minor_installed))
            misc.print_ok(log_message)

    def _memcached(self):
        """Determine pip3 version.

        Args:
            None

        Returns:
            None

        """
        # Find pip3 executable
        cli_string = 'which memcached'
        response = general.run_script(cli_string)

        # Not OK if not found
        if bool(response['returncode']) is True:
            log_message = (
                'memcached is not installed. infoset-ng runs best with it.')
            log.log2see_safe(1076, log_message)
        else:
            log_message = 'memcached executable found.'
            misc.print_ok(log_message)

            # Check whether the server is running
            cli_string = 'ps aux | grep /usr/bin/memcached | grep -v grep'
            ps_response = bool(os.popen(cli_string).read())

            # Not OK if not fount
            if ps_response is False:
                log_message = (
                    'memcached is not running. infoset-ng runs best with it.')
                log.log2see_safe(1077, log_message)
            else:
                log_message = 'memcached is running.'
                misc.print_ok(log_message)

    def _mysql(self):
        """Determine MySQL version.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        valid = True
        versions = {
            'maria': {'major': 10, 'minor': 0},
            'mysql': {'major': 5, 'minor': 7}
        }

        # Get response from mysql command
        cli_string = '/usr/bin/mysql --version'
        response = general.run_script(cli_string)

        # Not OK if not fount
        if bool(response['returncode']) is True:
            valid = False
            log_message = ('MySQL / MariaDB not installed.')
            log.log2die_safe(1096, log_message)

        else:
            # Determine major and minor versions of software
            version_string = response['stdout'].split()[4]
            version_list = version_string.split('.')
            major_installed = int(version_list[0])
            minor_installed = int(version_list[1])

            # We are running MariaDB
            if 'maria' in version_string.lower():
                major = versions['maria']['major']
                minor = versions['maria']['minor']

                # Exit if  version is too low
                if major_installed < major:
                    valid = False
                elif major_installed == major and minor_installed < minor:
                    valid = False
                else:
                    valid = True

                if valid is False:
                    log_message = (
                        'MariaDB version needs to be >= than {}.{}.'
                        ''.format(major, minor))
                    log.log2die_safe(1097, log_message)
                else:
                    log_message = (
                        'MariaDB version {}.{}.'
                        ''.format(major_installed, minor_installed))
                    misc.print_ok(log_message)

            # We are running MySQL
            else:
                major = versions['mysql']['major']
                minor = versions['mysql']['minor']

                # Exit if  version is too low
                if major_installed < major:
                    valid = False
                elif major_installed == major and minor_installed < minor:
                    valid = False
                else:
                    valid = True

                if valid is False:
                    log_message = (
                        'MySQL version needs to be >= than {}.{}.'
                        ''.format(major, minor))
                    log.log2die_safe(1098, log_message)
                else:
                    log_message = (
                        'MySQL version {}.{}.'
                        ''.format(major_installed, minor_installed))
                    misc.print_ok(log_message)

        # Check whether the server is running
        cli_string = 'ps aux | grep /usr/sbin/mysqld | grep -v grep'
        response = bool(os.popen(cli_string).read())

        # Not OK if not fount
        if response is False:
            log_message = ('MySQL / MariaDB is not running.')
            log.log2die_safe(1099, log_message)
        else:
            log_message = 'MySQL / MariaDB is running.'
            misc.print_ok(log_message)


def _pip3_install(module):
    """Install python module using pip3.

    Args:
        module: module to install

    Returns:
        None

    """
    # Find pip3 executable
    cli_string = 'which pip3'
    response = general.run_script(cli_string, die=False)

    # Not OK if not fount
    if bool(response['returncode']) is True:
        log_message = ('python pip3 not installed.')
        log.log2die_safe(1041, log_message)
    else:
        log_message = 'Python pip3 executable found.'
        misc.print_ok(log_message)

    # Determine version of pip3
    cli_string = 'pip3 --version'
    _response = os.popen(cli_string).read()
    version = _response.split()[1]

    # Attempt to install module
    if version < '9.0.0':
        cli_string = 'pip3 list | grep {}'.format(module)
    else:
        cli_string = 'pip3 list --format columns | grep {}'.format(module)
    __response = bool(os.popen(cli_string).read())

    if __response is False:
        # YAML is not installed try to install it
        cli_string = 'pip3 install --user {}'.format(module)
        response_install = general.run_script(cli_string, die=False)

        # Fail if module cannot be installed
        if bool(response_install['returncode']) is True:
            log_message = ('python pip3 cannot install "{}".'.format(module))
            log.log2die_safe(1100, log_message)
        else:
            log_message = (
                'Python module "{}" is installed.'.format(module))
            misc.print_ok(log_message)
    else:
        log_message = 'Python module "{}" is installed.'.format(module)
        misc.print_ok(log_message)


if __name__ == '__main__':
    # Run main
    run()
