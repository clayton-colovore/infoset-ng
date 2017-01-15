"""infoset-ng database API. Data table."""

# Standard imports
import time

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.utils import general
from infoset.db import db_agent
from infoset.db import db_data
from infoset.db import db_device
from infoset.db import db_deviceagent
from infoset.api import CACHE, CONFIG

# Define the DB_DATA global variable
DB_DATA = Blueprint('DB_DATA', __name__)


@DB_DATA.route('/db/data/ts_lastcontacts/<ts_start>')
def db_ts_dlc(ts_start):
    """Get last contact data from the DB.

    Args:
        ts_start: Timestamp to start from

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api:db/data/ts_lastcontacts/{}'.format(ts_start))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_data.last_contacts(int(ts_start))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DB_DATA.route(
    '/db/data/ts_lastcontactsbydevice/'
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
    key = ('infoset.api:db/data/ts_lastcontactsbydevice/{}/{}'
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


@DB_DATA.route(
    '/db/data/ts_lastcontactsbydeviceagent/'
    '<devicename>/<id_agent>/<ts_start>')
def db_dlc_ts_deviceagent(devicename, id_agent, ts_start):
    """Get last contact data from the DB.

    Args:
        ts_start: Timestamp to start from

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api:db/data/ts_lastcontactsbydeviceagent/{}/{}/{}'
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


@DB_DATA.route('/db/data/lastcontacts')
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
    key = ('infoset.api:db/data/lastcontacts')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_data.last_contacts(int(ts_start))
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DB_DATA.route(
    '/db/data/lastcontactsbydevice/'
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
    key = ('infoset.api:db/data/lastcontactsbydevice/{}'
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


@DB_DATA.route(
    '/db/data/lastcontactsbydeviceagent/'
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
    key = ('infoset.api:db/data/lastcontactsbydeviceagent/{}/{}'
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


@DB_DATA.route(
    '/db/data/getidxdata/<value>/<ts_start>/<ts_stop>')
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
    key = ('infoset.api:db/data/getidxdata/{}/{}/{}'
           ''.format(value, ts_start, ts_stop))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_data.GetIDXData(
            CONFIG,
            general.integerize(value),
            general.integerize(ts_start),
            general.integerize(ts_stop))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)
