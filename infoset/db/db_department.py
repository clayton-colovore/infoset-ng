"""Module of infoset database functions.

Classes for agent data

"""

# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import general
from infoset.db import db
from infoset.db.db_orm import Department


class GetCodeDepartment(object):
    """Class to return Department data by code.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, code):
        """Function for intializing the class.

        Args:
            code: Department code

        Returns:
            None

        """
        # Initialize important variables
        value = code.encode()
        self.data_dict = defaultdict(dict)
        keys = ['idx_department', 'code', 'name', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Department).filter(Department.code == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx_department'] = instance.idx_department
                self.data_dict[
                    'code'] = general.decode(instance.code)
                self.data_dict[
                    'name'] = general.decode(instance.name)
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


class GetIDXDepartment(object):
    """Class to return device data by idx_department.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_department):
        """Function for intializing the class.

        Args:
            idx_department: Department Index

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        keys = ['idx_department', 'code', 'name', 'enabled']
        for key in keys:
            self.data_dict[key] = None
        self.data_dict['exists'] = False

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(
            Department).filter(Department.idx_department == idx_department)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx_department'] = instance.idx_department
                self.data_dict[
                    'code'] = general.decode(instance.code)
                self.data_dict[
                    'name'] = general.decode(instance.name)
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
        code: Department code

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetCodeDepartment(code)
    if data.exists() is True:
        exists = True

    # Return
    return exists


def idx_department_exists(idx_department):
    """Determine whether the idx_department exists.

    Args:
        idx_department: idx_department value for datapoint

    Returns:
        exists: True if exists

    """
    # Initialize key variables
    exists = False

    # Get information on agent from database
    data = GetIDXDepartment(idx_department)
    if data.exists() is True:
        exists = True

    # Return
    return exists
