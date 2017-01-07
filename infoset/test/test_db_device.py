#!/usr/bin/env python3
"""Test the db_device library in the infoset.db module."""

import unittest

# Import infoset stuff
from infoset.db import db_device
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestGetIDXDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_device_good = 1
    expected = unittest_setup_db.setup_db_device()

    # Create device object
    good_device = db_device.GetIDXDevice(idx_device_good)

    def test_init(self):
        """Testing method __init__."""
        # Test with non existent IDXDevice
        record = db_device.GetIDXDevice('bogus')
        self.assertEqual(record.exists(), False)

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

    def test_ip_address(self):
        """Testing function ip_address."""
        # Testing with known good value
        result = self.good_device.ip_address()
        self.assertEqual(result, self.expected['ip_address'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.ip_address()
        self.assertNotEqual(result, expected)

    def test_exists(self):
        """Testing function exists."""
        # Testing with known good value
        result = self.good_device.exists()
        self.assertEqual(result, True)


class TestGetDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_device_good = 1
    expected = unittest_setup_db.setup_db_device()

    # Create device object
    good_device = db_device.GetIDXDevice(idx_device_good)

    def test___init__(self):
        """Testing function __init__."""
        # Test with non existent DeviceIDX
        record = db_device.GetIDXDevice('bogus')
        self.assertEqual(record.exists(), False)

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

    def test_ip_address(self):
        """Testing function ip_address."""
        # Testing with known good value
        result = self.good_device.ip_address()
        self.assertEqual(result, self.expected['ip_address'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_device.ip_address()
        self.assertNotEqual(result, expected)


class TestFunctions(unittest.TestCase):
    """Checks all functions."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_device_good = 1
    expected = unittest_setup_db.setup_db_device()

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
        result = db_device.idx_device_exists(1)
        self.assertEqual(result, True)

        # Test known false value
        result = db_device.idx_device_exists(-1)
        self.assertEqual(result, False)

if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
