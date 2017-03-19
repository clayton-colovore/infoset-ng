#!/usr/bin/env python3
"""Test the CheckData class in the infoset.cache.validate module."""

# Standard imports
import unittest
import copy
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

# Infoset imports
from infoset.cache import validate
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestCheckData(unittest.TestCase):
    """Checks all functions and methods."""
    # Initialize key variables
    data = unittest_setup.TestVariables().cache_data()

    def test___init__(self):
        """Testing function __init__."""
        # Test with value that is not a dict
        result = validate._CheckData('string')
        self.assertEqual(result.valid(), False)

    def test__data_keys_ok(self):
        """Testing function _data_keys_ok."""
        # Test with good data
        data_dict = copy.deepcopy(self.data)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._data_keys_ok(), True)

        # Test with good data (missing one time keys)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timefixed', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._data_keys_ok(), True)

        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timeseries', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._data_keys_ok(), True)

        # Test with bad data (no time keys)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timefixed', None)
        data_dict.pop('timeseries', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._data_keys_ok(), False)

    def test__agent_label_keys_ok(self):
        """Testing function _agent_label_keys_ok."""
        # Test with good data
        data_dict = copy.deepcopy(self.data)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._agent_label_keys_ok(), True)

        # Test with good data (missing one time keys)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timefixed', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._agent_label_keys_ok(), True)

        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timeseries', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._agent_label_keys_ok(), True)

        # Test with bad data (missing all time keys)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timeseries', None)
        data_dict.pop('timefixed', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._agent_label_keys_ok(), False)

        # Test with bad data (no keys under agent_label)
        data_dict = copy.deepcopy(self.data)
        for _, sub_dict in data_dict['timeseries'].items():
            sub_dict.pop('base_type', None)
            result = validate._CheckData(sub_dict)
            self.assertEqual(result._agent_label_keys_ok(), False)

        data_dict = copy.deepcopy(self.data)
        for _, sub_dict in data_dict['timeseries'].items():
            sub_dict.pop('description', None)
            result = validate._CheckData(sub_dict)
            self.assertEqual(result._agent_label_keys_ok(), False)

        data_dict = copy.deepcopy(self.data)
        for _, sub_dict in data_dict['timeseries'].items():
            sub_dict.pop('data', None)
            result = validate._CheckData(sub_dict)
            self.assertEqual(result._agent_label_keys_ok(), False)

        # Test with bad data (not enough keys under 'data')
        data_dict = copy.deepcopy(self.data)
        for agent_label, _ in data_dict['timeseries'].items():
            data_dict['timeseries'][agent_label]['data'][0].remove(
                data_dict['timeseries'][agent_label]['data'][0][-1])
            break
        result = validate._CheckData(sub_dict)
        self.assertEqual(result._agent_label_keys_ok(), False)

    def test__timeseries_data_ok(self):
        """Testing function _timeseries_data_ok."""
        # Test with good data
        data_dict = copy.deepcopy(self.data)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._timeseries_data_ok(), True)

        # Test with bad data (base_type is non-numeric string)
        data_dict = copy.deepcopy(self.data)
        for agent_label, _ in data_dict['timeseries'].items():
            data_dict['timeseries'][agent_label]['base_type'] = 'string'
            break
        result = validate._CheckData(data_dict)
        self.assertEqual(result._timeseries_data_ok(), False)

        # Test with bad data ('data' value is non numeric)
        data_dict = copy.deepcopy(self.data)
        for agent_label, _ in data_dict['timeseries'].items():
            data_dict['timeseries'][agent_label]['data'][0][1] = 'string'
            break
        result = validate._CheckData(data_dict)
        self.assertEqual(result._timeseries_data_ok(), False)

        # Test with good data (missing one time keys)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timeseries', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._timeseries_data_ok(), True)

        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timefixed', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._timeseries_data_ok(), True)

        # Test with bad data (no timeseries key)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timeseries', None)
        data_dict.pop('timefixed', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._timeseries_data_ok(), False)

        # Test with bad data (no keys under agent_label)
        data_dict = copy.deepcopy(self.data)
        for _, sub_dict in data_dict['timeseries'].items():
            sub_dict.pop('base_type', None)
            result = validate._CheckData(sub_dict)
            self.assertEqual(result._timeseries_data_ok(), False)

        data_dict = copy.deepcopy(self.data)
        for _, sub_dict in data_dict['timeseries'].items():
            sub_dict.pop('data', None)
            result = validate._CheckData(sub_dict)
            self.assertEqual(result._timeseries_data_ok(), False)

    def test_valid(self):
        """Testing function valid."""
        # Test with good data
        data_dict = copy.deepcopy(self.data)
        result = validate._CheckData(data_dict)
        self.assertEqual(result.valid(), True)

        # Test with bad data (base_type is non-numeric string)
        data_dict = copy.deepcopy(self.data)
        for agent_label, _ in data_dict['timeseries'].items():
            data_dict['timeseries'][agent_label]['base_type'] = 'string'
            break
        result = validate._CheckData(data_dict)
        self.assertEqual(result.valid(), False)


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
