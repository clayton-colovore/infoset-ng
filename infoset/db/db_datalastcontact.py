"""Module of infoset database functions.

Classes for DataLastContact data

"""
# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import general
from infoset.db import db
from infoset.db import db_datapoint
from infoset.db.db_orm import DataLastContact, Datapoint


class GetIDDataLastContact(object):
    """Class to return last contact data by datapoint idx_datapoint."""

    def __init__(self, id_datapoint):
        """Function for intializing the class.

        Args:
            id_datapoint: Datapoint Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_datapoint', 'timestamp', 'value']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Only work if the value is an integer
        if (isinstance(id_datapoint, str) is True) and (
                id_datapoint is not None):
            # Get idx_datapoint
            datapoint = db_datapoint.GetIDDatapoint(id_datapoint)
            exists = datapoint.exists()
            idx_datapoint = datapoint.idx_datapoint()

            if exists is True:
                # Establish a database session
                database = db.Database()
                session = database.session()

                # Get results for idx_datapoint
                result = session.query(DataLastContact).filter(
                    DataLastContact.idx_datapoint == idx_datapoint)

                # Massage data
                if result.count() == 1:
                    for instance in result:
                        self.data_dict[
                            'idx_datapoint'] = instance.idx_datapoint
                        self.data_dict[
                            'timestamp'] = instance.timestamp
                        self.data_dict[
                            'value'] = instance.value
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

    def timestamp(self):
        """Get timestamp value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['timestamp']
        return value

    def value(self):
        """Get value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['value']
        return value


class GetIDXDataLastContact(object):
    """Class to return last contact data by datapoint idx_datapoint."""

    def __init__(self, idx_datapoint):
        """Function for intializing the class.

        Args:
            idx_datapoint: DataLastContact Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_datapoint', 'timestamp', 'value']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Only work if the value is an integer
        if (isinstance(idx_datapoint, int) is True) and (
                idx_datapoint is not None):
            # Establish a database session
            database = db.Database()
            session = database.session()
            result = session.query(DataLastContact).filter(
                DataLastContact.idx_datapoint == idx_datapoint)

            # Massage data
            if result.count() == 1:
                for instance in result:
                    self.data_dict['idx_datapoint'] = instance.idx_datapoint
                    self.data_dict[
                        'timestamp'] = instance.timestamp
                    self.data_dict[
                        'value'] = instance.value
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

    def timestamp(self):
        """Get timestamp value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['timestamp']
        return value

    def value(self):
        """Get value value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['value']
        return value


def get_all_last_contacts():
    """Get all current values from database.

    Args:
        None

    Returns:
        listing: List of values

    """
    # Initialize key variables
    data = []
    datapoints = {}

    # Establish a database session
    database = db.Database()
    session = database.session()

    # Get list of enabled datapoints
    result = session.query(
        Datapoint.idx_datapoint, Datapoint.id_datapoint).filter(
            Datapoint.enabled == 1)
    for instance in result:
        idx_datapoint = instance.idx_datapoint
        data_dict = {}
        data_dict['enabled'] = instance.idx_datapoint
        data_dict['id_datapoint'] = general.decode(instance.id_datapoint)
        datapoints[idx_datapoint] = data_dict

    # Add to the list of device idx values
    new_result = session.query(DataLastContact)
    for instance in new_result:
        # Only process existing, enabled datapoints
        idx_datapoint = instance.idx_datapoint
        if idx_datapoint not in datapoints:
            continue
        if idx_datapoint[idx_datapoint]['enabled'] is False:
            continue

        # Process data
        data_dict = {}
        id_datapoint = idx_datapoint[idx_datapoint]['id_datapoint']
        data_dict['idx_datapoint'] = idx_datapoint
        data_dict['id_datapoint'] = id_datapoint
        data_dict['value'] = instance.value
        data_dict['timestamp'] = instance.timestamp
        data.append(data_dict)

    # Return the session to the pool after processing
    database.close()

    # Return
    return data
