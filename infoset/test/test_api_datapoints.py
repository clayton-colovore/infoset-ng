#!/usr/bin/env python3
"""Test the db_datapoint library in the infoset.db module."""

import unittest
import json
import time

from infoset.api import API, CACHE
from infoset.db import db_datapoint

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
    expected['idx_datapoint'] = database.idx_datapoint()
    expected['id_datapoint'] = database.id_datapoint()
    expected['idx_deviceagent'] = database.idx_deviceagent()
    expected['id_agent'] = database.id_agent()
    expected['devicename'] = database.devicename()
    expected['agent'] = database.agent()
    expected['values'] = database.values()

    # Retrieve data
    test_object = db_datapoint.GetIDXDatapoint(expected['idx_datapoint'])

    def setUp(self):
        """Setup the environment prior to testing."""
        # Test mode
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_datapoints(self):
        """Testing method / function datapoints."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = (
            '/infoset/api/v1/datapoints/{}'.format(
                self.expected['idx_datapoint'])
        )
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(result, dict), True)
        self.assertEqual(
            result['idx_datapoint'], self.test_object.idx_datapoint())
        self.assertEqual(
            result['id_datapoint'], self.test_object.id_datapoint())
        self.assertEqual(
            result['idx_deviceagent'], self.test_object.idx_deviceagent())
        self.assertEqual(
            result['idx_department'], self.test_object.idx_department())
        self.assertEqual(
            result['idx_billcode'], self.test_object.idx_billcode())
        self.assertEqual(result['agent_label'], self.test_object.agent_label())
        self.assertEqual(
            result['agent_source'], self.test_object.agent_source())
        self.assertEqual(result['billable'], self.test_object.billable())
        self.assertEqual(result['base_type'], self.test_object.base_type())
        self.assertEqual(
            result['timefixed_value'], self.test_object.timefixed_value())
        self.assertEqual(
            result['last_timestamp'], self.test_object.last_timestamp())
        self.assertEqual(result['exists'], self.test_object.exists())
        self.assertEqual(result['enabled'], self.test_object.enabled())

        # Test the number and names of keys
        keys = [
            'idx_datapoint', 'id_datapoint', 'idx_deviceagent',
            'idx_department', 'idx_billcode', 'agent_label', 'agent_source',
            'enabled', 'billable', 'base_type', 'timefixed_value',
            'last_timestamp', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_datapoints_query_1(self):
        """Testing method / function datapoints_query."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = (
            '/infoset/api/v1/datapoints?id_datapoint={}'
            ''.format(self.expected['id_datapoint']))
        response = self.API.get(uri)
        data = json.loads(response.get_data(as_text=True))
        result = data[0]

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, list), True)
        self.assertEqual(
            result['idx_datapoint'], self.test_object.idx_datapoint())
        self.assertEqual(
            result['id_datapoint'], self.test_object.id_datapoint())
        self.assertEqual(
            result['idx_deviceagent'], self.test_object.idx_deviceagent())
        self.assertEqual(
            result['idx_department'], self.test_object.idx_department())
        self.assertEqual(
            result['idx_billcode'], self.test_object.idx_billcode())
        self.assertEqual(result['agent_label'], self.test_object.agent_label())
        self.assertEqual(
            result['agent_source'], self.test_object.agent_source())
        self.assertEqual(result['billable'], self.test_object.billable())
        self.assertEqual(result['base_type'], self.test_object.base_type())
        self.assertEqual(
            result['timefixed_value'], self.test_object.timefixed_value())
        self.assertEqual(
            result['last_timestamp'], self.test_object.last_timestamp())
        self.assertEqual(result['exists'], self.test_object.exists())
        self.assertEqual(result['enabled'], self.test_object.enabled())

        # Test the number and names of keys
        keys = [
            'idx_datapoint', 'id_datapoint', 'idx_deviceagent',
            'idx_department', 'idx_billcode', 'agent_label', 'agent_source',
            'enabled', 'billable', 'base_type', 'timefixed_value',
            'last_timestamp', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_datapoints_query_2(self):
        """Testing method / function datapoints_query."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = (
            '/infoset/api/v1/datapoints?idx_deviceagent={}'
            ''.format(self.expected['idx_deviceagent']))
        response = self.API.get(uri)
        data = json.loads(response.get_data(as_text=True))
        result = data[0]

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, list), True)
        self.assertEqual(
            result['idx_datapoint'], self.test_object.idx_datapoint())
        self.assertEqual(
            result['id_datapoint'], self.test_object.id_datapoint())
        self.assertEqual(
            result['idx_deviceagent'], self.test_object.idx_deviceagent())
        self.assertEqual(
            result['idx_department'], self.test_object.idx_department())
        self.assertEqual(
            result['idx_billcode'], self.test_object.idx_billcode())
        self.assertEqual(result['agent_label'], self.test_object.agent_label())
        self.assertEqual(
            result['agent_source'], self.test_object.agent_source())
        self.assertEqual(result['billable'], self.test_object.billable())
        self.assertEqual(result['base_type'], self.test_object.base_type())
        self.assertEqual(
            result['timefixed_value'], self.test_object.timefixed_value())
        self.assertEqual(
            result['last_timestamp'], self.test_object.last_timestamp())
        self.assertEqual(result['exists'], self.test_object.exists())
        self.assertEqual(result['enabled'], self.test_object.enabled())

        # Test the number and names of keys
        keys = [
            'idx_datapoint', 'id_datapoint', 'idx_deviceagent',
            'idx_department', 'idx_billcode', 'agent_label', 'agent_source',
            'enabled', 'billable', 'base_type', 'timefixed_value',
            'last_timestamp', 'exists']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)

    def test_getdata_secondsago_1(self):
        """Testing method / function getdata."""
        # Clear the memory cache
        CACHE.clear()

        # Initialize key variables
        precision = 5

        # Get results for up to an hour ago
        uri = (
            '/infoset/api/v1/datapoints/{}/data?secondsago=3600'
            ''.format(self.expected['idx_datapoint']))
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        # Convert the list of expected values to an easy to compare dict
        check_dict = {}
        for item in self.expected['values']:
            check_dict[str(item['timestamp'])] = item['value']

        # Verify the expected data is there
        for timestamp, value in sorted(result.items()):
            if timestamp in check_dict:
                self.assertEqual(
                    round(result[timestamp], precision),
                    round(check_dict[timestamp], precision))
            else:
                self.assertEqual(value, 0)

    def test_getdata_secondsago_2(self):
        """Testing method / function getdata."""
        # Clear the memory cache
        CACHE.clear()

        # Get results for up to 1/4 hour ago - No data should be present
        uri = (
            '/infoset/api/v1/datapoints/{}/data?secondsago=900'
            ''.format(self.expected['idx_datapoint']))
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        # Go through the results
        for timestamp, value in sorted(result.items()):
            self.assertEqual(result[timestamp], 0)
            self.assertEqual(value, 0)

    def test_getdata_timestamp(self):
        """Testing method / function getdata."""
        # Clear the memory cache
        CACHE.clear()

        # Initialize key variables
        precision = 5
        ts_stop = int(time.time())
        ts_start = int(time.time()) - 3600

        # Get results for up to 1/4 hour ago - No data should be present
        uri = (
            '/infoset/api/v1/datapoints/{}/data?ts_start={}&ts_stop={}'
            ''.format(self.expected['idx_datapoint'], ts_start, ts_stop))
        response = self.API.get(uri)
        result = json.loads(response.get_data(as_text=True))

        # Convert the list of expected values to an easy to compare dict
        check_dict = {}
        for item in self.expected['values']:
            check_dict[str(item['timestamp'])] = item['value']

        # Verify the expected data is there
        for timestamp, value in sorted(result.items()):
            if timestamp in check_dict:
                self.assertEqual(
                    round(result[timestamp], precision),
                    round(check_dict[timestamp], precision))
            else:
                self.assertEqual(value, 0)

    def test_db_datapoint_summary(self):
        """Testing method / function db_datapoint_summary."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = '/infoset/api/v1/datapoints/all/summary'
        response = self.API.get(uri)
        data = json.loads(response.get_data(as_text=True))

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, dict), True)
        self.assertEqual(len(data), 1)

        for idx_datapoint, result in data.items():
            self.assertEqual(
                int(idx_datapoint), self.test_object.idx_datapoint())

            self.assertEqual(
                result['idx_deviceagent'], self.test_object.idx_deviceagent())
            self.assertEqual(
                result['agent_label'], self.test_object.agent_label())
            self.assertEqual(
                result['agent_source'], self.test_object.agent_source())

            # Get remaining values
            self.assertEqual(result['devicename'], self.expected['devicename'])
            self.assertEqual(result['id_agent'], self.expected['id_agent'])
            self.assertEqual(result['agent'], self.expected['agent'])

            # Test the number and names of keys
            keys = [
                'idx_deviceagent', 'agent_label',
                'agent_source', 'devicename', 'id_agent', 'agent']
            self.assertEqual(len(result), len(keys))
            for key in keys:
                self.assertEqual(key in result, True)

            # All done
            break

    def test_db_datapoint_summary_list(self):
        """Testing method / function db_datapoint_summary_list."""
        # Clear the memory cache
        CACHE.clear()

        # Get results
        uri = '/infoset/api/v1/datapoints/all/summarylist'
        response = self.API.get(uri)
        data = json.loads(response.get_data(as_text=True))
        result = data[0]

        # Verify reponse code
        self.assertEqual(response.status_code, 200)

        # Verify response content
        self.assertEqual(isinstance(data, list), True)
        self.assertEqual(
            result['idx_datapoint'], self.test_object.idx_datapoint())
        self.assertEqual(
            result['idx_deviceagent'], self.test_object.idx_deviceagent())
        self.assertEqual(result['agent_label'], self.test_object.agent_label())
        self.assertEqual(
            result['agent_source'], self.test_object.agent_source())

        # Get remaining values
        self.assertEqual(result['devicename'], self.expected['devicename'])
        self.assertEqual(result['id_agent'], self.expected['id_agent'])
        self.assertEqual(result['agent'], self.expected['agent'])

        # Test the number and names of keys
        keys = [
            'idx_datapoint', 'idx_deviceagent', 'agent_label', 'agent_source',
            'devicename', 'id_agent', 'agent']
        self.assertEqual(len(result), len(keys))
        for key in keys:
            self.assertEqual(key in result, True)


if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
