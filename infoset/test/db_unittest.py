#!/usr/bin/env python3
"""Test the general module."""

# Standard imports

# PIP3 imports
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import create_database, drop_database

# Import infoset libraries
from infoset.utils import configuration
from infoset.utils import log
from infoset.utils import general
from infoset.db.db_orm import BASE, Agent, Device
from infoset.db import URL, TEST_ENGINE
from infoset.db import db


class TestDatabase(object):
    """Checks all functions and methods."""

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
    setup_database = TestDatabase()
    setup_database.drop()
    setup_database.create()
    setup_database.populate()

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
        'enabled': 1
    }

    # Drop the database and create tables
    setup_database = TestDatabase()
    setup_database.drop()
    setup_database.create()
    setup_database.populate()

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
