#!/usr/bin/env python3
"""This module sets up the database for specific unittests.

The TestDatabase class can create, drop a configured database. It can also
create empty tables for the database.

There are related functions for populating specific tables for unittests.

There are also functions for validating that the configured database
is a test database.

"""

# Standard imports
import random

# PIP3 imports
from sqlalchemy_utils.functions import database_exists
from sqlalchemy_utils.functions import create_database, drop_database
from sqlalchemy import and_

# Import infoset libraries
from infoset.test import unittest_setup
from infoset.utils import configuration
from infoset.utils import log
from infoset.utils import general
from infoset.db.db_orm import BASE, Agent, Device, DeviceAgent, Billcode, Data
from infoset.db.db_orm import Department, Datapoint, AgentName, Configuration
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
        # Setup database variables
        self.url = URL
        self.engine = TEST_ENGINE

        # Get configuration
        self.config = configuration.Config()

        # Validate the configuration
        unittest_setup.ready()

        # Validate the database
        self.validate()

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

    def create_tables(self):
        """Create tables."""
        # Apply schemas
        if database_exists(self.url) is True:
            BASE.metadata.create_all(self.engine)

    def validate(self):
        """Make sure we are using a test database."""
        # Only work on test databases
        if self.config.db_name().startswith('test_') is False:
            log_message = (
                'Test database not found in configuration. '
                'Try setting your "INFOSET_CONFIGDIR" environment '
                'variable to a directory with a test configuration')
            log.log2die(1017, log_message)


class TestData(object):
    """Populate the database with data for unittests."""

    def __init__(self):
        """Method initializing the class."""
        # Initialize key variables
        self.data = {}
        self.data['idx_datapoint'] = 1
        self.data['idx_agentname'] = 1
        self.data['idx_billcode'] = 1
        self.data['idx_device'] = 1
        self.data['idx_deviceagent'] = 1
        self.data['idx_department'] = 1
        self.data['timestamp'] = general.normalized_timestamp()
        self.data['last_timestamp'] = general.normalized_timestamp()
        self.data['devicename'] = general.hashstring(general.randomstring())
        self.data['id_agent'] = general.hashstring(general.randomstring())
        self.data['id_datapoint'] = general.hashstring(general.randomstring())
        self.data['devicename'] = general.hashstring(general.randomstring())
        self.data['device_description'] = general.hashstring(
            general.randomstring())
        self.data['agent'] = general.hashstring(general.randomstring())
        self.data['agent_source'] = general.hashstring(general.randomstring())
        self.data['agent_label'] = general.hashstring(general.randomstring())
        self.data['department_code'] = general.hashstring(
            general.randomstring())
        self.data['department_name'] = general.hashstring(
            general.randomstring())
        self.data['billcode_code'] = general.hashstring(
            general.randomstring())
        self.data['billcode_name'] = general.hashstring(
            general.randomstring())

        # Define data to Insert
        self.data['values'] = []
        for timestamp in _timestamps():
            value_dict = {
                'idx_datapoint': self.data['idx_datapoint'],
                'value': timestamp * (1 + random.uniform(0, 1)),
                'timestamp': timestamp}
            self.data['values'].append(value_dict)

        # Drop the database and create tables
        initialize_db()

        # Initialize agent variables
        agent_data = {}
        agent_data['devicename'] = self.data['devicename']
        agent_data['device_description'] = self.data['device_description']
        agent_data['id_agent'] = self.data['id_agent']
        agent_data['agent'] = self.data['agent']
        agent_data['timestamp'] = self.data['timestamp']
        (
            self.data['idx_device'],
            self.data['idx_agent']) = _setup_db_deviceagent(agent_data)

        # Get DeviceAgent index value
        deviceagent = hagent.GetDeviceAgent(
            self.data['idx_device'], self.data['idx_agent'])
        self.data['idx_deviceagent'] = deviceagent.idx_deviceagent()

        # Insert Department data into database
        dept_data = Department(
            name=self.data['department_name'].encode(),
            code=self.data['department_code'].encode()
        )
        database = db.Database()
        database.add_all([dept_data], 1035)

        # Insert Billcode data into database
        bill_data = Billcode(
            name=self.data['billcode_name'].encode(),
            code=self.data['billcode_code'].encode()
        )
        database = db.Database()
        database.add_all([bill_data], 1039)

        # Insert Datapoint data into database
        new_data = Datapoint(
            agent_source=self.data['agent_source'].encode(),
            agent_label=self.data['agent_label'].encode(),
            last_timestamp=self.data['last_timestamp'],
            idx_deviceagent=self.data['idx_deviceagent'],
            id_datapoint=self.data['id_datapoint'].encode())
        database = db.Database()
        database.add_all([new_data], 1072)

        # Insert timeseries data into database
        new_data_list = []
        for item in self.data['values']:
            new_data_list.append(
                Data(
                    idx_datapoint=item['idx_datapoint'],
                    timestamp=item['timestamp'],
                    value=item['value']))

        database = db.Database()
        database.add_all(new_data_list, 1072)

    def agent_label(self):
        """Return agent_label."""
        # Initialize key variables
        value = self.data['agent_label']
        return value

    def agent(self):
        """Return agent."""
        # Initialize key variables
        value = self.data['agent']
        return value

    def agent_source(self):
        """Return agent_source."""
        # Initialize key variables
        value = self.data['agent_source']
        return value

    def billcode_code(self):
        """Return billcode_code."""
        # Initialize key variables
        value = self.data['billcode_code']
        return value

    def billcode_name(self):
        """Return billcode_name."""
        # Initialize key variables
        value = self.data['billcode_name']
        return value

    def department_code(self):
        """Return department_code."""
        # Initialize key variables
        value = self.data['department_code']
        return value

    def department_name(self):
        """Return department_name."""
        # Initialize key variables
        value = self.data['department_name']
        return value

    def devicename(self):
        """Return devicename."""
        # Initialize key variables
        value = self.data['devicename']
        return value

    def device_description(self):
        """Return device_description."""
        # Initialize key variables
        value = self.data['device_description']
        return value

    def id_agent(self):
        """Return id_agent."""
        # Initialize key variables
        value = self.data['id_agent']
        return value

    def id_datapoint(self):
        """Return id_datapoint."""
        # Initialize key variables
        value = self.data['id_datapoint']
        return value

    def idx_agent(self):
        """Return idx_agent."""
        # Initialize key variables
        value = self.data['idx_agent']
        return value

    def idx_agentname(self):
        """Return idx_agentname."""
        # Initialize key variables
        value = self.data['idx_agentname']
        return value

    def idx_billcode(self):
        """Return idx_billcode."""
        # Initialize key variables
        value = self.data['idx_billcode']
        return value

    def idx_datapoint(self):
        """Return idx_datapoint."""
        # Initialize key variables
        value = self.data['idx_datapoint']
        return value

    def idx_department(self):
        """Return idx_department."""
        # Initialize key variables
        value = self.data['idx_department']
        return value

    def idx_device(self):
        """Return idx_device."""
        # Initialize key variables
        value = self.data['idx_device']
        return value

    def idx_deviceagent(self):
        """Return idx_deviceagent."""
        # Initialize key variables
        value = self.data['idx_deviceagent']
        return value

    def last_timestamp(self):
        """Return last_timestamp."""
        # Initialize key variables
        value = self.data['last_timestamp']
        return value

    def timestamp(self):
        """Return timestamp."""
        # Initialize key variables
        value = self.data['timestamp']
        return value

    def values(self):
        """Return values."""
        # Initialize key variables
        value = self.data['values']
        return value


def _setup_db_deviceagent(data):
    """Create the database for DeviceAgent table testing.

    Args:
        None

    Returns:
        result: Tuple of (idx_device, idx_agent)

    """
    # Initialize key variables
    devicename = data['devicename']
    description = data['device_description']
    id_agent = data['id_agent']
    agent = data['agent']
    last_timestamp = data['timestamp']

    # Add AgentName record to the database
    record = AgentName(
        name=general.encode(agent))
    database = db.Database()
    database.add(record, 1031)

    # Add Agent record to the database
    record = Agent(
        id_agent=general.encode(id_agent))
    database = db.Database()
    database.add(record, 1031)

    # Get idx_agent value from database
    agent_info = db_agent.GetIDAgent(id_agent)
    idx_agent = agent_info.idx_agent()

    # Add record to the database
    dev_record = Device(
        description=general.encode(description),
        devicename=general.encode(devicename))
    database = db.Database()
    database.add(dev_record, 1034)

    # Get idx of newly added device
    device_info = db_device.GetDevice(devicename)
    idx_device = device_info.idx_device()

    # Update DeviceAgent table
    if hagent.device_agent_exists(idx_device, idx_agent) is False:
        # Add to DeviceAgent table
        da_record = DeviceAgent(idx_device=idx_device, idx_agent=idx_agent)
        database = db.Database()
        database.add(da_record, 1020)

    # Update DeviceAgent table with timestamp
    database = db.Database()
    session = database.session()
    record = session.query(DeviceAgent).filter(
        and_(
            DeviceAgent.idx_device == idx_device,
            DeviceAgent.idx_agent == idx_agent)).one()
    record.last_timestamp = last_timestamp
    database.commit(session, 1042)

    # Return
    result = (idx_device, idx_agent)
    return result


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
    setup_database.create_tables()


def _timestamps():
    """Create a list of timestamps staring starting 30 minutes ago.

    Args:
        None

    Returns:
        timestamps: List of timestamps

    """
    # Initialize key variables
    timestamps = []
    config = configuration.Config()
    interval = config.interval()
    starting_timestamp = general.normalized_timestamp() - 1800
    timestamps = list(
        range(starting_timestamp, starting_timestamp - 1800, -interval))
    return timestamps


def setup_db_configuration():
    """Create the database for Configuration table testing.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_configuration = 1

    # Get Configuration
    config_key = general.hashstring('_INFOSET_TEST_')
    config_value = general.hashstring('_INFOSET_TEST_VALUE_')

    # Create a dict of all the expected values
    expected = {
        'config_key': config_key,
        'config_value': config_value,
        'idx_configuration': idx_configuration,
        'enabled': 1
    }

    # Drop the database and create tables
    initialize_db()

    # Insert data into database
    data = Configuration(
        config_key=general.encode(expected['config_key']),
        config_value=general.encode(expected['config_value']),
        enabled=expected['enabled'])
    database = db.Database()
    database.add_all([data], 1045)

    # Return
    return expected


def setup_db_IDXConfiguration():
    """Create the database for Configuration table testing.

    Args:
        None

    Returns:
        None

    """
    # Initialize key variables
    idx_configuration = 1

    # Get Configuration
    config_key = general.hashstring('_INFOSET_TEST_')
    config_value = general.hashstring('_INFOSET_TEST_VALUE_')

    # Create a dict of all the expected values
    expected = {
        'config_key': config_key,
        'config_value': config_value,
        'idx_configuration': idx_configuration,
        'enabled': 1,
        'exists': True
    }

    # Drop the database and create tables
    initialize_db()

    # Insert data into database
    data = Configuration(
        config_key=general.encode(expected['config_key']),
        config_value=general.encode(expected['config_value']),
        enabled=expected['enabled'])
    database = db.Database()
    database.add_all([data], 1045)

    # Return
    return expected
