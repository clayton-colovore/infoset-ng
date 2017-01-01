#!/usr/bin/env python3
"""Test the CheckData class in the infoset.cache.validate module."""

# Standard imports
import unittest
import copy

# Infoset imports
from infoset.cache import validate
from infoset.test import unittest_db
from infoset.test import unittest_variables


class TestCheckData(unittest.TestCase):
    """Checks all functions and methods."""
    # Initialize key variables
    data = unittest_variables.TestVariables().cache_data()

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
    # Test the configuration variables
    unittest_db.validate()

    # Do the unit test
    unittest.main()
