"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import general
from infoset.db import db
from infoset.db.db_orm import Billcode


class GetCodeBillcode(object):
    """Class to return Billcode data by code.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, code):
        """Function for intializing the class.

        Args:
            code: Billcode code

        Returns:
            None

        """
        # Initialize important variables
        value = code.encode()
        self.data_dict = defaultdict(dict)
        keys = ['idx_billcode', 'code', 'name']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Billcode).filter(Billcode.code == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['code'] = code
                self.data_dict['idx_billcode'] = instance.idx_billcode
                self.data_dict[
                    'name'] = general.decode(instance.name)
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

    def code(self):
        """Get code value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['code']
        return value

    def name(self):
        """Get name value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
        return value


class GetIDXBillcode(object):
    """Class to return device data by idx_billcode.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_billcode):
        """Function for intializing the class.

        Args:
            idx_billcode: Billcode Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_billcode', 'code', 'name']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(
            Billcode).filter(Billcode.idx_billcode == idx_billcode)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx_billcode'] = instance.idx_billcode
                self.data_dict[
                    'code'] = general.decode(instance.code)
                self.data_dict[
                    'name'] = general.decode(instance.name)
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

    def code(self):
        """Get code value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['code']
        return value

    def name(self):
        """Get name value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
        return value


def code_exists(code):
    """Determine whether the code exists.

    Args:
        code: Billcode code

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetCodeBillcode(code)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def idx_billcode_exists(idx_billcode):
    """Determine whether the idx_billcode exists.

    Args:
        idx_billcode: idx_billcode value for datapoint

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetIDXBillcode(idx_billcode)
    if data.exists() is True:
        exists = True

    # Return
    return exists
