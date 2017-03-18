#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

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

from infoset.db import db_agent
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
    expected['idx_agent'] = database.idx_agent()
    expected['idx_agentname'] = database.idx_agentname()
    expected['id_agent'] = database.id_agent()
    expected['agent'] = database.agent()
    expected['enabled'] = True
    expected['exists'] = True

    # Retrieve data
    good_agent = db_agent.GetIDXAgent(expected['idx_agent'])

    def test_init(self):
        """Testing method init."""
        # Test with non existent AgentIDX
        record = db_agent.GetIDXAgent(-1)
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.enabled(), None)
        self.assertEqual(record.idx_agent(), None)
        self.assertEqual(record.agent(), None)
        self.assertEqual(record.idx_agentname(), None)

    def test_id_agent(self):
        """Testing method id_agent."""
        # Testing with known good value
        result = self.good_agent.id_agent()
        self.assertEqual(result, self.expected['id_agent'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.id_agent()
        self.assertNotEqual(result, expected)

    def test_idx_agent(self):
        """Testing method idx."""
        # Testing with known good value
        result = self.good_agent.idx_agent()
        self.assertEqual(result, self.expected['idx_agent'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx_agent()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, True)

    def test_idx_agentname(self):
        """Testing method idx_agentname."""
        # Testing with known good value
        result = self.good_agent.idx_agentname()
        self.assertEqual(result, self.expected['idx_agentname'])

    def test_agent(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.agent()
        self.assertEqual(result, self.expected['agent'])

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
        keys = [
            'idx_agent', 'idx_agentname', 'id_agent',
            'enabled', 'agent', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


class TestGetIdentifier(unittest.TestCase):
    """Checks all functions and methods."""

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_agent'] = database.idx_agent()
    expected['id_agent'] = database.id_agent()
    expected['idx_agentname'] = database.idx_agentname()
    expected['agent'] = database.agent()
    expected['enabled'] = True
    expected['exists'] = True

    # Retrieve data
    good_agent = db_agent.GetIDAgent(expected['id_agent'])

    def test_init(self):
        """Testing method __init__."""
        # Test with non existent AgentID
        record = db_agent.GetIDAgent('bogus')
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.enabled(), None)
        self.assertEqual(record.idx_agent(), None)
        self.assertEqual(record.agent(), None)
        self.assertEqual(record.idx_agentname(), None)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, True)

    def test_idx_agentname(self):
        """Testing method idx_agentname."""
        # Testing with known good value
        result = self.good_agent.idx_agentname()
        self.assertEqual(result, self.expected['idx_agentname'])

    def test_idx_agent(self):
        """Testing method idx."""
        # Testing with known good value
        result = self.good_agent.idx_agent()
        self.assertEqual(result, self.expected['idx_agent'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx_agent()
        self.assertNotEqual(result, expected)

    def test_agent(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.agent()
        self.assertEqual(result, self.expected['agent'])

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
        keys = [
            'idx_agent', 'idx_agentname', 'id_agent',
            'enabled', 'agent', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


class Other(unittest.TestCase):
    """Checks all functions and methods."""

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_agent'] = database.idx_agent()
    expected['idx_agentname'] = database.idx_agentname()
    expected['id_agent'] = database.id_agent()
    expected['enabled'] = True
    expected['exists'] = True

    # Retrieve data
    good_agent = db_agent.GetIDXAgent(expected['idx_agent'])

    def test_id_agent_exists(self):
        """Testing function id_agent_exists."""
        # Testing with known good value
        expected = True
        result = db_agent.id_agent_exists(self.expected['id_agent'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agent.id_agent_exists('bogus')
        self.assertEqual(result, expected)

    def test_idx_agent_exists(self):
        """Testing function idx_agent_exists."""
        # Testing with known good value
        expected = True
        result = db_agent.idx_agent_exists(self.expected['idx_agent'])
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agent.idx_agent_exists(None)
        self.assertEqual(result, expected)

    def test_get_all_agents(self):
        """Testing function get_all_agents."""
        # Testing with known good value
        result = db_agent.get_all_agents()
        self.assertEqual(isinstance(result, list), True)
        self.assertEqual(result[0]['idx_agent'], self.expected['idx_agent'])
        self.assertEqual(result[0]['exists'], self.expected['exists'])
        self.assertEqual(result[0]['enabled'], self.expected['enabled'])
        self.assertEqual(
            result[0]['idx_agentname'], self.expected['idx_agentname'])


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
