#!/usr/bin/env python3
"""infoset classes that manage various configurations."""

import os.path
import os

# Import project libraries
from infoset.utils import general
from infoset.utils import log


class Config(object):
    """Class gathers all configuration information."""

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        # Initialize key variables
        directories = general.config_directories()
        self.config_dict = general.read_yaml_files(directories)

    def ingest_cache_directory(self):
        """Determine the ingest_cache_directory.

        Args:
            None

        Returns:
            value: configured ingest_cache_directory

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'ingest_cache_directory'

        # Process configuration
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'ingest_cache_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1011, log_message)

        # Return
        return value

    def ingest_failures_directory(self):
        """Determine the ingest_failures_directory.

        Args:
            None

        Returns:
            value: configured ingest_failures_directory

        """
        # Get parameter
        value = ('%s/failures') % (self.ingest_cache_directory())

        # Check if value exists
        if os.path.exists(value) is False:
            os.makedirs(value, mode=0o755)

        # Return
        return value

    def db_name(self):
        """Get db_name.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_name'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def db_username(self):
        """Get db_username.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_username'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def db_password(self):
        """Get db_password.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_password'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def db_hostname(self):
        """Get db_hostname.

        Args:
            None

        Returns:
            result: result

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'db_hostname'

        # Process configuration
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Get result
        return result

    def listen_address(self):
        """Get listen_address.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'listen_address'
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 0.0.0.0
        if result is None:
            result = '0.0.0.0'
        return result

    def interval(self):
        """Get interval.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'interval'
        intermediate = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 300
        if intermediate is None:
            result = 300
        else:
            result = int(intermediate)
        return result

    def bind_port(self):
        """Get bind_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'bind_port'
        intermediate = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 6000
        if intermediate is None:
            result = 6000
        else:
            result = int(intermediate)
        return result

    def ingest_pool_size(self):
        """Get ingest_pool_size.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'ingest_pool_size'
        intermediate = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to 20
        if intermediate is None:
            result = 20
        else:
            result = int(intermediate)
        return result

    def sqlalchemy_pool_size(self):
        """Get sqlalchemy_pool_size.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'sqlalchemy_pool_size'
        intermediate = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Set default
        if intermediate is None:
            result = 10
        else:
            result = int(intermediate)
        return result

    def memcached_port(self):
        """Get memcached_port.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'memcached_port'
        intermediate = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Set default
        if intermediate is None:
            result = 11211
        else:
            result = int(intermediate)
        return result

    def memcached_hostname(self):
        """Get memcached_hostname.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'memcached_hostname'
        result = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Default to localhost
        if result is None:
            result = 'localhost'
        return result

    def sqlalchemy_max_overflow(self):
        """Get sqlalchemy_max_overflow.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        key = 'main'
        sub_key = 'sqlalchemy_max_overflow'
        intermediate = _key_sub_key(key, sub_key, self.config_dict, die=False)

        # Set default
        if intermediate is None:
            result = 10
        else:
            result = int(intermediate)
        return result

    def log_directory(self):
        """Determine the log_directory.

        Args:
            None

        Returns:
            value: configured log_directory

        """
        # Initialize key variables
        key = 'main'
        sub_key = 'log_directory'

        # Process configuration
        value = _key_sub_key(key, sub_key, self.config_dict)

        # Check if value exists
        if os.path.isdir(value) is False:
            log_message = (
                'log_directory: "%s" '
                'in configuration doesn\'t exist!') % (value)
            log.log2die(1030, log_message)

        # Return
        return value

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = ('%s/infoset-ng.log') % (self.log_directory())

        # Return
        return result

    def web_log_file(self):
        """Get web_log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get new result
        result = ('%s/api-web.log') % (self.log_directory())

        # Return
        return result

    def log_level(self):
        """Get log_level.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'log_level'
        result = None
        key = 'main'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Return
        return result


def _key_sub_key(key, sub_key, config_dict, die=True):
    """Get config parameter from YAML.

    Args:
        key: Primary key
        sub_key: Secondary key
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    result = None

    # Verify config_dict is indeed a dict.
    # Die safely as log_directory is not defined
    if isinstance(config_dict, dict) is False:
        log.log2die_safe(1021, 'Invalid configuration file. YAML not found')

    # Get new result
    if key in config_dict:
        # Make sure we don't have a None value
        if config_dict[key] is None:
            log_message = (
                'Configuration value {}: is blank. Please fix.'
                ''.format(key))
            log.log2die_safe(1129, log_message)

        # Get value we need
        if sub_key in config_dict[key]:
            result = config_dict[key][sub_key]

    # Error if not configured
    if result is None and die is True:
        log_message = (
            '%s:%s not defined in configuration') % (key, sub_key)
        log.log2die_safe(1016, log_message)

    # Return
    return result
