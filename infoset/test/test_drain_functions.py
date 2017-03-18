#!/usr/bin/env python3
"""Test the functions in the infoset.cache.validate module."""

# Standard imports
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

# Infoset imports
from infoset.cache import drain
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    # Initialize key variables
    setup = unittest_setup.TestVariables()
    data = setup.cache_data()

    def test__id_datapoint(self):
        """Testing function _id_datapoint."""
        # Initialize key variables
        id_agent = 'id_agent'
        label = 'label'
        index = 'index'
        agent_name = 'agent_name'
        devicename = 'devicename'

        # Test
        result = drain._id_datapoint(
            id_agent, label, index, agent_name, devicename)
        self.assertEqual(
            result,
            '9af342e9f23a5e2ff09d8a799a2b9f5234b'
            'addc31f3c09b309be9dfe6801ee40')

    def test__main_keys(self):
        """Testing function _main_keys."""
        # Initialize key variables
        agent_meta_keys = [
            'timestamp', 'id_agent', 'agent', 'devicename']

        # Test
        result = drain._main_keys(self.data)
        for key in agent_meta_keys:
            self.assertEqual(result[key], self.data[key])

    def test__base_type(self):
        """Testing function _base_type."""
        # Initialize key variables
        base_types = [1, 32, 64]

        # Test
        for base_type in base_types:
            # Test with know values
            result = drain._base_type(base_type)
            self.assertEqual(result, base_type)

            result = drain._base_type(str(base_type))
            self.assertEqual(result, None)


if __name__ == '__main__':
    # Test the configuration variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
