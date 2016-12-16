#!/usr/bin/env python3
"""Test the CheckDuplicates class in the infoset.cache.validate module."""

# Standard imports
import unittest

# PIP libraries
from sqlalchemy import and_

# Infoset imports
from infoset.cache import validate
from infoset.utils import general
from infoset.db import db_device
from infoset.db import db
from infoset.db import db_deviceagent as hagent
from infoset.db import db_agent
from infoset.db.db_orm import Agent, Device, DeviceAgent
from infoset.test import unittest_db
from infoset.test import unittest_variables


class TestCheckDuplicates(unittest.TestCase):
    """Checks all functions and methods."""
    # Initialize key variables
    data = unittest_variables.TestVariables().cache_data()

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
        agent_name = self.data['agent']
        last_timestamp = self.data['timestamp']

        # Drop the database and create tables
        unittest_db.initialize_db()

        # Add record to the database
        record = Agent(
            id_agent=general.encode(id_agent),
            name=general.encode(agent_name))
        database = db.Database()
        database.add(record, 1081)

        # Test must be good as DeviceAgent last_timestamp not updated
        result = validate._CheckDuplicates(self.data)
        self.assertEqual(result.valid(), True)

        # Get idx_agent value from database
        data = db_agent.GetIDAgent(id_agent)
        idx_agent = data.idx_agent()

        # Add record to the database
        record = Device(devicename=general.encode(devicename))
        database = db.Database()
        database.add(record, 1080)

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
            database.add(record, 1038)

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
        database.commit(session, 1124)

        # Test must fail as DeviceAgent last_timestamp not updated
        result = validate._CheckDuplicates(self.data)
        self.assertEqual(result.valid(), False)


if __name__ == '__main__':
    # Test the configuration variables
    unittest_db.validate()

    # Do the unit test
    unittest.main()
