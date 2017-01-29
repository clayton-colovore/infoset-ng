"""Module of infoset database functions. Datapoint table."""

# Python standard libraries
from collections import defaultdict

# PIP libraries
from sqlalchemy import and_

# Infoset libraries
from infoset.utils import general
from infoset.db import db
from infoset.db import db_deviceagent
from infoset.db.db_orm import Datapoint


class GetIDDatapoint(object):
    """Class to return datapoint data by datapoint idx_datapoint.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, id_datapoint):
        """Function for intializing the class.

        Args:
            id_datapoint: Datapoint ID

        Returns:
            None

        """
        # Initialize important variables
        if isinstance(id_datapoint, str) is True:
            value = id_datapoint.encode()
        else:
            value = None
        self.data_dict = defaultdict(dict)
        keys = [
            'idx_datapoint', 'id_datapoint', 'idx_deviceagent',
            'idx_department',
            'idx_billcode', 'agent_label', 'agent_source', 'enabled',
            'billable', 'base_type', 'timefixed_value', 'last_timestamp']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(
            Datapoint).filter(Datapoint.id_datapoint == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx_datapoint'] = instance.idx_datapoint
                self.data_dict['id_datapoint'] = id_datapoint
                self.data_dict['idx_deviceagent'] = instance.idx_deviceagent
                self.data_dict['idx_department'] = instance.idx_department
                self.data_dict['idx_billcode'] = instance.idx_billcode
                self.data_dict[
                    'agent_label'] = general.decode(instance.agent_label)
                self.data_dict[
                    'agent_source'] = general.decode(instance.agent_source)
                self.data_dict['enabled'] = bool(instance.enabled)
                self.data_dict['billable'] = bool(instance.billable)
                self.data_dict[
                    'base_type'] = general.decode(instance.base_type)
                self.data_dict['timefixed_value'] = instance.timefixed_value
                self.data_dict['last_timestamp'] = instance.last_timestamp
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

    def timefixed_value(self):
        """Get timefixed_value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['timefixed_value']
        return value

    def base_type(self):
        """Get base_type value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['base_type']
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

    def billable(self):
        """Get billable value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['billable']
        return value

    def agent_source(self):
        """Get agent_source value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_source']
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

    def id_datapoint(self):
        """Get id_datapoint value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['id_datapoint']
        return value

    def idx_datapoint(self):
        """Get idx_datapoint value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_datapoint']
        return value

    def idx_department(self):
        """Get idx_department value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_department']
        return value

    def idx_billcode(self):
        """Get idx_billcode value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_billcode']
        return value

    def agent_label(self):
        """Get agent_label value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_label']
        return value


class GetIDXDatapoint(object):
    """Class to return datapoint data by datapoint idx_datapoint.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_datapoint):
        """Function for intializing the class.

        Args:
            idx_datapoint: Datapoint Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = [
            'idx_datapoint', 'id_datapoint', 'idx_deviceagent',
            'idx_department',
            'idx_billcode', 'agent_label', 'agent_source', 'enabled',
            'billable', 'base_type', 'timefixed_value', 'last_timestamp']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Only work if the value is an integer
        if (isinstance(idx_datapoint, int) is True) and (
                idx_datapoint is not None):
            # Establish a database session
            database = db.Database()
            session = database.session()
            result = session.query(
                Datapoint).filter(Datapoint.idx_datapoint == idx_datapoint)

            # Massage data
            if result.count() == 1:
                for instance in result:
                    self.data_dict['idx_datapoint'] = instance.idx_datapoint
                    self.data_dict[
                        'id_datapoint'] = general.decode(
                            instance.id_datapoint)
                    self.data_dict[
                        'idx_deviceagent'] = instance.idx_deviceagent
                    self.data_dict['idx_department'] = instance.idx_department
                    self.data_dict['idx_billcode'] = instance.idx_billcode
                    self.data_dict[
                        'agent_label'] = general.decode(
                            instance.agent_label)
                    self.data_dict[
                        'agent_source'] = general.decode(
                            instance.agent_source)
                    self.data_dict['enabled'] = bool(instance.enabled)
                    self.data_dict['billable'] = bool(instance.billable)
                    self.data_dict['base_type'] = instance.base_type
                    self.data_dict[
                        'timefixed_value'] = instance.timefixed_value
                    self.data_dict['last_timestamp'] = instance.last_timestamp
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

    def timefixed_value(self):
        """Get timefixed_value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['timefixed_value']
        return value

    def base_type(self):
        """Get base_type value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['base_type']
        return value

    def billable(self):
        """Get billable value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['billable']
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

    def agent_source(self):
        """Get agent_source value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_source']
        return value

    def idx_datapoint(self):
        """Get idx_datapoint value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_datapoint']
        return value

    def id_datapoint(self):
        """Get id_datapoint value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['id_datapoint']
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

    def idx_department(self):
        """Get idx_department value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_department']
        return value

    def idx_billcode(self):
        """Get idx_billcode value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx_billcode']
        return value

    def agent_label(self):
        """Get agent_label value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['agent_label']
        return value


def id_datapoint_exists(id_datapoint):
    """Determine whether the DID exists.

    Args:
        id_datapoint: DID value for datapoint

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetIDDatapoint(id_datapoint)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def idx_datapoint_exists(idx_datapoint):
    """Determine whether the idx_datapoint exists.

    Args:
        idx_datapoint: idx_datapoint value for datapoint

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetIDXDatapoint(idx_datapoint)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def listing(idx_deviceagent, base_type=None):
    """List of datapoint data for a specific idx_device, idx_agent combination.

    Args:
        idx_deviceagent: DeviceAgent index
        base_type: base_type to filter by

    Returns:
        dict_list: List of dicts containing data

    """
    # Initialize key variables
    dict_list = []

    # Process information
    deviceagent = db_deviceagent.GetIDXDeviceAgent(idx_deviceagent)
    if deviceagent.exists() is True:
        # Establish a database session
        database = db.Database()
        session = database.session()
        if base_type is None:
            result = session.query(Datapoint).filter(
                Datapoint.idx_deviceagent == idx_deviceagent)
        else:
            result = session.query(Datapoint).filter(
                and_(
                    Datapoint.base_type == base_type,
                    Datapoint.idx_deviceagent == idx_deviceagent)
                )

        # Add to the list of device idx_datapoint values
        for instance in result:
            data_dict = {}
            data_dict['idx_datapoint'] = instance.idx_datapoint
            data_dict['id_datapoint'] = general.decode(instance.id_datapoint)
            data_dict['idx_deviceagent'] = instance.idx_deviceagent
            data_dict['idx_department'] = instance.idx_department
            data_dict['idx_billcode'] = instance.idx_billcode
            data_dict[
                'agent_label'] = general.decode(instance.agent_label)
            data_dict[
                'agent_source'] = general.decode(instance.agent_source)
            data_dict['enabled'] = bool(instance.enabled)
            data_dict['billable'] = bool(instance.billable)
            data_dict['base_type'] = instance.base_type
            data_dict[
                'timefixed_value'] = general.decode(instance.timefixed_value)
            data_dict['last_timestamp'] = instance.last_timestamp
            data_dict['exists'] = True
            dict_list.append(data_dict)

        # Return the connection to the pool
        database.close()

    # Return
    return dict_list
