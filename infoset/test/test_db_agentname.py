#!/usr/bin/env python3
"""Test the db_agentname library in the infoset.db module."""

import unittest
import os
import sys

# Try to create a working PYTHONPATH
_TEST_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
_LIB_DIRECTORY = os.path.abspath(os.path.join(_TEST_DIRECTORY, os.pardir))
_ROOT_DIRECTORY = os.path.abspath(os.path.join(_LIB_DIRECTORY, os.pardir))
if _TEST_DIRECTORY.endswith('/infoset-ng/infoset/test') is True:
    sys.path.append(_ROOT_DIRECTORY)
else:
    print(
        'This script is not installed in the "infoset-ng/bin" directory. '
        'Please fix.')
    sys.exit(2)

from infoset.db import db_agentname
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestGetIDX(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_agentname'] = database.idx_agentname()
    expected['name'] = database.agent()
    expected['enabled'] = True
    expected['exists'] = True

    # Retrieve data
    good_agent = db_agentname.GetIDXAgentName(expected['idx_agentname'])

    def test_init(self):
        """Testing method init."""
        # Test with non existent AgentNameIDX
        record = db_agentname.GetIDXAgentName(-1)
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.name(), None)
        self.assertEqual(record.idx_agentname(), None)
        self.assertEqual(record.enabled(), None)

    def test_name(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_idx_agentname(self):
        """Testing method idx."""
        # Testing with known good value
        result = self.good_agent.idx_agentname()
        self.assertEqual(result, self.expected['idx_agentname'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx_agentname()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, self.expected['exists'])

    def test_enabled(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)

    def test_everything(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_agent.everything()
        for key, _ in self.expected.items():
            self.assertEqual(result[key], self.expected[key])

        # Test the number and names of keys
        keys = ['idx_agentname', 'name', 'enabled', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


class TestGetIdentifier(unittest.TestCase):
    """Checks all functions and methods."""

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_agentname'] = database.idx_agentname()
    expected['name'] = database.agent()
    expected['enabled'] = True
    expected['exists'] = True

    # Retrieve data
    good_agent = db_agentname.GetAgentName(expected['name'])

    def test_init(self):
        """Testing method __init__."""
        # Test with non existent AgentNameID
        record = db_agentname.GetAgentName('bogus')
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.name(), None)
        self.assertEqual(record.idx_agentname(), None)
        self.assertEqual(record.enabled(), None)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, True)

    def test_name(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_idx_agentname(self):
        """Testing method idx."""
        # Testing with known good value
        result = self.good_agent.idx_agentname()
        self.assertEqual(result, self.expected['idx_agentname'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx_agentname()
        self.assertNotEqual(result, expected)

    def test_enabled(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)

    def test_everything(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_agent.everything()
        for key, _ in self.expected.items():
            self.assertEqual(result[key], self.expected[key])

        # Test the number and names of keys
        keys = ['idx_agentname', 'name', 'enabled', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


class Other(unittest.TestCase):
    """Checks all functions and methods."""

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_agentname'] = database.idx_agentname()
    expected['name'] = database.agent()
    expected['enabled'] = True
    expected['exists'] = True

    # Retrieve data
    good_agent = db_agentname.GetAgentName(expected['name'])

    def test_name_exists(self):
        """Testing function name_exists."""
        # Testing with known good value
        expected = True
        result = db_agentname.name_exists(self.expected['name'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agentname.name_exists('bogus')
        self.assertEqual(result, expected)

    def test_idx_agentname_exists(self):
        """Testing function idx_agentname_exists."""
        # Testing with known good value
        expected = True
        result = db_agentname.idx_agentname_exists(
            self.expected['idx_agentname'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agentname.idx_agentname_exists(None)
        self.assertEqual(result, expected)

    def test_get_all_names(self):
        """Testing function get_all_names."""
        # Testing with known good value
        result = db_agentname.get_all_names()
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(result[0]['name'], self.expected['name'])
        self.assertEqual(result[0]['exists'], self.expected['exists'])
        self.assertEqual(result[0]['enabled'], self.expected['enabled'])
        self.assertEqual(
            result[0]['idx_agentname'], self.expected['idx_agentname'])


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
