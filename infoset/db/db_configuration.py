"""Module of infoset database functions. Configuration table."""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import general
from infoset.db import db
from infoset.db.db_orm import Configuration


class GetConfigurationKey(object):
    """Class to return Configuration data by config_key.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, config_key):
        """Function for intializing the class.

        Args:
            config_key: Configuration config_key

        Returns:
            None

        """
        # Initialize important variables
        value = '{}'.format(config_key).encode()
        self.data_dict = defaultdict(dict)
        keys = ['idx_configuration', 'config_key', 'config_value', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(
            Configuration).filter(Configuration.config_key == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict[
                    'idx_configuration'] = instance.idx_configuration
                self.data_dict['config_key'] = config_key
                self.data_dict[
                    'config_value'] = general.decode(instance.config_value)
                self.data_dict['enabled'] = bool(instance.enabled)
                self.data_dict['exists'] = True
                break

        # Return the session to the database pool after processing
        database.close()

    def exists(self):
        """Tell if row is exists.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['exists']
        return value

    def enabled(self):
        """Get agent enabled.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['enabled']

        # Return
        return value

    def idx_configuration(self):
        """Get idx_configuration value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_configuration']
        return value

    def config_key(self):
        """Get config_key value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['config_key']
        return value

    def config_value(self):
        """Get config_value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['config_value']
        return value


class GetIDXConfiguration(object):
    """Class to return device data by idx_configuration.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_configuration):
        """Function for intializing the class.

        Args:
            idx_configuration: Configuration Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_configuration', 'config_key', 'config_value']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(
            Configuration).filter(
                Configuration.idx_configuration == idx_configuration)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict[
                    'idx_configuration'] = instance.idx_configuration
                self.data_dict[
                    'config_key'] = general.decode(instance.config_key)
                self.data_dict[
                    'config_value'] = general.decode(instance.config_value)
                self.data_dict['exists'] = True
                break

        # Return the session to the database pool after processing
        database.close()

    def exists(self):
        """Tell if row is exists.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['exists']
        return value

    def config_key(self):
        """Get config_key value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['config_key']
        return value

    def config_value(self):
        """Get config_value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['config_value']
        return value


def config_key_exists(config_key):
    """Determine whether the config_key exists.

    Args:
        config_key: Configuration config_key

    Returns:
        found: True if found

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetConfigurationKey(config_key)
    if data.exists() is True:
        exists = True

    # Return
    return exists
