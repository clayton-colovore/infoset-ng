#!/usr/bin/env python3
"""This module sets up the database for specific unittests.

The TestDatabase class can create, drop a configured database. It can also
create empty tables for the database.

There are related functions for populating specific tables for unittests.

There are also functions for validating that the configured database
is a test database.

"""

# Standard imports

# PIP3 imports
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy import and_

# Import infoset libraries
from infoset.utils import configuration
from infoset.utils import log
from infoset.utils import general
from infoset.db.db_orm import BASE, Agent, Device, DeviceAgent, Billcode, Department
from infoset.db.db_orm import Department
from infoset.db import URL, TEST_ENGINE
from infoset.db import db
from infoset.db import db_agent
from infoset.db import db_device
from infoset.db import db_deviceagent as hagent


class TestDatabase(object):
    """Manage the basic operations of database setup for unittests.

    This includes methods for creating and dropping the database.
    This class also has the ability to create empty tables.

    """

    def __init__(self):
        """Method initializing the class."""
        # Initialize key variables
        self.url = URL
        self.engine = TEST_ENGINE

        # Validate the database
        validate()

        # Get configuration
        self.config = configuration.Config()

    def drop(self):
        """Drop database if exists."""
        # Initialize key variables
        if database_exists(self.url) is True:
            drop_database(self.url)

    def create(self):
        """Create database if exists."""
        # Initialize key variables
        if database_exists(self.url) is False:
            create_database(self.url)

        # Alter the encoding for database character set
        sql_string = (
            'ALTER DATABASE %s CHARACTER SET utf8mb4 '
            'COLLATE utf8mb4_general_ci') % (self.config.db_name())
        self.engine.execute(sql_string)

    def populate(self):
        """Create tables."""
        # Apply schemas
        if database_exists(self.url) is True:
            BASE.metadata.create_all(self.engine)


def validate():
    """Make sure we are using a test database."""
    # Get configuration
    config = configuration.Config()

    # Only work on test databases
    if config.db_name().startswith('test_') is False:
        log_message = (
            'Test database not found in configuration. '
            'Try setting your "INFOSET_CONFIGDIR" environment '
            'variable to a directory with a test configuration')
        log.log2die(1017, log_message)


def setup_db_deviceagent(data):
    """Create the database for DeviceAgent table testing.

    Args:
        None

    Returns:
        result: Tuple of (idx_device, idx_agent)

    """
    # Initialize key variables
    devicename = data['devicename']
    id_agent = data['id_agent']
    agent_name = data['agent']
    last_timestamp = data['timestamp']

    # Add record to the database
    record = Agent(
        id_agent=general.encode(id_agent),
        name=general.encode(agent_name))
    database = db.Database()
    database.add(record, 1081)

    # Get idx_agent value from database
    agent_info = db_agent.GetIDAgent(id_agent)
    idx_agent = agent_info.idx_agent()

    # Add record to the database
    record = Device(devicename=general.encode(devicename))
    database = db.Database()
    database.add(record, 1080)

    # Get idx of newly added device
    device_info = db_device.GetDevice(devicename)
    idx_device = device_info.idx_device()

    # Update DeviceAgent table
    if hagent.device_agent_exists(idx_device, idx_agent) is False:
        # Add to DeviceAgent table
        record = DeviceAgent(idx_device=idx_device, idx_agent=idx_agent)
        database = db.Database()
        database.add(record, 1038)

    # Update DeviceAgent table with timestamp
    database = db.Database()
    session = database.session()
    record = session.query(DeviceAgent).filter(
        and_(
            DeviceAgent.idx_device == idx_device,
            DeviceAgent.idx_agent == idx_agent)).one()
    record.last_timestamp = last_timestamp
    database.commit(session, 1124)

    # Return
    result = (idx_agent, idx_device)
    return result


def setup_db_agent():
    """Create the database for Agent table testing.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_agent = 1

    # Get an agent ID
    id_agent = general.hashstring('_INFOSET_TEST_')
    last_timestamp = general.normalized_timestamp()

    # Create a dict of all the expected values
    expected = {
        'id_agent': id_agent,
        'last_timestamp': last_timestamp,
        'name': general.hashstring(general.randomstring()),
        'idx_agent': idx_agent,
        'enabled': 1
    }

    # Drop the database and create tables
    initialize_db()

    # Insert data into database
    data = Agent(
        id_agent=general.encode(expected['id_agent']),
        name=general.encode(expected['name']),
        enabled=expected['enabled'],
        last_timestamp=expected['last_timestamp'])
    database = db.Database()
    database.add_all([data], 1018)

    # Return
    return(id_agent, expected)


def initialize_db():
    """Create the database for validating ingest cache files.

    Args:
        None

    Returns:
        None

    """
    # Drop the database and create tables
    setup_database = TestDatabase()
    setup_database.drop()
    setup_database.create()
    setup_database.populate()


def setup_db_device():
    """Create the database for Device table testing.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_device = 1

    # Create a dict of all the expected values
    expected = {
        'devicename': general.hashstring(general.randomstring()),
        'description': general.hashstring(general.randomstring()),
        'ip_address': general.hashstring('100.100.100.100'),
        'idx_device': idx_device,
        'exists': True,
        'enabled': 1
    }

    # Drop the database and create tables
    initialize_db()

    # Insert data into database
    data = Device(
        description=general.encode(expected['description']),
        devicename=general.encode(expected['devicename']),
        ip_address=general.encode(expected['ip_address']),
        enabled=expected['enabled'])
    database = db.Database()
    database.add_all([data], 1019)

    # Return
    return expected


def setup_db_billcode():
    """Create the database for Billcode table testing.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_billcode = 1

    # Create a dict of all the expected values
    expected = {
        'enabled': True,
        'name': general.hashstring(general.randomstring()),
        'idx_billcode': idx_billcode,
        'code': general.hashstring(general.randomstring()),
        'enabled': 1
    }

    # Drop the database and create tables
    initialize_db()

    # Insert data into database
    data = Billcode(
        code=general.encode(expected['code']),
        name=general.encode(expected['name']))
    database = db.Database()
    database.add_all([data], 1018)

    # Return
    return expected


def setup_db_department():
    """Create the database for Department table testing.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_department = 1

    # Create a dict of all the expected values
    expected = {
        'enabled': True,
        'name': general.hashstring(general.randomstring()),
        'idx_department': idx_department,
        'code': general.hashstring(general.randomstring()),
        'enabled': 1
    }

    # Drop the database and create tables
    initialize_db()

    # Insert data into database
    data = Department(
        code=general.encode(expected['code']),
        name=general.encode(expected['name']))
    database = db.Database()
    database.add_all([data], 1018)

    # Return
    return expected
