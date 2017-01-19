"""infoset-ng database API. Datapoint table."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify, request, abort

# Infoset-ng imports
from infoset.utils import general
from infoset.db import db_datapoint
from infoset.db import db_multitable
from infoset.db import db_data
from infoset.api import CACHE, CONFIG

# Define the AGENT global variable
DATAPOINTS = Blueprint('DATAPOINTS', __name__)


@DATAPOINTS.route('/datapoints/<idx_datapoint>')
def datapoints(idx_datapoint):
    """Get datapoint data filtered by datapoint index value.

    Args:
        idx_datapoint: Datapoint index value

    Returns:
        data: JSON data for the selected agent

    """
    # Get data from cache
    key = ('DB/Datapoint/idx_datapoint/{}'.format(idx_datapoint))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_datapoint.GetIDXDatapoint(
            general.integerize(idx_datapoint))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DATAPOINTS.route('/datapoints')
def datapoints_query():
    """Get datapoint data filtered by query string values.

    Args:
        None

    Returns:
        data: JSON data for the selected agent

    """
    # Initialize key variables
    id_datapoint = request.args.get('id_datapoint')
    idx_deviceagent = request.args.get('idx_deviceagent')
    base_type = request.args.get('base_type')

    if bool(id_datapoint) is True:
        # Process id_datapoint request
        key = ('DB/Datapoint/iddatapoint/{}'.format(id_datapoint))
        cache_value = CACHE.get(key)

        # Process cache miss
        if cache_value is None:
            query = db_datapoint.GetIDDatapoint(id_datapoint)
            intermediate = query.everything()
            data = []
            data.append(intermediate)
            CACHE.set(key, data)
        else:
            data = cache_value

    elif bool(idx_deviceagent) is True:
        # Process idx_deviceagent request
        key = (
            'DB/Datapoint/idx_deviceagent/{}/base_type/{}'
            ''.format(idx_deviceagent, base_type))
        cache_value = CACHE.get(key)

        # Process cache miss
        if cache_value is None:
            data = db_datapoint.listing(
                general.integerize(idx_deviceagent), base_type=base_type)
            CACHE.set(key, data)
        else:
            data = cache_value

    else:
        abort(404)

    # Return
    return jsonify(data)


@DATAPOINTS.route('/datapoints/<int:value>/data')
def getdata(value):
    """Get Agent data from the DB by idx value.

    Args:
        value: idx_datapoint value

    Returns:
        data: JSON data for the selected agent

    """
    # Initialize key variables
    idx_datapoint = int(value)
    ts_start = general.normalized_timestamp(
        general.integerize(request.args.get('ts_start'))
        )
    ts_stop = general.normalized_timestamp(
        general.integerize(request.args.get('ts_stop'))
        )
    if ts_start > ts_stop:
        ts_start = ts_stop

    # Get data from cache
    key = (
        'DB/Data/idx_datapoint/{}/{}/{}'
        ''.format(idx_datapoint, ts_start, ts_stop))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_data.GetIDXData(CONFIG, idx_datapoint, ts_start, ts_stop)
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DATAPOINTS.route('/datapoints/all/summary')
def db_datapoint_summary():
    """Get Agent data from the DB by id_agent value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('DB/multitable/datapoints/all/summary')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_multitable.datapoint_summary()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)
