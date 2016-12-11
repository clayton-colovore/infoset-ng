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


class TestOther(unittest.TestCase):
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
    # Test the configuration variables
    db_unittest.validate()

    # Do the unit test
    unittest.main()
