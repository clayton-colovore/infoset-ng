#!/usr/bin/env python3
"""Test the CheckFile class in the infoset.cache.validate module."""

# Standard imports
import unittest
import tempfile
import time
import os
import json

# Infoset imports
from infoset.cache import validate
from infoset.utils import general
from infoset.test import unittest_db


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
        # Initialize key variables
        id_agent = general.hashstring(general.randomstring())
        hosthash = general.hashstring(general.randomstring())
        timestamp = general.normalized_timestamp()

        # Create a directory and filename for testing
        directory = tempfile.mkdtemp()
        filename = ('%s/%s_%s_%s.json') % (
            directory,
            timestamp,
            id_agent,
            hosthash)

        # Test with good data
        data = {
            'id_agent': id_agent,
            'timestamp': timestamp
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        self.assertEqual(result._keys_in_filename(), True)

        # Test with bad data (missing id_agent value)
        data = {
            'id_agent': '',
            'timestamp': timestamp
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        self.assertEqual(result._keys_in_filename(), False)

        # Test with bad data (mismatched timestamp value)
        data = {
            'id_agent': id_agent,
            'timestamp': 0
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        self.assertEqual(result._keys_in_filename(), False)

        # Test with bad data (string timestamp value)
        data = {
            'id_agent': id_agent,
            'timestamp': str(timestamp)
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        self.assertEqual(result._keys_in_filename(), False)

        # Test with bad data (string timestamp value)
        data = {
            'id_agent': id_agent,
            'timestamp': str(timestamp)
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        self.assertEqual(result._keys_in_filename(), False)

        # Test with bad data
        # (non normalized timestamp value in filename and data)
        bad_time = timestamp + 1
        bad_filename = ('%s/%s_%s_%s.json') % (
            directory,
            bad_time,
            id_agent,
            hosthash)
        data = {
            'id_agent': id_agent,
            'timestamp': str(timestamp)
        }
        with open(bad_filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(bad_filename)
        self.assertEqual(result._keys_in_filename(), False)

        # Cleanup
        # Get all files in directory
        filenames = [filename for filename in os.listdir(
            directory) if os.path.isfile(
                os.path.join(directory, filename))]
        # Get the full filepath for the cache file and post
        for filename in filenames:
            filepath = os.path.join(directory, filename)
            os.remove(filepath)

    def test_valid(self):
        """Testing function valid."""
        # Initialize key variables
        devicename = general.hashstring(general.randomstring())
        id_agent = general.hashstring(general.randomstring())
        agent_name = general.hashstring(general.randomstring())
        hosthash = general.hashstring(devicename)
        timestamp = general.normalized_timestamp()

        # Create a directory and filename for testing
        directory = tempfile.mkdtemp()
        filename = ('%s/%s_%s_%s.json') % (
            directory,
            timestamp,
            id_agent,
            hosthash)

        # Test with good data
        data = {
            'id_agent': id_agent,
            'agent': agent_name,
            'devicename': devicename,
            'timestamp': timestamp
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        self.assertEqual(result.valid(), True)

        # Test with bad data (missing id_agent value)
        data = {
            'id_agent': '',
            'agent': agent_name,
            'devicename': devicename,
            'timestamp': timestamp
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        self.assertEqual(result.valid(), False)

        # Cleanup
        os.remove(filename)

    def test_contents(self):
        """Testing function contents."""
        # Initialize key variables
        devicename = general.hashstring(general.randomstring())
        id_agent = general.hashstring(general.randomstring())
        agent_name = general.hashstring(general.randomstring())
        hosthash = general.hashstring(devicename)
        timestamp = general.normalized_timestamp()

        # Create a directory and filename for testing
        directory = tempfile.mkdtemp()
        filename = ('%s/%s_%s_%s.json') % (
            directory,
            timestamp,
            id_agent,
            hosthash)

        # Test with good data
        data = {
            'id_agent': id_agent,
            'agent': agent_name,
            'devicename': devicename,
            'timestamp': timestamp
        }
        with open(filename, 'w') as f_handle:
            json.dump(data, f_handle)
        result = validate._CheckFile(filename)
        contents = result.contents()
        for key in contents.keys():
            self.assertEqual(contents[key], data[key])
        self.assertEqual(len(contents), len(data))


if __name__ == '__main__':
    # Test the configuration variables
    unittest_db.validate()

    # Do the unit test
    unittest.main()
