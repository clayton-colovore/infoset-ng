"""infoset-ng database API. Data table."""

# Standard imports
from datetime import datetime

# Flask imports
from flask import Blueprint, jsonify, request

# Infoset-ng imports
from infoset.utils import general
from infoset.db import db_agent
from infoset.db import db_data
from infoset.db import db_device
from infoset.db import db_deviceagent
from infoset.api import CACHE, CONFIG

# Define the LASTCONTACTS global variable
LASTCONTACTS = Blueprint('LASTCONTACTS', __name__)


@LASTCONTACTS.route('/lastcontacts')
def lastcontacts():
    """Get last contact data from the DB.

    Args:
        None

    Returns:
        data: JSON data for the selected agent

    """
    # Get starting timestamp
    secondsago = general.integerize(request.args.get('secondsago'))
    timestamp = general.integerize(request.args.get('ts_start'))
    if bool(timestamp) is True:
        ts_start = _start_timestamp(timestamp, relative=False)
    else:
        ts_start = _start_timestamp(secondsago)

    # Get data from cache
    key = ('DB/Data/secondsago/{}'.format(secondsago))
    cache_value = CACHE.get(key)

    if cache_value is None:
        data = db_data.last_contacts(ts_start)
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@LASTCONTACTS.route('/lastcontacts/deviceagents/<int:value>')
def deviceagents(value):
    """Get last contact data from the DB.

    Args:
        value: Index from the DeviceAgent table
        ts_start: Timestamp to start from

    Returns:
        data: JSON data for the selected agent

    """
    # Initialize key variables
    idx_deviceagent = int(value)

    # Get starting timestamp
    secondsago = general.integerize(request.args.get('secondsago'))
    timestamp = general.integerize(request.args.get('ts_start'))
    if bool(timestamp) is True:
        ts_start = _start_timestamp(timestamp, relative=False)
    else:
        ts_start = _start_timestamp(secondsago)

    # Get data from cache
    key = ('DB/DeviceAgent/secondsago/{}'.format(secondsago))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_data.last_contacts_by_device(idx_deviceagent, ts_start)
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@LASTCONTACTS.route(
    'lastcontacts/devicenames/<string:devicename>/id_agents/<string:id_agent>')
def devicename_agents(devicename, id_agent):
    """Get last contact data from the DB.

    Args:
        devicename: Device table devicename
        id_agent: Agent table id_agent

    Returns:
        data: JSON data for the selected agent

    """
    # Get starting timestamp
    secondsago = general.integerize(request.args.get('secondsago'))
    timestamp = general.integerize(request.args.get('ts_start'))
    if bool(timestamp) is True:
        ts_start = _start_timestamp(timestamp, relative=False)
    else:
        ts_start = _start_timestamp(secondsago)

    # Get data from cache
    key = (
        'DB/Multitable/devicename/{}/id_agent/{}/secondsago/{}'
        ''.format(devicename, id_agent, secondsago))
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


def _start_timestamp(secondsago=None, relative=False):
    """Determine the default starting timestamp when not provided.

    Args:
        None

    Returns:
        ts_start: Timestamp

    """
    # Provide a UTC timestamp 10x the configured interval
    interval = CONFIG.interval()

    if (bool(secondsago) is False) or (secondsago < 0):
        timestamp = int(datetime.utcnow().timestamp()) - (interval * 10)
    else:
        if bool(relative) is True:
            timestamp = int(datetime.utcnow().timestamp()) - secondsago
        else:
            timestamp = abs(secondsago)

    # Return
    ts_start = general.normalized_timestamp(timestamp)
    return ts_start
