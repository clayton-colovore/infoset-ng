#!/usr/bin/env python3
"""Test the db_device library in the infoset.db module."""

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

# Import infoset stuff
from infoset.db import db_device
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestGetIDXDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_device'] = database.idx_device()
    expected['devicename'] = database.devicename()
    expected['description'] = database.device_description()
    expected['enabled'] = True
    expected['exists'] = True

    # Create device object
    good_device = db_device.GetIDXDevice(expected['idx_device'])

    def test_init(self):
        """Testing method __init__."""
        # Test with non existent IDXDevice
        record = db_device.GetIDXDevice('bogus')
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.devicename(), None)
        self.assertEqual(record.enabled(), None)
        self.assertEqual(record.description(), None)
        self.assertEqual(record.idx_device(), None)

    def test_devicename(self):
        """Testing method devicename."""
        # Testing with known good value
        result = self.good_device.devicename()
        self.assertEqual(result, self.expected['devicename'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.devicename()
        self.assertNotEqual(result, expected)

    def test_description(self):
        """Testing function description."""
        # Testing with known good value
        result = self.good_device.description()
        self.assertEqual(result, self.expected['description'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.description()
        self.assertNotEqual(result, expected)

    def test_enabled(self):
        """Testing function enabled."""
        # Testing with known good value
        result = self.good_device.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.enabled()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing function exists."""
        # Testing with known good value
        result = self.good_device.exists()
        self.assertEqual(result, True)

    def test_everything(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_device.everything()
        for key, _ in self.expected.items():
            self.assertEqual(result[key], self.expected[key])

        # Test the number and names of keys
        keys = ['idx_device', 'devicename', 'description', 'enabled', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


class TestGetDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_device'] = database.idx_device()
    expected['devicename'] = database.devicename()
    expected['description'] = database.device_description()
    expected['enabled'] = True
    expected['exists'] = True

    # Create device object
    good_device = db_device.GetDevice(expected['devicename'])

    def test___init__(self):
        """Testing function __init__."""
        # Test with non existent DeviceIDX
        record = db_device.GetDevice('bogus')
        self.assertEqual(record.exists(), False)
        self.assertEqual(record.devicename(), None)
        self.assertEqual(record.enabled(), None)
        self.assertEqual(record.description(), None)
        self.assertEqual(record.idx_device(), None)

    def test_idx_device(self):
        """Testing method idx_device."""
        # Testing with known good value
        result = self.good_device.idx_device()
        self.assertEqual(result, self.expected['idx_device'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.devicename()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing function exists."""
        # Testing with known good value
        result = self.good_device.exists()
        self.assertEqual(result, True)

    def test_description(self):
        """Testing function description."""
        # Testing with known good value
        result = self.good_device.description()
        self.assertEqual(result, self.expected['description'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.description()
        self.assertNotEqual(result, expected)

    def test_enabled(self):
        """Testing function enabled."""
        # Testing with known good value
        result = self.good_device.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.enabled()
        self.assertNotEqual(result, expected)

    def test_everything(self):
        """Testing method everything."""
        # Testing with known good value
        result = self.good_device.everything()
        for key, _ in self.expected.items():
            self.assertEqual(result[key], self.expected[key])

        # Test the number and names of keys
        keys = ['idx_device', 'devicename', 'description', 'enabled', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


class TestFunctions(unittest.TestCase):
    """Checks all functions."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['idx_device'] = database.idx_device()
    expected['devicename'] = database.devicename()
    expected['description'] = database.device_description()
    expected['enabled'] = True
    expected['exists'] = True

    def test_all_devices(self):
        """Testing function all_devices."""
        # Test known working value
        results = db_device.all_devices()
        for result in results:
            for key, _ in result.items():
                self.assertEqual(result[key], self.expected[key])

    def test_devicename_exists(self):
        """Testing function devicename_exists."""
        # Test known working value
        result = db_device.devicename_exists(self.expected['devicename'])
        self.assertEqual(result, True)

        # Test known false value
        result = db_device.devicename_exists(False)
        self.assertEqual(result, False)

    def test_idx_device_exists(self):
        """Testing function idx_exists."""
        # Test known working value
        result = db_device.idx_device_exists(self.expected['idx_device'])
        self.assertEqual(result, True)

        # Test known false value
        result = db_device.idx_device_exists(-1)
        self.assertEqual(result, False)


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
