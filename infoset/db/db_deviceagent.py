"""Module of infoset database functions. DeviceAgent table."""

# Python standard libraries
from collections import defaultdict

# Python libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.db import db
from infoset.db.db_orm import DeviceAgent


class GetIDXDeviceAgent(object):
    """Class to return deviceagent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_deviceagent):
        """Function for intializing the class.

        Args:
            idx_deviceagent: DeviceAgent idx_deviceagent

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_deviceagent', 'idx_agent', 'enabled', 'idx_device']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Fix values passed
        if isinstance(idx_deviceagent, int) is False:
            idx_deviceagent = None

        # Only work if the value is an integer
        if isinstance(idx_deviceagent, int) is True and (
                idx_deviceagent is not None):
            # Get the result
            database = db.Database()
            session = database.session()
            result = session.query(DeviceAgent).filter(
                DeviceAgent.idx_deviceagent == idx_deviceagent)

            # Massage data
            if result.count() == 1:
                for instance in result:
                    self.data_dict['idx_deviceagent'] = idx_deviceagent
                    self.data_dict['idx_agent'] = instance.idx_agent
                    self.data_dict['enabled'] = bool(instance.enabled)
                    self.data_dict['idx_device'] = instance.idx_device
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

    def idx_deviceagent(self):
        """Get idx_deviceagent value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_deviceagent']
        return value

    def idx_agent(self):
        """Get idx_agent value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_agent']
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

    def idx_device(self):
        """Get agent idx_device.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_device']
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


class GetDeviceAgent(object):
    """Class to return DeviceAgent data by device and agent idx.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_device, idx_agent):
        """Method initializing the class.

        Args:
            idx_device: Device idx
            idx_agent: Agent idx

        Returns:
            None

        """
        # Initialize key variables
        self.data_dict = defaultdict(dict)
        keys = ['last_timestamp', 'idx_deviceagent', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Fix values passed
        if isinstance(idx_device, int) is False:
            idx_device = None
        if isinstance(idx_agent, int) is False:
            idx_agent = None

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(DeviceAgent).filter(and_(
            DeviceAgent.idx_device == idx_device,
            DeviceAgent.idx_agent == idx_agent))

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['last_timestamp'] = instance.last_timestamp
                self.data_dict['idx_deviceagent'] = instance.idx_deviceagent
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
        """Get enabled value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['enabled']
        return value

    def last_timestamp(self):
        """Get last_timestamp value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['last_timestamp']
        return value

    def idx_deviceagent(self):
        """Get idx_deviceagent value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_deviceagent']
        return value


def device_agent_exists(idx_device, idx_agent):
    """Determine whether a device / agent entry exists in the DeviceAgent table.

    Args:
        idx_device: Device idx
        idx_agent: Agent idx

    Returns:
        found: True if found

    """
    # Initialize key variables
    exists = False

    # Fix values passed
    if isinstance(idx_device, int) is False:
        idx_device = None
    if isinstance(idx_agent, int) is False:
        idx_agent = None

    # Get information on agent from database
    data = GetDeviceAgent(idx_device, idx_agent)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def all_device_indices():
    """Get list of all device indexes in database.

    Args:
        None

    Returns:
        listing: List of indexes

    """
    idx_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(DeviceAgent.idx_device)

    # Add to the list of device idx values
    for instance in result:
        idx_list.append(instance.idx_device)

    # Return the session to the pool after processing
    database.close()

    # Return
    return list(set(idx_list))


def device_indices(idx_agent):
    """Get list of all device indexes for a specific agent_idx.

    Args:
        None

    Returns:
        listing: List of indexes

    """
    idx_list = []

    # Fix values passed
    if isinstance(idx_agent, int) is False:
        idx_agent = None

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(DeviceAgent.idx_device).filter(
        DeviceAgent.idx_agent == idx_agent)

    # Add to the list of device idx values
    for instance in result:
        idx_list.append(instance.idx_device)

    # Return the session to the pool after processing
    database.close()

    # Return
    return list(set(idx_list))


def agent_indices(idx_device):
    """Get list of all agent indexes for a specific device_idx.

    Args:
        None

    Returns:
        listing: List of indexes

    """
    idx_list = []

    # Fix values passed
    if isinstance(idx_device, int) is False:
        idx_device = None

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(DeviceAgent.idx_agent).filter(
        DeviceAgent.idx_device == idx_device)

    # Add to the list of device idx values
    for instance in result:
        idx_list.append(instance.idx_agent)

    # Return the session to the pool after processing
    database.close()

    # Return
    return idx_list


def get_all_device_agents():
    """Get list of all DeviceAgent indexes.

    Args:
        None

    Returns:
        listing: List of indexes

    """
    data = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(DeviceAgent)

    # Add to the list of device idx values
    for instance in result:
        data_dict = {}
        data_dict['idx_deviceagent'] = instance.idx_deviceagent
        data_dict['idx_agent'] = instance.idx_agent
        data_dict['idx_device'] = instance.idx_device
        data.append(data_dict)

    # Return the session to the pool after processing
    database.close()

    # Return
    return data
