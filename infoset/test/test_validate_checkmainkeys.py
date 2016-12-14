#!/usr/bin/env python3
"""Test the general module."""

# Standard imports
import unittest
import copy

# Infoset imports
from infoset.cache import validate
from infoset.utils import general
from infoset.test import db_unittest


class TestCheckMainKeys(unittest.TestCase):
    """Checks all functions and methods."""
    # Initialize key variables
    devicename = general.hashstring(general.randomstring())
    id_agent = general.hashstring(general.randomstring())
    agent_name = general.hashstring(general.randomstring())
    timestamp = general.normalized_timestamp()

    # Test with good data
    data = {
        'id_agent': id_agent,
        'agent': agent_name,
        'devicename': devicename,
        'timestamp': timestamp
    }

    def test___init__(self):
        """Testing function __init__."""
        # Test with value that is not a dict
        result = validate._CheckMainKeys('string')
        self.assertEqual(result.valid(), False)

    def test__timestamp(self):
        """Testing function _timestamp."""
        # Initialize key variables
        test_dict = copy.deepcopy(self.data)

        # Test good data
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._timestamp(), True)

        # Test bad data (key is string)
        test_dict['timestamp'] = 'string'
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._timestamp(), False)

        # Test bad data (no key)
        test_dict.pop('timestamp', None)
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._timestamp(), False)

    def test__id_agent(self):
        """Testing function _id_agent."""
        # Initialize key variables
        test_dict = copy.deepcopy(self.data)

        # Test good data
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._id_agent(), True)

        # Test bad data (key is integer)
        test_dict['id_agent'] = 0
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._id_agent(), False)

        # Test bad data (no key)
        test_dict.pop('id_agent', None)
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._id_agent(), False)

    def test__agent(self):
        """Testing function _agent."""
        # Initialize key variables
        test_dict = copy.deepcopy(self.data)

        # Test good data
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._agent(), True)

        # Test bad data (key is integer)
        test_dict['agent'] = 0
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._agent(), False)

        # Test bad data (no key)
        test_dict.pop('agent', None)
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._agent(), False)

    def test__devicename(self):
        """Testing function _devicename."""
        # Initialize key variables
        test_dict = copy.deepcopy(self.data)

        # Test good data
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._devicename(), True)

        # Test bad data (key is integer)
        test_dict['devicename'] = 0
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._devicename(), False)

        # Test bad data (no key)
        test_dict.pop('devicename', None)
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result._devicename(), False)

    def test_valid(self):
        """Testing function valid."""
        # Initialize key variables
        test_dict = copy.deepcopy(self.data)

        # Test good data
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result.valid(), True)

        # Test bad data (key is integer)
        test_dict['devicename'] = 0
        result = validate._CheckMainKeys(test_dict)
        self.assertEqual(result.valid(), False)


if __name__ == '__main__':
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
