#!/usr/bin/env python3
"""Test the general module."""

# Standard imports
import unittest
import tempfile
import json
import time
import os
from mock import Mock

# Infoset imports
from infoset.cache import validate
from infoset.utils import configuration
from infoset.utils import log
from infoset.utils import general
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


if __name__ == '__main__':
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
