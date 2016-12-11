#!/usr/bin/env python3
"""Test the general module."""

# Standard imports
import unittest
from mock import Mock

# Infoset imports
from infoset.utils import configuration
from infoset.utils import log
from infoset.test import db_unittest


class TestValidateCache(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_getinfo(self):
        """Testing function getinfo."""
        database = db_unittest.TestDatabase()

    def test_valid(self):
        """Testing function valid."""
        pass


class TestCheckDuplicates(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_valid(self):
        """Testing function valid."""
        pass


class TestCheckData(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test__data_keys_ok(self):
        """Testing function _data_keys_ok."""
        pass

    def test__agent_label_keys_ok(self):
        """Testing function _agent_label_keys_ok."""
        pass

    def test__charable_data_ok(self):
        """Testing function _charable_data_ok."""
        pass

    def test_valid(self):
        """Testing function valid."""
        pass


class TestCheckMainKeys(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test__timestamp(self):
        """Testing function _timestamp."""
        pass

    def test__id_agent(self):
        """Testing function _id_agent."""
        pass

    def test__agent(self):
        """Testing function _agent."""
        pass

    def test__devicename(self):
        """Testing function _devicename."""
        pass

    def test_valid(self):
        """Testing function valid."""
        pass


class TestCheckFile(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test__keys_in_filename(self):
        """Testing function _keys_in_filename."""
        pass

    def test_valid(self):
        """Testing function valid."""
        pass

    def test_contents(self):
        """Testing function contents."""
        pass

    def test__valid_filename(self):
        """Testing function _valid_filename."""
        pass

    def test__read_data_from_file(self):
        """Testing function _read_data_from_file."""
        pass


if __name__ == '__main__':
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
