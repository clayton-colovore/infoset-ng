"""infoset-ng database API. Datapoint table."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.db import db_datapoint
from infoset.api import CACHE

# Define the AGENT global variable
DB_DATAPOINT = Blueprint('DB_DATAPOINT', __name__)


@DB_DATAPOINT.route('/db/datapoint/getiddatapoint/<value>')
def db_datapoint_getiddatapoint(value):
    """Get datapoint data from the DB by did value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api:db/datapoint/getiddatapoint/{}'.format(value))
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


@DB_DATAPOINT.route('/db/datapoint/getidxdatapoint/<value>')
def db_getidxdatapoint(value):
    """Get datapoint data from the DB by idx value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api:db/datapoint/getidxdatapoint/{}'.format(value))
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


@DB_DATAPOINT.route(
    '/db/datapoint/timeseries/<idx_device>/<idx_agent>')
def db_datapoint_timeseries(idx_device, idx_agent):
    """Get timeseries datapoint metadata.

    Args:
        idx_device: Index value of device
        idx_agent: Index value of agent

    Returns:
        List of agent indices reporting on the device

    """
    # Get data from cache
    key = ('infoset.api:db/datapoint/timeseries/{}/{}'
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


@DB_DATAPOINT.route('/db/datapoint/timefixed/<idx_device>/<idx_agent>')
def db_datapoint_timefixed(idx_device, idx_agent):
    """Get timefixed datapoint metadata.

    Args:
        idx_device: Index value of device
        idx_agent: Index value of agent

    Returns:
        List of agent indices reporting on the device

    """
    # Get data from cache
    key = ('infoset.api:db/datapoint/timefixed/{}/{}'
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
