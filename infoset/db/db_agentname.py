"""Module of infoset database functions. AgentName table."""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import general
from infoset.db import db
from infoset.db.db_orm import AgentName


class GetIDXAgentName(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_agentname):
        """Function for intializing the class.

        Args:
            idx_agentname: AgentName idx_agentname

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_agentname', 'name', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Fix values passed
        if isinstance(idx_agentname, int) is False:
            idx_agentname = None

        # Only work if the value is an integer
        if (isinstance(idx_agentname, int) is True) and (
                idx_agentname is not None):
            # Get the result
            database = db.Database()
            session = database.session()
            result = session.query(AgentName).filter(
                AgentName.idx_agentname == idx_agentname)

            # Massage data
            if result.count() == 1:
                for instance in result:
                    self.data_dict['idx_agentname'] = idx_agentname
                    self.data_dict['name'] = general.decode(instance.name)
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

    def idx_agentname(self):
        """Get idx_agentname value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_agentname']
        return value

    def name(self):
        """Get agent name.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
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

    def everything(self):
        """Get all agent data.

        Args:
            None

        Returns:
            value: Data as a dict

        """
        # Initialize key variables
        value = self.data_dict
        return value


class GetAgentName(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, name):
        """Function for intializing the class.

        Args:
            name: Name of agent

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_agentname', 'name', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Encode the Name
        value = '{}'.format(name).encode()

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(AgentName).filter(AgentName.name == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx_agentname'] = instance.idx_agentname
                self.data_dict['name'] = name
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

    def idx_agentname(self):
        """Get idx_agentname value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_agentname']
        return value

    def name(self):
        """Get agent name.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
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

    def everything(self):
        """Get all agent data.

        Args:
            None

        Returns:
            value: Data as a dict

        """
        # Initialize key variables
        value = self.data_dict
        return value


def name_exists(name):
    """Determine whether the Identifier exists.

    Args:
        name: Identifier value for agent

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    value = '{}'.format(name)
    data = GetAgentName(value)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def idx_agentname_exists(idx_agentname):
    """Determine whether the idx_agentname exists.

    Args:
        idx_agentname: idx_agentname value for datapoint

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Fix values passed
    if isinstance(idx_agentname, int) is False:
        idx_agentname = None

    # Get information on agent from database
    data = GetIDXAgentName(idx_agentname)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def get_all_names():
    """Get data on all names in the database.

    Args:
        None

    Returns:
        data: List of dicts of agent data.

    """
    # Initialize important variables
    data = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(AgentName)

    # Massage data
    for instance in result:
        # Get next record
        data_dict = defaultdict(dict)
        data_dict['name'] = general.decode(instance.name)
        data_dict['idx_agentname'] = instance.idx_agentname
        data_dict['enabled'] = bool(instance.enabled)
        data_dict['exists'] = True

        # Append to list
        data.append(data_dict)

    # Return the session to the database pool after processing
    database.close()

    # Return
    return data
