#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import unittest

from infoset.db import db_agent
from infoset.test import unittest_db


class TestGetIDX(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database
    (_, expected) = unittest_db.setup_db_agent()

    # Retrieve data
    good_agent = db_agent.GetIDXAgent(1)

    def test_init_getidx(self):
        """Testing method init."""
        # Test with non existent AgentIDX
        record = db_agent.GetIDXAgent(-1)
        self.assertEqual(record.exists(), False)

    def test_id_agent_getidx(self):
        """Testing method id_agent."""
        # Testing with known good value
        result = self.good_agent.id_agent()
        self.assertEqual(result, self.expected['id_agent'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.id_agent()
        self.assertNotEqual(result, expected)

    def test_name_getidx(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, True)

    def test_enabled_getidx(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)

    def test_everything_getidx(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_agent.everything()
        for key, _ in self.expected.items():
            self.assertEqual(result[key], self.expected[key])


class TestGetIdentifier(unittest.TestCase):
    """Checks all functions and methods."""

    # Setup database
    (good_id, expected) = unittest_db.setup_db_agent()

    # Retrieve data
    good_agent = db_agent.GetIDAgent(good_id)

    def test_init_getid_agent(self):
        """Testing method __init__."""
        # Test with non existent AgentID
        record = db_agent.GetIDAgent('bogus')
        self.assertEqual(record.exists(), False)

    def test_exists(self):
        """Testing method exists."""
        # Testing with known good value
        result = self.good_agent.exists()
        self.assertEqual(result, True)

    def test_idx_getidx_agent(self):
        """Testing method idx."""
        # Testing with known good value
        result = self.good_agent.idx_agent()
        self.assertEqual(result, self.expected['idx_agent'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.idx_agent()
        self.assertNotEqual(result, expected)

    def test_name_getid_agent(self):
        """Testing method name."""
        # Testing with known good value
        result = self.good_agent.name()
        self.assertEqual(result, self.expected['name'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.name()
        self.assertNotEqual(result, expected)

    def test_enabled_getid_agent(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_agent.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_agent.enabled()
        self.assertNotEqual(result, expected)

    def test_everything_getid_agent(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_agent.everything()
        for key, _ in self.expected.items():
            self.assertEqual(result[key], self.expected[key])


class Other(unittest.TestCase):
    """Checks all functions and methods."""

    # Intstantiate a good agent
    idx_agent_good = 1

    # Setup database
    (good_id, _) = unittest_db.setup_db_agent()

    # Retrieve data
    good_agent = db_agent.GetIDAgent(good_id)

    def test_id_agent_exists(self):
        """Testing function id_agent_exists."""
        # Testing with known good value
        expected = True
        result = db_agent.id_agent_exists(self.good_id)
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agent.id_agent_exists('bogus')
        self.assertEqual(result, expected)

    def test_idx_agent_exists(self):
        """Testing function idx_agent_exists."""
        # Testing with known good value
        expected = True
        result = db_agent.idx_agent_exists(self.idx_agent_good)
        self.assertEqual(result, expected)

        # Testing with known bad value
        expected = False
        result = db_agent.idx_agent_exists(None)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    # Test the configuration variables
    unittest_db.validate()

    # Do the unit test
    unittest.main()
