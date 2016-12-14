#!/usr/bin/env python3
"""Test the general module."""

import unittest

# Import infoset stuff
from infoset.db import db_device
from infoset.test import unittest_db


class TestGetIDXDevice(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_device_good = 1
    expected = unittest_db.setup_db_device()

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
    expected = unittest_db.setup_db_device()

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


class TestOther(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Intstantiate a good agent
    idx_device_good = 1
    good_device = db_device.GetIDXDevice(idx_device_good)

    def test_all_devices(self):
        """Testing function all_devices."""
        pass

    def test_devicename_exists(self):
        """Testing function devicename_exists."""
        pass

    def test_idx_exists(self):
        """Testing function idx_exists."""
        pass

if __name__ == '__main__':

    # Do the unit test
    unittest.main()
