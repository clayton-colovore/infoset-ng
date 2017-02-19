"""Module of infoset database functions. Device table."""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import general
from infoset.db import db
from infoset.db.db_orm import Device


class GetDevice(object):
    """Class to return device data by devicename.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, devicename):
        """Function for intializing the class.

        Args:
            devicename: Devicename

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = [
            'idx_device', 'devicename', 'description', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Encode the id_agent
        if isinstance(devicename, str) is True:
            value = devicename.encode()
        else:
            value = None

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Device).filter(Device.devicename == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx_device'] = instance.idx_device
                self.data_dict[
                    'devicename'] = devicename
                self.data_dict[
                    'description'] = general.decode(instance.description)
                self.data_dict['enabled'] = bool(instance.enabled)
                self.data_dict['exists'] = True
                break

        # Return the session to the database pool after processing
        database.close()

    def exists(self):
        """Tell if row is found.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['exists']
        return value

    def idx_device(self):
        """Get idx_device value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_device']
        return value

    def devicename(self):
        """Get devicename value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['devicename']
        return value

    def description(self):
        """Get description value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['description']
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


class GetIDXDevice(object):
    """Class to return device data by idx_device.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_device):
        """Function for intializing the class.

        Args:
            idx_device: Device Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = [
            'idx_device', 'devicename', 'description', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Only work if the value is an integer
        if isinstance(idx_device, int) is True and idx_device is not None:
            # Establish a database session
            database = db.Database()
            session = database.session()
            result = session.query(
                Device).filter(Device.idx_device == idx_device)

            # Massage data
            if result.count() == 1:
                for instance in result:
                    self.data_dict['idx_device'] = instance.idx_device
                    self.data_dict['devicename'] = general.decode(
                        instance.devicename)
                    self.data_dict['description'] = general.decode(
                        instance.description)
                    self.data_dict['enabled'] = bool(instance.enabled)
                    self.data_dict['exists'] = True
                    break

            # Return the session to the database pool after processing
            database.close()

    def exists(self):
        """Tell if row is found.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['exists']
        return value

    def idx_device(self):
        """Get idx_device value.

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

    def devicename(self):
        """Get devicename value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['devicename']
        return value

    def description(self):
        """Get description value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['description']
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


def all_devices(enabled=True):
    """Get list of all devices.

    Args:
        enabled: Only return enabled devices if true

    Returns:
        devicelist: List of dicts of device data

    """
    devicelist = []
    idx_device_list = []

    # Establish a database session
    database = db.Database()
    session = database.session()
    if enabled is True:
        result = session.query(Device.idx_device).filter(Device.enabled == 1)
    else:
        result = session.query(Device.idx_device)

    # Add to the list of device idx_device values
    for instance in result:
        idx_device_list.append(instance.idx_device)

    # Get device information
    if bool(idx_device_list) is True:
        for idx_device in idx_device_list:
            data_dict = {}
            device = GetIDXDevice(idx_device)
            data_dict['devicename'] = device.devicename()
            data_dict['description'] = device.description()
            data_dict['enabled'] = device.enabled()
            data_dict['exists'] = True
            devicelist.append(data_dict)

    # Return the session to the database pool after processing
    database.close()

    # Return
    return devicelist


def devicename_exists(devicename):
    """Determine whether the devicename exists.

    Args:
        devicename: Devicename

    Returns:
        exists: True if found

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetDevice(devicename)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def idx_device_exists(idx_device):
    """Determine whether the idx_device exists.

    Args:
        idx_device: idx_device value for datapoint

    Returns:
        exists: True if found

    """
    # Initialize key variables
    exists = False

    # Fix values passed
    if isinstance(idx_device, int) is False:
        idx_device = None

    # Get information on agent from database
    data = GetIDXDevice(idx_device)
    if data.exists() is True:
        exists = True

    # Return
    return exists
