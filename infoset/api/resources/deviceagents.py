"""infoset-ng database API. DeviceAgent table."""

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.db import db_deviceagent
from infoset.api import CACHE


# Define the DEVICEAGENTS global variable
DEVICEAGENTS = Blueprint('DEVICEAGENTS', __name__)


@DEVICEAGENTS.route('/deviceagents/<int:value>')
@CACHE.cached()
def deviceagents_query(value):
    """Get DeviceAgent data from the DB by idx value.

    Args:
        value: idx_deviceagent

    Returns:
        data: JSON data for the selected deviceagent

    """
    # Initialize key variables
    idx_deviceagent = int(value)

    # Process cache miss
    query = db_deviceagent.GetIDXDeviceAgent(idx_deviceagent)
    data = query.everything()

    # Return
    return jsonify(data)


@DEVICEAGENTS.route('/deviceagents')
@CACHE.cached()
def deviceagents():
    """Get all DeviceAgent data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Get data
    data = db_deviceagent.get_all_device_agents()

    # Return
    return jsonify(data)
