#!/usr/bin/env python3
"""Test the db_device library in the infoset.db module."""

import unittest
import json
from datetime import datetime

from pprint import pprint

from infoset.api import API, CACHE
from infoset.db import db_device
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class APITestCase(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################

    # Setup database based on the config
    database = unittest_setup_db.TestData()

    # Define expected values
    expected = {}
    expected['values'] = database.values()
    expected['idx_device'] = database.idx_device()
    expected['idx_deviceagent'] = database.idx_deviceagent()
    expected['agent'] = database.agent()
    expected['devicename'] = database.devicename()
    expected['id_agent'] = database.id_agent()
    expected['agent_label'] = database.agent_label()

    # Retrieve data
    test_object = db_device.GetIDXDevice(expected['idx_device'])

    def setUp(self):
        """Setup the environment prior to testing."""
        # Test mode
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_lastcontacts(self):
        """Testing method / function lastcontacts."""
        # Initialize key variables
        precision = 5

        #######################################################################
        # Try with secondsago = 3600
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = '/infoset/api/v1/lastcontacts?secondsago=3600'
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with secondsago = 60 (No values expected)
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to a minute ago
        uri = '/infoset/api/v1/lastcontacts?secondsago=60'
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

        #######################################################################
        # Try with ts_start = 0
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = '/infoset/api/v1/lastcontacts?ts_start=0'
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = an hour ago
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 3600
        uri = '/infoset/api/v1/lastcontacts?ts_start={}'.format(ts_start)
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = a minute ago
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 60
        uri = '/infoset/api/v1/lastcontacts?ts_start={}'.format(ts_start)
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test type of result
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

    def test_id_agents(self):
        """Testing method / function id_agents."""
        # Initialize key variables
        precision = 5

        #######################################################################
        # Try with default values
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = '/infoset/api/v1/lastcontacts/id_agents'
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Further testing
        result = results[0]
        self.assertEqual(result['agent'], self.expected['agent'])
        self.assertEqual(result['devicename'], self.expected['devicename'])
        self.assertEqual(result['id_agent'], self.expected['id_agent'])
        self.assertEqual('timeseries' in result, True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]

        # We should only have a single result to test
        for agent_label, data_dict in result['timeseries'].items():
            # Test match for agent_label
            self.assertEqual(agent_label, self.expected['agent_label'])

            for key, value in data_dict.items():
                # Test presence of timeseries values
                if key == 'timestamp':
                    self.assertEqual(value, expected['timestamp'])
                elif key == 'value':
                    self.assertEqual(
                        round(value, precision),
                        round(expected['value'], precision))

        #######################################################################
        # Try with secondsago = 3600
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = '/infoset/api/v1/lastcontacts/id_agents?secondsago=3600'
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Further testing
        result = results[0]
        self.assertEqual(result['agent'], self.expected['agent'])
        self.assertEqual(result['devicename'], self.expected['devicename'])
        self.assertEqual(result['id_agent'], self.expected['id_agent'])
        self.assertEqual('timeseries' in result, True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]

        # We should only have a single result to test
        for agent_label, data_dict in result['timeseries'].items():
            # Test match for agent_label
            self.assertEqual(agent_label, self.expected['agent_label'])

            for key, value in data_dict.items():
                # Test presence of timeseries values
                if key == 'timestamp':
                    self.assertEqual(value, expected['timestamp'])
                elif key == 'value':
                    self.assertEqual(
                        round(value, precision),
                        round(expected['value'], precision))

        #######################################################################
        # Try with secondsago = 60 (No response expected)
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = '/infoset/api/v1/lastcontacts/id_agents?secondsago=60'
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

        #######################################################################
        # Try with ts_star = 0
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = '/infoset/api/v1/lastcontacts/id_agents?ts_start=0'
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Further testing
        result = results[0]
        self.assertEqual(result['agent'], self.expected['agent'])
        self.assertEqual(result['devicename'], self.expected['devicename'])
        self.assertEqual(result['id_agent'], self.expected['id_agent'])
        self.assertEqual('timeseries' in result, True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]

        # We should only have a single result to test
        for agent_label, data_dict in result['timeseries'].items():
            # Test match for agent_label
            self.assertEqual(agent_label, self.expected['agent_label'])

            for key, value in data_dict.items():
                # Test presence of timeseries values
                if key == 'timestamp':
                    self.assertEqual(value, expected['timestamp'])
                elif key == 'value':
                    self.assertEqual(
                        round(value, precision),
                        round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = an hour ago
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 3600
        uri = (
            '/infoset/api/v1/lastcontacts/id_agents?ts_start={}'
            ''.format(ts_start))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Further testing
        result = results[0]
        self.assertEqual(result['agent'], self.expected['agent'])
        self.assertEqual(result['devicename'], self.expected['devicename'])
        self.assertEqual(result['id_agent'], self.expected['id_agent'])
        self.assertEqual('timeseries' in result, True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]

        # We should only have a single result to test
        for agent_label, data_dict in result['timeseries'].items():
            # Test match for agent_label
            self.assertEqual(agent_label, self.expected['agent_label'])

            for key, value in data_dict.items():
                # Test presence of timeseries values
                if key == 'timestamp':
                    self.assertEqual(value, expected['timestamp'])
                elif key == 'value':
                    self.assertEqual(
                        round(value, precision),
                        round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = 15 minutes ago (No values expected)
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 900
        uri = (
            '/infoset/api/v1/lastcontacts/id_agents?ts_start={}'
            ''.format(ts_start))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

    def test_deviceagents(self):
        """Testing method / function deviceagents."""
        # Initialize key variables
        precision = 5

        #######################################################################
        # Try with secondsago = 3600
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = (
            '/infoset/api/v1/lastcontacts/deviceagents/{}?secondsago=3600'
            ''.format(self.expected['idx_deviceagent']))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with secondsago = 60 (No response expected)
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = (
            '/infoset/api/v1/lastcontacts/deviceagents/{}?secondsago=60'
            ''.format(self.expected['idx_deviceagent']))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

        #######################################################################
        # Try with ts_star = 0
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = (
            '/infoset/api/v1/lastcontacts/deviceagents/{}?ts_start=0'
            ''.format(self.expected['idx_deviceagent']))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = an hour ago
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 3600
        uri = (
            '/infoset/api/v1/lastcontacts/deviceagents/{}?ts_start={}'
            ''.format(self.expected['idx_deviceagent'], ts_start))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = 15 minutes ago (No values expected)
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 900
        uri = (
            '/infoset/api/v1/lastcontacts/deviceagents/{}?ts_start={}'
            ''.format(self.expected['idx_deviceagent'], ts_start))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

    def test_devicename_agents(self):
        """Testing method / function devicename_agents."""
        # Initialize key variables
        precision = 5

        #######################################################################
        # Try with secondsago = 3600
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = (
            '/infoset/api/v1/lastcontacts/devicenames/{}/id_agents/{}'
            '?secondsago=3600'
            ''.format(self.expected['devicename'], self.expected['id_agent']))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with secondsago = 60 (No response expected)
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = (
            '/infoset/api/v1/lastcontacts/devicenames/{}/id_agents/{}'
            '?secondsago=60'
            ''.format(self.expected['devicename'], self.expected['id_agent']))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

        #######################################################################
        # Try with ts_star = 0
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        uri = (
            '/infoset/api/v1/lastcontacts/devicenames/{}/id_agents/{}'
            '?ts_start=0'
            ''.format(self.expected['devicename'], self.expected['id_agent']))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = an hour ago
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 3600
        uri = (
            '/infoset/api/v1/lastcontacts/devicenames/{}/id_agents/{}'
            '?ts_start={}'
            ''.format(
                self.expected['devicename'],
                self.expected['id_agent'],
                ts_start))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)

        # First item in expected should be the most recent contact.
        # Expected['values'] is sorted by timestamp.
        expected = self.expected['values'][0]
        result = results[0]

        self.assertEqual(result['timestamp'], expected['timestamp'])
        self.assertEqual(
            round(result['value'], precision),
            round(expected['value'], precision))

        #######################################################################
        # Try with ts_start = 15 minutes ago (No values expected)
        #######################################################################

        # Clear the memory cache
        CACHE.clear()

        # Get results for up to an hour ago
        ts_start = int(datetime.utcnow().timestamp()) - 900
        uri = (
            '/infoset/api/v1/lastcontacts/devicenames/{}/id_agents/{}'
            '?ts_start={}'
            ''.format(
                self.expected['devicename'],
                self.expected['id_agent'],
                ts_start))
        response = self.API.get(uri)
        results = json.loads(response.get_data(as_text=True))

        # Test
        self.assertEqual(isinstance(results, list), True)
        self.assertEqual(bool(results), False)

    def test__start_timestamp(self):
        """Testing method / function _start_timestamp."""
        # Tested by other unittests here
        pass


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
