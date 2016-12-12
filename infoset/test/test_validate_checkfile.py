#!/usr/bin/env python3
"""Test the general module."""

# Standard imports
import unittest
import tempfile
import time
import os

# Infoset imports
from infoset.cache import validate
from infoset.utils import general
from infoset.test import db_unittest


class TestCheckFile(unittest.TestCase):
    """Checks all functions and methods."""

    def test___init__(self):
        """Testing function __init__."""
        # Test non existent file
        directory = tempfile.mkdtemp()
        badfile = general.randomstring()
        result = validate._CheckFile(badfile)
        self.assertEqual(result.valid(), False)

        # Test bad filename, existing file (Non hex characters in name)
        badfile = ('%s/%s_%s_%s.json') % (
            directory, int(time.time()),
            general.randomstring(),
            general.randomstring())
        data = general.randomstring()
        with open(badfile, 'w') as f_handle:
            f_handle.write(data)
        result = validate._CheckFile(badfile)
        self.assertEqual(result.valid(), False)
        os.remove(badfile)

        # Test good filename, no data
        id_agent = general.hashstring(general.randomstring())
        hosthash = general.hashstring(general.randomstring())
        filename = ('%s/%s_%s_%s.json') % (
            directory,
            int(time.time()),
            id_agent,
            hosthash)
        data = general.randomstring()
        with open(filename, 'w') as f_handle:
            f_handle.write(data)
        result = validate._CheckFile(badfile)
        self.assertEqual(result.valid(), False)
        os.remove(filename)

    def test__keys_in_filename(self):
        """Testing function _keys_in_filename."""
        pass

    def test_valid(self):
        """Testing function valid."""
        pass

    def test_contents(self):
        """Testing function contents."""
        pass


if __name__ == '__main__':
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
