"""infoset-ng database API. Device table."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.db import db_device
from infoset.db import db_deviceagent
from infoset.api import CACHE

# Define the DEVICES global variable
DEVICES = Blueprint('DEVICES', __name__)


@DEVICES.route('/devices/<int:value>')
@CACHE.cached()
def db_getidxdevice(value):
    """Get device data from the DB by idx value.

    Args:
        value: Index from the Device table

    Returns:
        Home Page

    """
    # Initialize key variables
    idx_device = int(value)

    # Get data
    query = db_device.GetIDXDevice(idx_device)
    data = query.everything()

    # Return
    return jsonify(data)


@DEVICES.route('/devices/<int:value>/agents')
@CACHE.cached()
def db_deviceagent_agentindices(value):
    """Get all agent indices from the DB.

    Args:
        idx_device: Index value of device

    Returns:
        List of agent indices reporting on the device

    """
    # Initialize key variables
    idx_device = int(value)

    # Process cache miss
    data = db_deviceagent.agent_indices(idx_device)

    # Return
    return jsonify(data)
