#!/usr/bin/env python3
""" Module of infoset testing database functions."""

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

# Infoset libraries
from infoset.db import db_configuration
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup
from infoset.utils import general
from infoset.db import db
from infoset.db.db_orm import Configuration


class TestGetConfigurationKey(unittest.TestCase):

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    expected = unittest_setup_db.setup_db_configuration()

    # Retrieve data
    good_config = db_configuration.GetConfigurationKey(expected['config_key'])

    def test_init_get_configuration_key(self):
        """Testing method init."""
        record = db_configuration.GetConfigurationKey(-1)
        self.assertEqual(record.exists(), False)

    def test_idx_configuration_getkey(self):
        """Testing method idx_configuration."""
        # Testing with known good value
        result = self.good_config.idx_configuration()
        self.assertEqual(result, self.expected['idx_configuration'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_config.idx_configuration()
        self.assertNotEqual(result, expected)

    def test_config_key(self):
        """Testing method config_key."""
        # Testing with known good value
        result = self.good_config.config_key()
        self.assertEqual(result, self.expected['config_key'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_config.config_key()
        self.assertNotEqual(result, expected)

    def test_config_value(self):
        """Testing method config_value."""
        # Testing with known good value
        result = self.good_config.config_value()
        self.assertEqual(result, self.expected['config_value'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_config.config_value()
        self.assertNotEqual(result, expected)

    def test_enabled(self):
        """Testing method enabled."""
        # Testing with known good value
        result = self.good_config.enabled()
        self.assertEqual(result, self.expected['enabled'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_config.enabled()
        self.assertNotEqual(result, expected)


class TestGetIDXConfiguration(unittest.TestCase):

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    expected = unittest_setup_db.setup_db_IDXConfiguration()

    # Retrieve data
    good_config = db_configuration.GetIDXConfiguration(
        expected['idx_configuration'])

    def test_init_get_configuration_key(self):
        """Testing method init."""
        record = db_configuration.GetIDXConfiguration(-1)
        self.assertEqual(record.exists(), False)

    def test_config_key(self):
        """Testing method config_key."""
        # Testing with known good value
        result = self.good_config.config_key()
        self.assertEqual(result, self.expected['config_key'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_config.config_key()
        self.assertNotEqual(result, expected)

    def test_config_value(self):
        """Testing method config_value."""
        # Testing with known good value
        result = self.good_config.config_value()
        self.assertEqual(result, self.expected['config_value'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_config.config_value()
        self.assertNotEqual(result, expected)

    def test_config_key_exists(self):
        """Testing method config_value."""
        # Testing with known good value
        result = self.good_config.exists()
        self.assertEqual(result, self.expected['exists'])

        # Testing with known bad value
        expected = ('bogus')
        result = self.good_config.exists()
        self.assertNotEqual(result, expected)

if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
