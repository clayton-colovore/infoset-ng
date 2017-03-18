#!/usr/bin/env python3
"""Test the db_datapoint library in the infoset.db module."""

import unittest
import os
import sys

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

from infoset.db import db_datapoint
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestGetID(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['id_datapoint'] = database.id_datapoint()
    expected['last_timestamp'] = database.timestamp()
    expected['idx_deviceagent'] = database.idx_deviceagent()
    expected['idx_datapoint'] = database.idx_datapoint()
    expected['idx_department'] = database.idx_department()
    expected['idx_billcode'] = database.idx_billcode()
    expected['agent_label'] = database.agent_label()
    expected['agent_source'] = database.agent_source()
    expected['enabled'] = True
    expected['exists'] = True
    expected['billable'] = False
    expected['base_type'] = 1
    expected['timefixed_value'] = None

    # Retrieve data
    testing = db_datapoint.GetIDDatapoint(expected['id_datapoint'])

    def test___init__(self):
        """Testing function __init__."""
        # Test with non existent AgentIDX
        record = db_datapoint.GetIDDatapoint(-1)
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.enabled(), None)
        self.assertEqual(record.last_timestamp(), None)
        self.assertEqual(record.timefixed_value(), None)
        self.assertEqual(record.base_type(), None)
        self.assertEqual(record.billable(), None)
        self.assertEqual(record.agent_source(), None)
        self.assertEqual(record.idx_deviceagent(), None)
        self.assertEqual(record.id_datapoint(), None)
        self.assertEqual(record.idx_datapoint(), None)
        self.assertEqual(record.idx_department(), None)
        self.assertEqual(record.idx_billcode(), None)
        self.assertEqual(record.agent_label(), None)

    def test_exists(self):
        """Testing function exists."""
        # Testing with known good value
        result = self.testing.exists()
        self.assertEqual(result, self.expected['exists'])

    def test_everything(self):
        """Testing function everything."""
        # Testing with known good value
        result = self.testing.everything()
        for key, _ in result.items():
            self.assertEqual(result[key], self.expected[key])

        # Test the number and names of keys
        keys = [
            'idx_datapoint', 'id_datapoint', 'idx_deviceagent',
            'idx_department', 'idx_billcode', 'agent_label',
            'agent_source', 'enabled', 'billable', 'base_type',
            'timefixed_value', 'last_timestamp', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_last_timestamp(self):
        """Testing function last_timestamp."""
        # Testing with known good value
        result = self.testing.last_timestamp()
        self.assertEqual(result, self.expected['last_timestamp'])

    def test_timefixed_value(self):
        """Testing function timefixed_value."""
        # Testing with known good value
        result = self.testing.timefixed_value()
        self.assertEqual(result, self.expected['timefixed_value'])

    def test_base_type(self):
        """Testing function base_type."""
        # Testing with known good value
        result = self.testing.base_type()
        self.assertEqual(result, self.expected['base_type'])

    def test_enabled(self):
        """Testing function enabled."""
        # Testing with known good value
        result = self.testing.base_type()
        self.assertEqual(result, self.expected['enabled'])

    def test_billable(self):
        """Testing function billable."""
        # Testing with known good value
        result = self.testing.billable()
        self.assertEqual(result, self.expected['billable'])

    def test_agent_source(self):
        """Testing function agent_source."""
        # Testing with known good value
        result = self.testing.agent_source()
        self.assertEqual(result, self.expected['agent_source'])

    def test_idx_deviceagent(self):
        """Testing function idx_deviceagent."""
        # Testing with known good value
        result = self.testing.idx_deviceagent()
        self.assertEqual(result, self.expected['idx_deviceagent'])

    def test_id_datapoint(self):
        """Testing function id_datapoint."""
        # Testing with known good value
        result = self.testing.id_datapoint()
        self.assertEqual(result, self.expected['id_datapoint'])

    def test_idx_datapoint(self):
        """Testing function idx_datapoint."""
        # Testing with known good value
        result = self.testing.idx_datapoint()
        self.assertEqual(result, self.expected['idx_datapoint'])

    def test_idx_department(self):
        """Testing function idx_department."""
        # Testing with known good value
        result = self.testing.idx_department()
        self.assertEqual(result, self.expected['idx_department'])

    def test_idx_billcode(self):
        """Testing function idx_billcode."""
        # Testing with known good value
        result = self.testing.idx_billcode()
        self.assertEqual(result, self.expected['idx_billcode'])

    def test_agent_label(self):
        """Testing function agent_label."""
        # Testing with known good value
        result = self.testing.agent_label()
        self.assertEqual(result, self.expected['agent_label'])


class TestGetIDX(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['id_datapoint'] = database.id_datapoint()
    expected['last_timestamp'] = database.timestamp()
    expected['idx_deviceagent'] = database.idx_deviceagent()
    expected['idx_datapoint'] = database.idx_datapoint()
    expected['idx_department'] = database.idx_department()
    expected['idx_billcode'] = database.idx_billcode()
    expected['agent_label'] = database.agent_label()
    expected['agent_source'] = database.agent_source()
    expected['enabled'] = True
    expected['exists'] = True
    expected['billable'] = False
    expected['base_type'] = 1
    expected['timefixed_value'] = None

    # Retriev edata
    testing = db_datapoint.GetIDXDatapoint(expected['idx_datapoint'])

    def test___init__(self):
        """Testing function __init__."""
        # Test with non existent AgentIDX
        record = db_datapoint.GetIDXDatapoint(-1)
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.enabled(), None)
        self.assertEqual(record.last_timestamp(), None)
        self.assertEqual(record.timefixed_value(), None)
        self.assertEqual(record.base_type(), None)
        self.assertEqual(record.billable(), None)
        self.assertEqual(record.agent_source(), None)
        self.assertEqual(record.idx_deviceagent(), None)
        self.assertEqual(record.id_datapoint(), None)
        self.assertEqual(record.idx_datapoint(), None)
        self.assertEqual(record.idx_department(), None)
        self.assertEqual(record.idx_billcode(), None)
        self.assertEqual(record.agent_label(), None)

    def test_exists(self):
        """Testing function exists."""
        # Testing with known good value
        result = self.testing.exists()
        self.assertEqual(result, self.expected['exists'])

    def test_everything(self):
        """Testing function everything."""
        # Testing with known good value
        result = self.testing.everything()
        for key, _ in result.items():
            self.assertEqual(result[key], self.expected[key])

        # Test the number and names of keys
        keys = [
            'idx_datapoint', 'id_datapoint', 'idx_deviceagent',
            'idx_department', 'idx_billcode', 'agent_label',
            'agent_source', 'enabled', 'billable', 'base_type',
            'timefixed_value', 'last_timestamp', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_last_timestamp(self):
        """Testing function last_timestamp."""
        # Testing with known good value
        result = self.testing.last_timestamp()
        self.assertEqual(result, self.expected['last_timestamp'])

    def test_timefixed_value(self):
        """Testing function timefixed_value."""
        # Testing with known good value
        result = self.testing.timefixed_value()
        self.assertEqual(result, self.expected['timefixed_value'])

    def test_base_type(self):
        """Testing function base_type."""
        # Testing with known good value
        result = self.testing.base_type()
        self.assertEqual(result, self.expected['base_type'])

    def test_enabled(self):
        """Testing function enabled."""
        # Testing with known good value
        result = self.testing.base_type()
        self.assertEqual(result, self.expected['enabled'])

    def test_billable(self):
        """Testing function billable."""
        # Testing with known good value
        result = self.testing.billable()
        self.assertEqual(result, self.expected['billable'])

    def test_agent_source(self):
        """Testing function agent_source."""
        # Testing with known good value
        result = self.testing.agent_source()
        self.assertEqual(result, self.expected['agent_source'])

    def test_idx_deviceagent(self):
        """Testing function idx_deviceagent."""
        # Testing with known good value
        result = self.testing.idx_deviceagent()
        self.assertEqual(result, self.expected['idx_deviceagent'])

    def test_id_datapoint(self):
        """Testing function id_datapoint."""
        # Testing with known good value
        result = self.testing.id_datapoint()
        self.assertEqual(result, self.expected['id_datapoint'])

    def test_idx_datapoint(self):
        """Testing function idx_datapoint."""
        # Testing with known good value
        result = self.testing.idx_datapoint()
        self.assertEqual(result, self.expected['idx_datapoint'])

    def test_idx_department(self):
        """Testing function idx_department."""
        # Testing with known good value
        result = self.testing.idx_department()
        self.assertEqual(result, self.expected['idx_department'])

    def test_idx_billcode(self):
        """Testing function idx_billcode."""
        # Testing with known good value
        result = self.testing.idx_billcode()
        self.assertEqual(result, self.expected['idx_billcode'])

    def test_agent_label(self):
        """Testing function agent_label."""
        # Testing with known good value
        result = self.testing.agent_label()
        self.assertEqual(result, self.expected['agent_label'])


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['id_datapoint'] = database.id_datapoint()
    expected['last_timestamp'] = database.timestamp()
    expected['idx_deviceagent'] = database.idx_deviceagent()
    expected['idx_datapoint'] = database.idx_datapoint()
    expected['idx_department'] = database.idx_department()
    expected['idx_billcode'] = database.idx_billcode()
    expected['agent_label'] = database.agent_label()
    expected['agent_source'] = database.agent_source()
    expected['enabled'] = True
    expected['exists'] = True
    expected['billable'] = False
    expected['base_type'] = 1
    expected['timefixed_value'] = None

    def test_id_datapoint_exists(self):
        """Testing function id_datapoint_exists."""
        # Testing with known good value
        expected = True
        result = db_datapoint.id_datapoint_exists(
            self.expected['id_datapoint'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_datapoint.id_datapoint_exists('bogus')
        self.assertEqual(result, expected)

    def test_idx_datapoint_exists(self):
        """Testing function idx_datapoint_exists."""
        # Testing with known good value
        expected = True
        result = db_datapoint.idx_datapoint_exists(
            self.expected['idx_datapoint'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_datapoint.idx_datapoint_exists(None)
        self.assertEqual(result, expected)

    def test_listing(self):
        """Testing function listing."""
        # Testing with known good value
        results = db_datapoint.listing(self.expected['idx_deviceagent'])
        for result in results:
            for key, _ in result.items():
                self.assertEqual(result[key], self.expected[key])


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
