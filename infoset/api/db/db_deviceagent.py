"""infoset-ng database API. DeviceAgent table."""

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.utils import general
from infoset.db import db_deviceagent
from infoset.api import CACHE


# Define the DB_DEVICEAGENT global variable
DB_DEVICEAGENT = Blueprint('DB_DEVICEAGENT', __name__)


@DB_DEVICEAGENT.route(
    '/db/deviceagent/getidxdeviceagent/<value>')
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
        query = db_deviceagent.GetIDXDeviceAgent(general.integerize(value))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DB_DEVICEAGENT.route('/db/deviceagent/alldeviceindices')
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


@DB_DEVICEAGENT.route(
    '/db/deviceagent/agentindices/<idx_device>')
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
        data = db_deviceagent.agent_indices(general.integerize(idx_device))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DB_DEVICEAGENT.route('/db/deviceagent/getalldeviceagents')
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
