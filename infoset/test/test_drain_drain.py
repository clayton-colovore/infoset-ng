#!/usr/bin/env python3
"""Test the classes in the infoset.cache.validate module."""

# Standard imports
import unittest
import json
import tempfile

# Infoset imports
from infoset.utils import general
from infoset.cache import drain
from infoset.test import unittest_db
from infoset.test import unittest_variables


class TestDrain(unittest.TestCase):
    """Checks all functions and methods."""

    # Initialize key variables
    setup = unittest_variables.TestVariables()
    data = setup.cache_data()

    # Create valid file filled with valid data
    directory = tempfile.mkdtemp()
    filepath = ('%s/%s_%s_%s.json') % (
        directory,
        data['timestamp'],
        data['id_agent'],
        general.hashstring(data['devicename']))
    with open(filepath, 'w') as f_handle:
        json.dump(data, f_handle)

    # Create a valid Drain object
    ingest = drain.Drain(filepath)

    def test___init__(self):
        """Testing function __init__."""
        pass

    def test_valid(self):
        """Testing function valid."""
        # Test
        result = self.ingest.valid()
        self.assertEqual(result, True)

    def test_id_agent(self):
        """Testing function id_agent."""
        # Test
        result = self.ingest.id_agent()
        self.assertEqual(result, self.data['id_agent'])

    def test_timestamp(self):
        """Testing function timestamp."""
        # Test
        result = self.ingest.timestamp()
        self.assertEqual(result, self.data['timestamp'])

    def test_agent(self):
        """Testing function agent."""
        # Test
        result = self.ingest.agent()
        self.assertEqual(result, self.data['agent'])

    def test_devicename(self):
        """Testing function devicename."""
        # Test
        result = self.ingest.devicename()
        self.assertEqual(result, self.data['devicename'])

    def test_counter32(self):
        """Testing function counter32."""
        pass

    def test_counter64(self):
        """Testing function counter64."""
        pass

    def test_floating(self):
        """Testing function floating."""
        pass

    def test_timeseries(self):
        """Testing function timeseries."""
        pass

    def test_timefixed(self):
        """Testing function timefixed."""
        pass

    def test_sources(self):
        """Testing function sources."""
        pass

    def test_purge(self):
        """Testing function purge."""
        pass


if __name__ == '__main__':
    # Test the configuration variables
    unittest_db.validate()

    # Do the unit test
    unittest.main()
