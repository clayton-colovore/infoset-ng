#!/usr/bin/env python3
"""Test the classes in the infoset.cache.validate module."""

# Standard imports
import unittest
import json
import os
import tempfile

# Infoset imports
from infoset.utils import general
from infoset.cache import drain
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class TestDrain(unittest.TestCase):
    """Checks all functions and methods."""

    # Initialize key variables
    setup = unittest_setup.TestVariables()
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

    @classmethod
    def tearDownClass(cls):
        """Clean up when all over."""
        # Delete unnecessary files
        os.remove(cls.filepath)

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
        # Initialize key variables
        datapoints = _expected(self.data, 32)
        found = 0

        # Test
        results = self.ingest.counter32()
        for datapoint in datapoints:
            for result in results:
                if result['id_datapoint'] == datapoint['id_datapoint']:
                    self.assertEqual(
                        result['timestamp'], datapoint['timestamp'])
                    self.assertEqual(
                        result['value'], datapoint['value'])
                    self.assertEqual(
                        result['id_agent'], datapoint['id_agent'])

                    # Increment found
                    found += 1

        # Make sure that all are found
        self.assertEqual(len(results), len(datapoints))
        self.assertEqual(len(results), found)

    def test_counter64(self):
        """Testing function counter64."""
        # Initialize key variables
        datapoints = _expected(self.data, 64)
        found = 0

        # Test
        results = self.ingest.counter64()
        for datapoint in datapoints:
            for result in results:
                if result['id_datapoint'] == datapoint['id_datapoint']:
                    self.assertEqual(
                        result['timestamp'], datapoint['timestamp'])
                    self.assertEqual(
                        result['value'], datapoint['value'])
                    self.assertEqual(
                        result['id_agent'], datapoint['id_agent'])

                    # Increment found
                    found += 1

        # Make sure that all are found
        self.assertEqual(len(results), len(datapoints))
        self.assertEqual(len(results), found)

    def test_floating(self):
        """Testing function floating."""
        # Initialize key variables
        datapoints = _expected(self.data, 1)
        found = 0

        # Test
        results = self.ingest.floating()
        for datapoint in datapoints:
            for result in results:
                if result['id_datapoint'] == datapoint['id_datapoint']:
                    self.assertEqual(
                        result['timestamp'], datapoint['timestamp'])
                    self.assertEqual(
                        result['value'], datapoint['value'])
                    self.assertEqual(
                        result['id_agent'], datapoint['id_agent'])

                    # Increment found
                    found += 1

        # Make sure that all are found
        self.assertEqual(len(results), len(datapoints))
        self.assertEqual(len(results), found)

    def test_timeseries(self):
        """Testing function timeseries."""
        # Initialize key variables
        datapoints = []
        found = 0

        # Populate datapoints list
        datapoints.extend(_expected(self.data, 1))
        datapoints.extend(_expected(self.data, 32))
        datapoints.extend(_expected(self.data, 64))

        # Test
        results = self.ingest.timeseries()
        for datapoint in datapoints:
            for result in results:
                if result['id_datapoint'] == datapoint['id_datapoint']:
                    self.assertEqual(
                        result['timestamp'], datapoint['timestamp'])
                    self.assertEqual(
                        result['value'], datapoint['value'])
                    self.assertEqual(
                        result['id_agent'], datapoint['id_agent'])

                    # Increment found
                    found += 1

        # Make sure that all are found
        self.assertEqual(len(results), len(datapoints))
        self.assertEqual(len(results), found)

    def test_timefixed(self):
        """Testing function timefixed."""
        # Initialize key variables
        datapoints = _expected(self.data, None)
        found = 0

        # Test
        results = self.ingest.timefixed()
        for datapoint in datapoints:
            for result in results:
                if result['id_datapoint'] == datapoint['id_datapoint']:
                    self.assertEqual(
                        result['timestamp'], datapoint['timestamp'])
                    self.assertEqual(
                        result['value'], datapoint['value'])
                    self.assertEqual(
                        result['id_agent'], datapoint['id_agent'])

                    # Increment found
                    found += 1

        # Make sure that all are found
        self.assertEqual(len(results), len(datapoints))
        self.assertEqual(len(results), found)

    def test_sources(self):
        """Testing function sources."""
        # Initialize key variables
        sources = _sources(self.data)
        found = 0

        # Test
        results = self.ingest.sources()
        for source in sources:
            for result in results:
                if result['id_datapoint'] == source['id_datapoint']:
                    self.assertEqual(
                        result['id_agent'], source['id_agent'])
                    self.assertEqual(
                        result['agent_label'], source['agent_label'])
                    self.assertEqual(
                        result['agent_source'], source['agent_source'])
                    self.assertEqual(
                        result['description'], source['description'])
                    self.assertEqual(
                        result['base_type'], source['base_type'])

                    # Increment found
                    found += 1

        # Make sure that all are found
        self.assertEqual(len(results), len(sources))
        self.assertEqual(len(results), found)

    def test_purge(self):
        """Testing function purge."""
        directory = tempfile.mkdtemp()
        filepath = ('%s/%s_%s_%s.json') % (
            directory,
            self.data['timestamp'],
            self.data['id_agent'],
            general.hashstring(self.data['devicename']))
        with open(filepath, 'w') as f_handle:
            json.dump(self.data, f_handle)

        # Create a valid Drain object
        ingest = drain.Drain(filepath)

        # Test
        self.assertEqual(os.path.exists(filepath), True)
        self.assertEqual(os.path.isfile(filepath), True)
        ingest.purge()
        self.assertEqual(os.path.exists(filepath), False)
        self.assertEqual(os.path.isfile(filepath), False)


def _expected(data, base_type):
    """Convert data read from cache file to format for ingester.

    args:
        data: Data read from cache file
        base_type: Base type to filter by

    returns:
        expected: List of dicts

    """
    # Initialize key variables
    id_agent = data['id_agent']
    agent = data['agent']
    devicename = data['devicename']
    timestamp = data['timestamp']
    expected = []

    # Get all 32 bit counter values from data
    if base_type is not None:
        primary_key = 'timeseries'
    else:
        primary_key = 'timefixed'

    # Retrieve data
    if primary_key in data:
        for label, metadata in data[primary_key].items():
            # Isolate 32 bit counter data
            if metadata['base_type'] == base_type:
                # Create list of dicts of data
                for data_item in metadata['data']:
                    index = data_item[0]
                    value = data_item[1]
                    expected.append(
                        {'id_agent': id_agent,
                         'id_datapoint': drain._id_datapoint(
                             id_agent, label, index, agent, devicename),
                         'value': value,
                         'timestamp': timestamp}
                    )

    # Return
    return expected


def _sources(data):
    """Convert data read from cache file to format for ingester.

    args:
        data: Data read from cache file
        base_type: Base type to filter by

    returns:
        data_sources: List of dicts

    """
    # Initialize key variables
    id_agent = data['id_agent']
    agent = data['agent']
    devicename = data['devicename']
    primary_keys = ['timeseries', 'timefixed']
    data_sources = []

    # Retrieve data
    for primary_key in primary_keys:
        # Skip if there are no matching keys
        if primary_key not in data:
            continue

        # Process data
        for label, metadata in data[primary_key].items():
            # Create list of dicts of data
            for data_item in metadata['data']:
                index = data_item[0]
                source = data_item[2]
                data_sources.append(
                    {'id_agent': id_agent,
                     'id_datapoint': drain._id_datapoint(
                         id_agent, label, index, agent, devicename),
                     'agent_label': label,
                     'agent_source': source,
                     'description': metadata['description'],
                     'base_type': metadata['base_type']}
                )

    # Return
    return data_sources


if __name__ == '__main__':
    # Test the configuration variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
