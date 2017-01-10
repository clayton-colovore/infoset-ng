#! /usr/bin/env python3
"""infoset-ng api."""

# Standard imports
import json
import time

# Flask imports
from flask import Flask, jsonify, request, abort

# Infoset-ng imports
from infoset.utils import configuration
from infoset.utils import general
from infoset.db import db_agent
from infoset.db import db_data
from infoset.db import db_datapoint
from infoset.db import db_device
from infoset.db import db_deviceagent
from infoset.api import cache

# Define the API global variable
API = Flask(__name__)
CONFIG = configuration.Config()
CACHE = cache.Cache(CONFIG)


@API.route('/infoset/api/v1.0/')
def index():
    """Function for handling home route.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    return 'Infoset API v1.0 Operational.\n'


@API.route('/infoset/api/v1.0/receive/<id_agent>', methods=['POST'])
def receive(id_agent):
    """Function for handling /infoset/api/v1.0/receive/<id_agent> route.

    Args:
        id_agent: Unique Identifier of an Infoset Agent

    Returns:
        Text response of Received

    """
    # Initialize key variables
    found_count = 0

    # Read configuration
    cache_dir = CONFIG.ingest_cache_directory()

    # Get JSON from incoming agent POST
    data = request.json

    # Make sure all the important keys are available
    keys = ['timestamp', 'id_agent', 'devicename']
    for key in keys:
        if key in data:
            found_count += 1

    # Do processing
    if found_count == 3:
        # Extract key values from posting
        try:
            timestamp = int(data['timestamp'])
        except:
            abort(404)
        id_agent = data['id_agent']
        devicename = data['devicename']

        # Create a hash of the devicename
        device_hash = general.hashstring(devicename, sha=1)
        json_path = (
            '%s/%s_%s_%s.json') % (cache_dir, timestamp, id_agent, device_hash)

        with open(json_path, "w+") as temp_file:
            json.dump(data, temp_file)

        # Return
        return 'OK'

    else:
        abort(404)


@API.route('/infoset/api/v1.0/db/data/ts_lastcontacts/<ts_start>')
def db_ts_dlc(ts_start):
    """Get last contact data from the DB.

    Args:
        ts_start: Timestamp to start from

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api.api:db/data/ts_lastcontacts/{}'.format(ts_start))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_data.last_contacts(int(ts_start))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route(
    '/infoset/api/v1.0/db/data/ts_lastcontactsbydevice/'
    '<idx_deviceagent>/<ts_start>')
def db_dlc_ts_device(idx_deviceagent, ts_start):
    """Get last contact data from the DB.

    Args:
        idx_deviceagent: Index from the DeviceAgent table
        ts_start: Timestamp to start from

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api.api:db/data/ts_lastcontactsbydevice/{}/{}'
           ''.format(idx_deviceagent, ts_start))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_data.last_contacts_by_device(
            int(idx_deviceagent), int(ts_start))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route(
    '/infoset/api/v1.0/db/data/ts_lastcontactsbydeviceagent/'
    '<devicename>/<id_agent>/<ts_start>')
def db_dlc_ts_deviceagent(devicename, id_agent, ts_start):
    """Get last contact data from the DB.

    Args:
        ts_start: Timestamp to start from

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api.api:db/data/ts_lastcontactsbydeviceagent/{}/{}/{}'
           ''.format(devicename, id_agent, ts_start))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        # Get idx_device and idx_agent
        device = db_device.GetDevice(devicename)
        if device.exists() is True:
            # Device Found
            idx_device = device.idx_device()

            # Now find idx_agent
            agent = db_agent.GetIDAgent(id_agent)
            if agent.exists() is True:
                idx_agent = agent.idx_agent()

            # Now get the idx_deviceagent
            deviceagent = db_deviceagent.GetDeviceAgent(idx_device, idx_agent)
            if deviceagent.exists() is True:
                idx_deviceagent = deviceagent.idx_deviceagent()

                # Now get the data
                data = db_data.last_contacts_by_device(
                    int(idx_deviceagent), int(ts_start))
                CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/data/lastcontacts')
def db_dlc():
    """Get last contact data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Initialize key variables
    ts_start = int(time.time())

    # Get data from cache
    key = ('infoset.api.api:db/data/lastcontacts')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_data.last_contacts(int(ts_start))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route(
    '/infoset/api/v1.0/db/data/lastcontactsbydevice/'
    '<idx_deviceagent>')
def db_dlc_device(idx_deviceagent):
    """Get last contact data from the DB.

    Args:
        idx_deviceagent: Index from the DeviceAgent table
        ts_start: Timestamp to start from

    Returns:
        Agent data

    """
    # Initialize key variables
    ts_start = int(time.time())

    # Get data from cache
    key = ('infoset.api.api:db/data/lastcontactsbydevice/{}'
           ''.format(idx_deviceagent))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_data.last_contacts_by_device(
            int(idx_deviceagent), int(ts_start))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route(
    '/infoset/api/v1.0/db/data/lastcontactsbydeviceagent/'
    '<devicename>/<id_agent>')
def db_dlc_deviceagent(devicename, id_agent):
    """Get last contact data from the DB.

    Args:
        ts_start: Timestamp to start from

    Returns:
        Agent data

    """
    # Initialize key variables
    ts_start = int(time.time())

    # Get data from cache
    key = ('infoset.api.api:db/data/lastcontactsbydeviceagent/{}/{}'
           ''.format(devicename, id_agent))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        # Get idx_device and idx_agent
        device = db_device.GetDevice(devicename)
        if device.exists() is True:
            # Device Found
            idx_device = device.idx_device()

            # Now find idx_agent
            agent = db_agent.GetIDAgent(id_agent)
            if agent.exists() is True:
                idx_agent = agent.idx_agent()

            # Now get the idx_deviceagent
            deviceagent = db_deviceagent.GetDeviceAgent(idx_device, idx_agent)
            if deviceagent.exists() is True:
                idx_deviceagent = deviceagent.idx_deviceagent()

                # Now get the data
                data = db_data.last_contacts_by_device(
                    int(idx_deviceagent), int(ts_start))
                CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route(
    '/infoset/api/v1.0/db/data/getidxdata/<value>/<ts_start>/<ts_stop>')
def db_getidxdata(value, ts_start, ts_stop):
    """Get Agent data from the DB by idx value.

    Args:
        value: idx_data value
        ts_start: Starting timestamp
        ts_stop: Ending timestamp

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/data/getidxdata/{}/{}/{}'
           ''.format(value, ts_start, ts_stop))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_data.GetIDXData(
            CONFIG, _integer(value), _integer(ts_start), _integer(ts_stop))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/agent/getidxagent/<value>')
def db_getidxagent(value):
    """Get Agent data from the DB by idx value.

    Args:
        None

    Returns:
        data: JSON data for the selected agent

    """
    # Get data from cache
    key = ('infoset.api.api:db/agent/getidxagent/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_agent.GetIDXAgent(_integer(value))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/agent/getidagent/<value>')
def db_agent_getid_agent(value):
    """Get Agent data from the DB by id_agent value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/agent/getidagent/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_agent.GetIDAgent(value)
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/agent/getallagents')
def db_agent_get_all_agents():
    """Get all agent data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api.api:db/agent/getallagents')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_agent.get_all_agents()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/datapoint/getiddatapoint/<value>')
def db_datapoint_getiddatapoint(value):
    """Get datapoint data from the DB by did value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/datapoint/getiddatapoint/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_datapoint.GetIDDatapoint(value)
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/datapoint/getidxdatapoint/<value>')
def db_getidxdatapoint(value):
    """Get datapoint data from the DB by idx value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/datapoint/getidxdatapoint/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_datapoint.GetIDXDatapoint(_integer(value))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/device/getidxdevice/<value>')
def db_getidxdevice(value):
    """Get device data from the DB by idx value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/device/getidxdevice/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_device.GetIDXDevice(_integer(value))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/getidxdeviceagent/<value>')
def db_getidxdeviceagent(value):
    """Get DeviceAgent data from the DB by idx value.

    Args:
        value: idx_deviceagent

    Returns:
        data: JSON data for the selected deviceagent

    """
    # Get data from cache
    key = ('infoset.api.api:db/deviceagent/getidxdeviceagent/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_deviceagent.GetIDXDeviceAgent(_integer(value))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/alldeviceindices')
def db_deviceagent_alldeviceindices():
    """Get all device indices from the DB.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/deviceagent/alldeviceindices')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_deviceagent.all_device_indices()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/agentindices/<idx_device>')
def db_deviceagent_agentindices(idx_device):
    """Get all agent indices from the DB.

    Args:
        idx_device: Index value of device

    Returns:
        List of agent indices reporting on the device

    """
    # Get data from cache
    key = ('infoset.api.api:db/deviceagent/agentindices/{}'.format(idx_device))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_deviceagent.agent_indices(_integer(idx_device))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/getalldeviceagents')
def db_devagt_get_all_device_agents():
    """Get all DeviceAgent data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api.api:db/deviceagent/getalldeviceagents')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_deviceagent.get_all_device_agents()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route(
    '/infoset/api/v1.0/db/datapoint/timeseries/<idx_device>/<idx_agent>')
def db_datapoint_timeseries(idx_device, idx_agent):
    """Get timeseries datapoint metadata.

    Args:
        idx_device: Index value of device
        idx_agent: Index value of agent

    Returns:
        List of agent indices reporting on the device

    """
    # Get data from cache
    key = ('infoset.api.api:db/datapoint/timeseries/{}/{}'
           ''.format(idx_device, idx_agent))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_datapoint.timeseries(
            _integer(idx_device), _integer(idx_agent))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/datapoint/timefixed/<idx_device>/<idx_agent>')
def db_datapoint_timefixed(idx_device, idx_agent):
    """Get timefixed datapoint metadata.

    Args:
        idx_device: Index value of device
        idx_agent: Index value of agent

    Returns:
        List of agent indices reporting on the device

    """
    # Get data from cache
    key = ('infoset.api.api:db/datapoint/timefixed/{}/{}'
           ''.format(idx_device, idx_agent))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_datapoint.timefixed(
            _integer(idx_device), _integer(idx_agent))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


def _integer(value):
    """Convert value to integer.

    Args:
        value: Value to convert

    Returns:
        result: Value converted to iteger

    """
    # Try conversion
    try:
        result = int(value)
    except:
        result = None

    # Return
    return result


def main():
    """Get Flask server running.

    Args:
        None

    Returns:
        None

    """
    # Start
    bind_port = CONFIG.bind_port()
    listen_address = CONFIG.listen_address()
    API.run(debug=True, host=listen_address, threaded=True, port=bind_port)


if __name__ == '__main__':
    main()
