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


if __name__ == '__main__':
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
