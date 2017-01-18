"""infoset-ng database API. DeviceAgent table."""

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.db import db_deviceagent
from infoset.api import CACHE


# Define the DEVICEAGENTS global variable
DEVICEAGENTS = Blueprint('DEVICEAGENTS', __name__)


@DEVICEAGENTS.route('/deviceagents/<int:value>')
def db_getidxdeviceagent(value):
    """Get DeviceAgent data from the DB by idx value.

    Args:
        value: idx_deviceagent

    Returns:
        data: JSON data for the selected deviceagent

    """
    # Initialize key variables
    idx_deviceagent = int(value)

    # Get data from cache
    key = ('DB/DeviceAgent/idx_deviceagent/{}'.format(idx_deviceagent))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_deviceagent.GetIDXDeviceAgent(idx_deviceagent)
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DEVICEAGENTS.route('/deviceagents')
def db_devagt_get_all_device_agents():
    """Get all DeviceAgent data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('DB/DeviceAgent')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_deviceagent.get_all_device_agents()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)
