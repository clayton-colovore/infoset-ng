#!/usr/bin/env python3
"""Test the db_multitable library in the infoset.db module."""

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

from infoset.db import db_multitable
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_datapoint'] = database.idx_datapoint()
    expected['id_agent'] = database.id_agent()
    expected['devicename'] = database.devicename()
    expected['agent_label'] = database.agent_label()
    expected['agent_source'] = database.agent_source()
    expected['agent'] = database.agent()
    expected['idx_deviceagent'] = database.idx_deviceagent()

    def test_datapoint_summary_list(self):
        """Testing function datapoint_summary_list."""
        # Start testing
        results = db_multitable.datapoint_summary_list()
        for data_dict in results:
            for key, _ in data_dict.items():
                self.assertEqual(data_dict[key], self.expected[key])

    def test_datapoint_summary(self):
        """Testing function datapoint_summary."""
        # Start testing
        result = db_multitable.datapoint_summary()
        for idx_datapoint, _ in result.items():
            data_dict = result[idx_datapoint]
            for key, _ in data_dict.items():
                self.assertEqual(data_dict[key], self.expected[key])

    def test__datapoint_summary(self):
        """Testing function _datapoint_summary."""
        # Tested by test_datapoint_summary and test_datapoint_summary_list
        pass


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
