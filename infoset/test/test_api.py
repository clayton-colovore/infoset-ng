#!/usr/bin/env python3
"""Test the db_agent library in the infoset.db module."""

import unittest
import os
import sys

from infoset.api import API
from infoset.test import unittest_setup_db
from infoset.test import unittest_setup


class APITestCase(unittest.TestCase):
    """Checks all functions and methods."""

    #########################################################################
    # General object setup
    #########################################################################
    def setUp(self):
        """Setup the environment prior to testing."""
        API.config['TESTING'] = True
        self.API = API.test_client()

    def test_index(self):
        """Testing method / function index."""
        # Initializing key variables
        expected = b'Infoset API v1.0 Operational.\n'
        response = self.API.get('/infoset/api/v1.0/')

        # Verify reponses
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, expected)

    def test_receive(self):
        """Testing method / function receive."""
        # Initializing key variables
        pass

    def test_db_ts_dlc(self):
        """Testing method / function db_ts_dlc."""
        # Initializing key variables
        pass

    def test_db_dlc_ts_device(self):
        """Testing method / function db_dlc_ts_device."""
        # Initializing key variables
        pass

    def test_db_dlc_ts_deviceagent(self):
        """Testing method / function db_dlc_ts_deviceagent."""
        # Initializing key variables
        pass

    def test_db_dlc(self):
        """Testing method / function db_dlc."""
        # Initializing key variables
        pass

    def test_db_dlc_device(self):
        """Testing method / function db_dlc_device."""
        # Initializing key variables
        pass

    def test_db_dlc_deviceagent(self):
        """Testing method / function db_dlc_deviceagent."""
        # Initializing key variables
        pass

    def test_db_getidxdata(self):
        """Testing method / function db_getidxdata."""
        # Initializing key variables
        pass

    def test_db_getidxagent(self):
        """Testing method / function db_getidxagent."""
        # Initializing key variables
        pass

    def test_db_agent_getid_agent(self):
        """Testing method / function db_agent_getid_agent."""
        # Initializing key variables
        pass

    def test_db_agent_get_all_agents(self):
        """Testing method / function db_agent_get_all_agents."""
        # Initializing key variables
        pass

    def test_db_datapoint_getiddatapoint(self):
        """Testing method / function db_datapoint_getiddatapoint."""
        # Initializing key variables
        pass

    def test_db_getidxdatapoint(self):
        """Testing method / function db_getidxdatapoint."""
        # Initializing key variables
        pass

    def test_db_getidxdevice(self):
        """Testing method / function db_getidxdevice."""
        # Initializing key variables
        pass

    def test_db_getidxdeviceagent(self):
        """Testing method / function db_getidxdeviceagent."""
        # Initializing key variables
        pass

    def test_db_deviceagent_alldeviceindices(self):
        """Testing method / function db_deviceagent_alldeviceindices."""
        # Initializing key variables
        pass

    def test_db_deviceagent_agentindices(self):
        """Testing method / function db_deviceagent_agentindices."""
        # Initializing key variables
        pass

    def test_db_devagt_get_all_device_agents(self):
        """Testing method / function db_devagt_get_all_device_agents."""
        # Initializing key variables
        pass

    def test_db_datapoint_timeseries(self):
        """Testing method / function db_datapoint_timeseries."""
        # Initializing key variables
        pass

    def test_db_datapoint_timefixed(self):
        """Testing method / function db_datapoint_timefixed."""
        # Initializing key variables
        pass

    def test__integer(self):
        """Testing method / function _integer."""
        # Initializing key variables
        pass

    def test_main(self):
        """Testing method / function main."""
        # Initializing key variables
        pass

if __name__ == '__main__':
    # Test the environment variables
    unittest_setup.ready()

    # Do the unit test
    unittest.main()
