#!/usr/bin/env python3
"""Test the CheckDuplicates class in the infoset.cache.validate module."""

# Standard imports
import unittest
import os
import sys

# PIP libraries
from sqlalchemy import and_

# Try to create a working PYTHONPATH
_test_directory = os.path.dirname(os.path.realpath(__file__))
_lib_directory = os.path.abspath(os.path.join(_test_directory, os.pardir))
_root_directory = os.path.abspath(os.path.join(_lib_directory, os.pardir))
if _test_directory.endswith('/infoset-ng/infoset/test') is True:
    sys.path.append(_root_directory)
else:
    print(
        'This script is not installed in the "infoset-ng/bin" directory. '
        'Please fix.')
    sys.exit(2)

# Infoset imports
from infoset.cache import validate
from infoset.utils import general
from infoset.db import db_device
from infoset.db import db
from infoset.db import db_deviceagent as hagent
from infoset.db import db_agent
from infoset.db.db_orm import Agent, Device, DeviceAgent
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestCheckDuplicates(unittest.TestCase):
    """Checks all functions and methods."""
    # Initialize key variables
    data = unittest_setup.TestVariables().cache_data()

    def test___init__(self):
        """Testing function __init__."""
        # Test with value that is not a dict
        result = validate._CheckDuplicates('string')
        self.assertEqual(result.valid(), False)

    def test_valid(self):
        """Testing function valid."""
        # Initialize key variables
        devicename = self.data['devicename']
        id_agent = self.data['id_agent']
        last_timestamp = self.data['timestamp']

        # Drop the database and create tables
        unittest_setup_db.TestData()

        # Add record to the database
        record = Agent(
            id_agent=general.encode(id_agent))
        database = db.Database()
        database.add(record, 1040)

        # Test must be good as DeviceAgent last_timestamp not updated
        result = validate._CheckDuplicates(self.data)
        self.assertEqual(result.valid(), True)

        # Get idx_agent value from database
        data = db_agent.GetIDAgent(id_agent)
        idx_agent = data.idx_agent()

        # Add record to the database
        record = Device(devicename=general.encode(devicename))
        database = db.Database()
        database.add(record, 1024)

        # Test must be good as DeviceAgent last_timestamp not updated
        result = validate._CheckDuplicates(self.data)
        self.assertEqual(result.valid(), True)

        # Get idx of newly added device
        device_info = db_device.GetDevice(devicename)
        idx_device = device_info.idx_device()

        # Update DeviceAgent table
        if hagent.device_agent_exists(idx_device, idx_agent) is False:
            # Add to DeviceAgent table
            record = DeviceAgent(idx_device=idx_device, idx_agent=idx_agent)
            database = db.Database()
            database.add(record, 1055)

        # Test must be good as DeviceAgent last_timestamp not updated
        result = validate._CheckDuplicates(self.data)
        self.assertEqual(result.valid(), True)

        # Update database with timestamp
        database = db.Database()
        session = database.session()
        record = session.query(DeviceAgent).filter(
            and_(
                DeviceAgent.idx_device == idx_device,
                DeviceAgent.idx_agent == idx_agent)).one()
        record.last_timestamp = last_timestamp
        database.commit(session, 1044)

        # Test must fail as DeviceAgent last_timestamp not updated
        result = validate._CheckDuplicates(self.data)
        self.assertEqual(result.valid(), False)


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
