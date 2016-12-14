#!/usr/bin/env python3
"""Test the general module."""

# Standard imports
import unittest
import time
import copy

# Infoset imports
from infoset.cache import validate
from infoset.utils import general
from infoset.test import db_unittest


class TestCheckData(unittest.TestCase):
    """Checks all functions and methods."""
    # Initialize key variables
    data = {
        'agent': 'unittest',
        'timeseries': {'cpu_count': {'base_type': 1,
                                     'data': [[0, 2, None]],
                                     'description': 'CPU Count'},
                       'packets_recv': {'base_type': 64,
                                        'data': [['lo', 304495689, 'lo'],
                                                 ['p10p1', 84319802, 'p10p1']],
                                        'description': 'Packets (In)'},
                       'packets_sent': {'base_type': 64,
                                        'data': [['lo', 304495689, 'lo'],
                                                 ['p10p1',
                                                  123705549, 'p10p1']],
                                        'description': 'Packets (Out)'},
                       'swap_used': {'base_type': 1,
                                     'data': [[None, 363606016, None]],
                                     'description': 'Swap Used'}},
        'devicename': 'unittest_device',
        'id_agent': 'a0810e3e36c59ea3cbdab599dcdb824fb468314b7340543493271ad',
        'timefixed': {'distribution': {'base_type': None,
                                       'data': [[0,
                                                 'Ubuntu 16.04 xenial', None]],
                                       'description': 'Linux Distribution'},
                      'version': {'base_type': None,
                                  'data': [[0, '#62-Ubuntu SMP', None]],
                                  'description': 'Kernel Type'}},
        'timestamp': 1481561700}

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

        # Test with bad data (no data keys)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timefixed', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._data_keys_ok(), False)

        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timeseries', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._data_keys_ok(), False)

    def test__agent_label_keys_ok(self):
        """Testing function _agent_label_keys_ok."""
        # Test with good data
        data_dict = copy.deepcopy(self.data)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._agent_label_keys_ok(), True)

        # Test with bad data (no data keys)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timefixed', None)
        result = validate._CheckData(data_dict)
        self.assertEqual(result._agent_label_keys_ok(), False)

        data_dict = copy.deepcopy(self.data)
        data_dict.pop('timeseries', None)
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
        pass

    def test_valid(self):
        """Testing function valid."""
        pass


if __name__ == '__main__':
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
