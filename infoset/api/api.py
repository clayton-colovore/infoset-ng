#! /usr/bin/env python3
"""infoset-ng api."""

# Standard imports
import json

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

# Define the API global variable
API = Flask(__name__)


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
    config = configuration.Config()
    cache_dir = config.ingest_cache_directory()

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
    # Return
    query = db_data.GetIDXData(
        _integer(value), _integer(ts_start), _integer(ts_stop))
    data = query.everything()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/agent/getidxagent/<value>')
def db_getidxagent(value):
    """Get Agent data from the DB by idx value.

    Args:
        None

    Returns:
        data: JSON data for the selected agent

    """
    # Return
    query = db_agent.GetIDXAgent(_integer(value))
    data = query.everything()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/agent/getidagent/<value>')
def db_agent_getid_agent(value):
    """Get Agent data from the DB by id_agent value.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    query = db_agent.GetIDAgent(value)
    data = query.everything()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/agent/getallagents')
def db_agent_get_all_agents():
    """Get all agent data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Return
    data = db_agent.get_all_agents()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/datapoint/getiddatapoint/<value>')
def db_datapoint_getiddatapoint(value):
    """Get datapoint data from the DB by did value.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    query = db_datapoint.GetIDDatapoint(value)
    data = query.everything()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/datapoint/getidxdatapoint/<value>')
def db_getidxdatapoint(value):
    """Get datapoint data from the DB by idx value.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    query = db_datapoint.GetIDXDatapoint(_integer(value))
    data = query.everything()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/device/getidxdevice/<value>')
def db_getidxdevice(value):
    """Get device data from the DB by idx value.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    query = db_device.GetIDXDevice(_integer(value))
    data = query.everything()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/getidxdeviceagent/<value>')
def db_getidxdeviceagent(value):
    """Get DeviceAgent data from the DB by idx value.

    Args:
        None

    Returns:
        data: JSON data for the selected deviceagent

    """
    # Return
    query = db_deviceagent.GetIDXDeviceAgent(_integer(value))
    data = query.everything()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/alldeviceindices')
def db_deviceagent_alldeviceindices():
    """Get all device indices from the DB.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    data = db_deviceagent.all_device_indices()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/agentindices/<idx_device>')
def db_deviceagent_agentindices(idx_device):
    """Get all agent indices from the DB.

    Args:
        idx_device: Index value of device

    Returns:
        List of agent indices reporting on the device

    """
    # Return
    data = db_deviceagent.agent_indices(_integer(idx_device))
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/deviceagent/getalldeviceagents')
def db_devagt_get_all_device_agents():
    """Get all DeviceAgent data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Return
    data = db_deviceagent.get_all_device_agents()
    return jsonify(data)


@API.route('/infoset/api/v1.0/db/datapoint/charted/<idx_device>/<idx_agent>')
def db_datapoint_charted(idx_device, idx_agent):
    """Get charted datapoint metadata.

    Args:
        idx_device: Index value of device
        idx_agent: Index value of agent

    Returns:
        List of agent indices reporting on the device

    """
    # Return
    data = db_datapoint.charted(_integer(idx_device), _integer(idx_agent))
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
    # Return
    data = db_datapoint.timefixed(_integer(idx_device), _integer(idx_agent))
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
    config = configuration.Config()
    bind_port = config.bind_port()
    listen_address = config.listen_address()
    API.run(debug=True, host=listen_address, threaded=True, port=bind_port)


if __name__ == '__main__':
    main()
