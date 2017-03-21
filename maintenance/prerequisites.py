#!/usr/bin/env python3
"""infoset  classes.

Manages the verification of required packages.

"""

# Main python libraries
import sys
import getpass
import os


# PIP3 libraries
###############################################################################
# Install all prerequisite packages for infoset-ng to be successfully installed
###############################################################################
try:
    import yaml
    import pymysql
    from sqlalchemy import create_engine
except ImportError:
    import pip
    _username = getpass.getuser()
    _PACKAGES = ['PyYAML', 'sqlalchemy', 'setuptools', 'pymysql']
    for _PACKAGE in _PACKAGES:
        # Install package globally if user 'root'
        if _username == 'root':
            pip.main(['install', _PACKAGE])
        else:
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
    # Prevent running as sudo user
    if 'SUDO_UID' in os.environ:
        log_message = (
            'Cannot run installation using "sudo". Run as a regular user to '
            'install in this directory or as user "root".')
        log.log2die_safe(1029, log_message)

    # Do precheck
    precheck = _PreCheck()
    precheck.validate()


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

        # Create a blank configuration
        self._blank_configuration()

    def _blank_configuration(self):
        """Determine if systemd is installed.

        Args:
            None

        Returns:
            None

        """
        # Verify
        found = False
        root_directory = general.root_directory()
        config_directory = '{}/etc'.format(root_directory)

        # Do nothing if running Travis CI
        if 'INFOSET_CONFIGDIR' in os.environ:
            return

        # Find yaml files in config_directory
        filenames = [
            filename for filename in os.listdir(
                config_directory) if os.path.isfile(
                    os.path.join(config_directory, filename))]
        for filename in filenames:
            if filename.lower().endswith('.yaml'):
                log_message = ('Configuration file found')
                misc.print_ok(log_message)
                found = True
                break

        # Create a blank config if none are found
        if found is False:
            config_yaml = ("""\
main:
    log_directory:
    log_level:
    ingest_cache_directory:
    ingest_pool_size:
    listen_address:
    bind_port:
    interval:
    memcached_hostname:
    memcached_port:
    sqlalchemy_pool_size:
    sqlalchemy_max_overflow:
    db_hostname:
    db_username:
    db_password:
    db_name:
    username:
""")

            # Write config back to directory
            config_dict = yaml.load(config_yaml)
            filepath = ('%s/config.yaml') % (config_directory)
            with open(filepath, 'w') as outfile:
                yaml.dump(config_dict, outfile, default_flow_style=False)

            # Message
            log_message = ('Created blank starter configuration')
            misc.print_ok(log_message)

    def _systemd(self):
        """Determine if systemd is installed.

        Args:
            None

        Returns:
            None

        """
        # Verify
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
