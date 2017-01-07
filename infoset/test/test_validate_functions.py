#!/usr/bin/env python3
"""Test the functions in the infoset.cache.validate module."""

# Standard imports
import unittest
import tempfile
import json
import time
import os

# Infoset imports
from infoset.cache import validate
from infoset.utils import general
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestGeneral(unittest.TestCase):
    """Checks all functions and methods."""

    def test__valid_filename(self):
        """Testing function _valid_filename."""
        # Test bad filename
        filename = general.randomstring()
        result = validate._valid_filename(filename)
        self.assertEqual(result, False)

        # Test bad filename
        filename = str(int(time.time()))
        result = validate._valid_filename(filename)
        self.assertEqual(result, False)

        # Test bad filename
        filename = ('%s_%s') % (
            int(time.time()),
            general.hashstring(general.randomstring()))
        result = validate._valid_filename(filename)
        self.assertEqual(result, False)

        # Test bad filename
        filename = ('%s_%s_%s') % (
            int(time.time()),
            general.hashstring(general.randomstring()),
            general.hashstring(general.randomstring()))
        result = validate._valid_filename(filename)
        self.assertEqual(result, False)

        # Test bad filename (Non hex characters in name)
        filename = ('%s_%s') % (
            int(time.time()),
            general.randomstring())
        result = validate._valid_filename(filename)
        self.assertEqual(result, False)

        # Test bad filename (Non hex characters in name)
        filename = ('%s_%s_%s') % (
            int(time.time()),
            general.randomstring(),
            general.randomstring())
        result = validate._valid_filename(filename)
        self.assertEqual(result, False)

        # Test bad filename (Non hex characters in name)
        filename = ('%s_%s_%s.json') % (
            int(time.time()),
            general.randomstring(),
            general.randomstring())
        result = validate._valid_filename(filename)
        self.assertEqual(result, False)

        # Test good filename
        filename = ('%s_%s_%s.json') % (
            int(time.time()),
            general.hashstring(general.randomstring()),
            general.hashstring(general.randomstring()))
        result = validate._valid_filename(filename)
        self.assertEqual(result, True)

    def test__read_data_from_file(self):
        """Testing function _read_data_from_file."""
        # Create filename
        document = tempfile.NamedTemporaryFile(delete=False)
        filename = document.name

        # Write non JSON to file and test
        data = general.randomstring()
        with open(filename, 'w') as f_handle:
            f_handle.write(data)
        result = validate._read_data_from_file(filename)
        self.assertEqual(bool(result), False)
        self.assertEqual(result, {})

        # Write JSON to file and test
        data = {
            'key0': 0,
            'key1': 1,
            'key2': 2,
            'key3': 3,
            'key4': 4
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._read_data_from_file(filename)
        for key in result.keys():
            self.assertEqual(result[key], data[key])

        # Delete temporary file
        os.remove(filename)


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
