#!/usr/bin/env python3
"""Test the general module."""

# Standard imports
import unittest
import tempfile
import json
import copy

# Infoset imports
from infoset.cache import validate
from infoset.test import db_unittest
from infoset.utils import general


class TestValidateCache(unittest.TestCase):
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
        # Drop the database and create tables
        db_unittest.initialize_db()

        # Test with valid data
        result = validate.ValidateCache(data=self.data)
        self.assertEqual(result.valid(), True)

        # Test with invalid data (string)
        result = validate.ValidateCache(data='string')
        self.assertEqual(result.valid(), False)

        # Test with invalid data (string)
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('agent', None)
        result = validate.ValidateCache(data=data_dict)
        self.assertEqual(result.valid(), False)

        # Drop the database and create tables
        db_unittest.initialize_db()

        # Do the same with a file
        directory = tempfile.mkdtemp()
        timestamp = general.normalized_timestamp()
        filename = ('%s/%s_%s_%s.json') % (
            directory,
            timestamp,
            general.hashstring(general.randomstring()),
            general.hashstring(general.randomstring()))

        # Write good data to file and test
        with open(filename, 'w') as f_handle:
            json.dump(self.data, f_handle)
        result = validate.ValidateCache(filepath=filename)
        self.assertEqual(result.valid(), True)

        # Attempting to insert duplicate data should fail
        with open(filename, 'w') as f_handle:
            json.dump(self.data, f_handle)
        result = validate.ValidateCache(filepath=filename)
        self.assertEqual(result.valid(), False)

        # Drop the database and create tables
        db_unittest.initialize_db()

        # Write bad data to file and test
        data_dict = copy.deepcopy(self.data)
        data_dict.pop('agent', None)
        with open(filename, 'w') as f_handle:
            json.dump(data_dict, f_handle)
        result = validate.ValidateCache(filepath=filename)
        self.assertEqual(result.valid(), True)

        # Cleanup
        os.remove(filename)
        os.removedirs(directory)

    def test_getinfo(self):
        """Testing function getinfo."""
        # Drop the database and create tables
        db_unittest.initialize_db()

        # Test with valid data
        result = validate.ValidateCache(data=self.data)
        data_dict = result.getinfo()

        # Check main keys
        for key, _ in self.data.items():
            self.assertEqual(self.data[key], data_dict[key])

    def test_valid(self):
        """Testing function valid."""
        # Drop the database and create tables
        db_unittest.initialize_db()

        # Test with valid data
        result = validate.ValidateCache(data=self.data)
        self.assertEqual(result.valid(), True)

        # Test with invalid data (string)
        result = validate.ValidateCache(data='string')
        self.assertEqual(result.valid(), False)


if __name__ == '__main__':
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
