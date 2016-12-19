#!/usr/bin/env python3
"""infoset classes that manage various configurations."""

import os.path
import os

# Import project libraries
from infoset.utils import general
from infoset.utils import log


class Config(object):
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        devices:
        snmp_auth:
    """

    def __init__(self):
        """Function for intializing the class.

        Args:
            None

        Returns:
            None

        """
        #####################################################################
        # Update the configuration directory
        # 'INFOSET_CONFIGDIR' is used for setting a non-default config
        # directory location. A good example of this is using a new config
        # directory for unit testing
        #####################################################################
        if 'INFOSET_CONFIGDIR' in os.environ:
            config_directory = os.environ['INFOSET_CONFIGDIR']
        else:
            config_directory = ('%s/etc') % (general.root_directory())
        directories = [config_directory]

        # Return
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
            log.log2die(1030, log_message)

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

    def log_file(self):
        """Get log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'log_file'
        result = None
        key = 'main'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

        # Return
        return result

    def web_log_file(self):
        """Get web_log_file.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        sub_key = 'web_log_file'
        result = None
        key = 'main'

        # Get new result
        result = _key_sub_key(key, sub_key, self.config_dict)

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

    def agents(self):
        """Get agents.

        Args:
            None

        Returns:
            result: list of agents

        """
        # Initialize key variables
        key = 'agents'
        result = None

        # Verify data
        if key not in self.config_dict:
            log_message = ('No agents configured')
            log.log2die(1100, log_message)

        # Process agents
        result = self.config_dict[key]

        # Return
        return result

    def _config(self):
        """Get the config as a dict.

        Args:
            None

        Returns:
            data: configuration

        """
        # Initialize key variables
        data = self.config_dict
        return data


class ConfigAgent(Config):
    """Class gathers all configuration information.

    Args:
        None

    Returns:
        None

    Functions:
        __init__:
        devices:
        snmp_auth:
    """

    def __init__(self, agent_name):
        """Function for intializing the class.

        Args:
            agent_name: Name of agent used to get descriptions
                from configuration subdirectory

        Returns:
            None

        """
        # Intialize key variables
        self._agent_name = agent_name

        # Instantiate the Config parent
        Config.__init__(self)

        # Get config as dictionary
        self.config_dict = self._config()

    def agent_name(self):
        """Get agent_name.

        Args:
            None

        Returns:
            result: result

        """
        # Get result
        result = self._agent_name
        return result

    def agent_enabled(self):
        """Get agent_enabled.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        if 'agent_enabled' in agent_config:
            result = bool(agent_config['agent_enabled'])
        else:
            result = False
        return result

    def monitor_agent_pid(self):
        """Get monitor_agent_pid.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        if 'monitor_agent_pid' in agent_config:
            result = bool(agent_config['monitor_agent_pid'])
        else:
            result = False
        return result

    def agent_filename(self):
        """Get agent_filename.

        Args:
            None

        Returns:
            result: result

        """
        # Get config
        agent_config = _agent_config(self.agent_name(), self.config_dict)

        # Get result
        result = agent_config['agent_filename']
        return result


def _agent_config(agent_name, config_dict):
    """Get agent config parameter from YAML.

    Args:
        agent_name: Agent Name
        config_dict: Dictionary to explore
        die: Die if true and the result encountered is None

    Returns:
        result: result

    """
    # Get result
    key = 'agents'
    result = None

    # Get new result
    if key in config_dict:
        configurations = config_dict[key]
        for configuration in configurations:
            if 'agent_name' in configuration:
                if configuration['agent_name'] == agent_name:
                    result = configuration
                    break

    # Error if not configured
    if result is None:
        log_message = (
            'Agent %s not defined in configuration in '
            'agents:%s section') % (key, key)
        log.log2die(1094, log_message)

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

    # Get new result
    if key in config_dict:
        if sub_key in config_dict[key]:
            result = config_dict[key][sub_key]

    # Error if not configured
    if result is None and die is True:
        log_message = (
            '%s:%s not defined in configuration') % (key, sub_key)
        log.log2die(1016, log_message)

    # Return
    return result
