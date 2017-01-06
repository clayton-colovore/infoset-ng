#!/usr/bin/env python3
"""Class used to set global variables used by unittests."""

# Standard imports
import tempfile
import os
import sys
import yaml

# Infoset libraries
try:
    from infoset.utils import log
except:
    print('You need to set your PYTHONPATH to include the infoset library')
    sys.exit(2)

# Initialize GLOBAL variables
CONFIG_DIRECTORY = '{}/.infoset_unittests/config'.format(os.environ['HOME'])


class TestVariables(object):
    """Creates variables for ingestion and ingest validation testing."""

    def __init__(self):
        """Method initializing the class."""
        # Initialize key variables
        self.data = {}

        # Data used for testing cache validation
        self.data['cache_data'] = {
            'agent': 'unittest',
            'timeseries': {
                'cpu_count': {'base_type': 1,
                              'data': [[0, 2, None]],
                              'description': 'CPU Count'},
                'packets_recv': {'base_type': 64,
                                 'data': [['lo', 304495689, 'lo'],
                                          ['p10p1', 84319802, 'p10p1']],
                                 'description': 'Packets (In)'},
                'packets_sent': {'base_type': 64,
                                 'data': [['lo', 304495689, 'lo'],
                                          ['p10p1',
                                           123705549, 'p10p1']],
                                 'description': 'Packets (Out)'},
                'swap_used': {'base_type': 32,
                              'data': [[None, 363606016, None]],
                              'description': 'Swap Used'}},
            'devicename': 'unittest_device',
            'id_agent': 'a0810e3e36c59ea3cbdab599dcdb8'
                        '24fb468314b7340543493271ad',
            'timefixed': {
                'distribution': {'base_type': None,
                                 'data': [[0, 'Ubuntu 16.04 xenial', None]],
                                 'description': 'Linux Distribution'},
                'version': {'base_type': None,
                            'data': [[0, '#62-Ubuntu SMP', None]],
                            'description': 'Kernel Type'}},
            'timestamp': 1481561700}

    def cache_data(self):
        """Return the contents of known working cache data."""
        # Initialize key variables
        result = self.data['cache_data']
        return result


class TestConfig(object):
    """Creates configuration for testing."""

    def __init__(self):
        """Method initializing the class."""
        # Set global variables
        global CONFIG_DIRECTORY
        self._log_directory = tempfile.mkdtemp()
        self._ingest_cache_directory = tempfile.mkdtemp()

        # Make sure the environmental variables are OK
        _environment()

        # Make sure the configuration directory is OK
        self._config_directory = CONFIG_DIRECTORY
        if os.path.isdir(CONFIG_DIRECTORY) is False:
            os.makedirs(CONFIG_DIRECTORY, mode=0o750, exist_ok=True)

        self._config = {
            'main': {
                'log_directory': self._log_directory,
                'log_level': 'debug',
                'ingest_cache_directory': self._ingest_cache_directory,
                'ingest_pool_size': 20,
                'bind_port': 3000,
                'interval': 300,
                'sqlalchemy_pool_size': 10,
                'sqlalchemy_max_overflow': 10,
                'db_hostname': 'localhost',
                'db_username': 'test_infoset',
                'db_password': 'A6azWBWDnvnX5VnF',
                'db_name': 'test_infoset'
            }
        }

    def create(self):
        """Create a good config and set the INFOSET_CONFIGDIR variable.

        Args:
            None

        Returns:
            self.config_directory: Directory where the config is placed

        """
        # Initialize key variables
        config_file = ('%s/test_config.yaml') % (self._config_directory)

        # Write good_config to file
        with open(config_file, 'w') as f_handle:
            yaml.dump(self._config, f_handle, default_flow_style=False)

        # Return
        return self._config_directory

    def cleanup(self):
        """Remove all residual directories.

        Args:
            None

        Returns:
            None

        """
        # Delete directories
        directories = [
            self._log_directory,
            self._ingest_cache_directory,
            self._config_directory]
        for directory in directories:
            _delete_files(directory)


def _delete_files(directory):
    """Delete all files in directory."""
    # Cleanup files in temp directories
    filenames = [filename for filename in os.listdir(
        directory) if os.path.isfile(
            os.path.join(directory, filename))]

    # Get the full filepath for the cache file and remove filepath
    for filename in filenames:
        filepath = os.path.join(directory, filename)
        os.remove(filepath)

    # Remove directory after files are deleted.
    os.rmdir(directory)


def _environment():
    """Make sure environmental variables are OK.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    global CONFIG_DIRECTORY

    # Make sure the INFOSET_CONFIGDIR environment variable is set
    if 'INFOSET_CONFIGDIR' not in os.environ:
        log_message = (
            'The INFOSET_CONFIGDIR is not set. Run this command to do so: '
            '"export INFOSET_CONFIGDIR={}"'.format(CONFIG_DIRECTORY))
        log.log2die_safe(1084, log_message)

    # Make sure the INFOSET_CONFIGDIR environment variable is set correctly
    if os.environ['INFOSET_CONFIGDIR'] != CONFIG_DIRECTORY:
        log_message = (
            'The INFOSET_CONFIGDIR is not set. Run this command to do so: '
            '"export INFOSET_CONFIGDIR={}"'.format(CONFIG_DIRECTORY))
        log.log2die_safe(1083, log_message)


def ready():
    """Verify that we are ready to run tests."""
    # Check environment
    _environment()


def main():
    """Verify that we are ready to run tests."""
    # Check environment
    config = TestConfig()
    config.create()


if __name__ == '__main__':
    # Do the unit test
    main()
