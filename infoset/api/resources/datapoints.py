"""infoset-ng database API. Datapoint table."""

# Standard imports
from datetime import datetime

# Flask imports
from flask import Blueprint, jsonify, request, abort

# Infoset-ng imports
from infoset.utils import general
from infoset.utils import memory
from infoset.db import db_datapoint
from infoset.db import db_multitable
from infoset.db import db_data
from infoset.api import CACHE, CONFIG

# Define the AGENT global variable
DATAPOINTS = Blueprint('DATAPOINTS', __name__)


@DATAPOINTS.route('/datapoints/<idx_datapoint>')
@CACHE.cached(key_prefix=memory.flask_cache_key)
def datapoints(idx_datapoint):
    """Get datapoint data filtered by datapoint index value.

    Args:
        idx_datapoint: Datapoint index value

    Returns:
        data: JSON data for the selected agent

    """
    # Get data
    query = db_datapoint.GetIDXDatapoint(general.integerize(idx_datapoint))
    data = query.everything()

    # Return
    return jsonify(data)


@DATAPOINTS.route('/datapoints')
@CACHE.cached(key_prefix=memory.flask_cache_key)
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
        query = db_datapoint.GetIDDatapoint(id_datapoint)
        intermediate = query.everything()
        data = []
        data.append(intermediate)

    elif bool(idx_deviceagent) is True:
        data = db_datapoint.listing(
            general.integerize(idx_deviceagent), base_type=base_type)

    else:
        abort(404)

    # Return
    return jsonify(data)


@DATAPOINTS.route('/datapoints/<int:value>/data')
@CACHE.cached(key_prefix=memory.flask_cache_key)
def getdata(value):
    """Get Agent data from the DB by idx value.

    Args:
        value: idx_datapoint value

    Returns:
        data: JSON data for the selected agent

    """
    # Initialize key variables
    idx_datapoint = int(value)
    secondsago = general.integerize(request.args.get('secondsago'))
    ts_stop = general.integerize(request.args.get('ts_start'))
    ts_start = general.integerize(request.args.get('ts_start'))

    # Process start and stop times
    if bool(secondsago) is True:
        ts_stop = int(datetime.utcnow().timestamp())
        ts_start = ts_stop - abs(secondsago)
    else:
        if bool(ts_start) is True and bool(ts_stop) is True:
            ts_start = abs(general.normalized_timestamp(
                general.integerize(request.args.get('ts_start'))
                ))
            ts_stop = abs(general.normalized_timestamp(
                general.integerize(request.args.get('ts_stop'))
                ))
        else:
            abort(404)

    # Fix start and stop times
    if ts_start > ts_stop:
        ts_start = ts_stop

    # Fail if more than a year of data is being requested
    if ts_stop - ts_start >= 31536000:
        abort(404)

    # Get data
    query = db_data.GetIDXData(CONFIG, idx_datapoint, ts_start, ts_stop)
    data = query.everything()

    # Return
    return jsonify(data)


@DATAPOINTS.route('/datapoints/all/summary')
@CACHE.cached(key_prefix=memory.flask_cache_key)
def db_datapoint_summary():
    """Get Agent data from the DB by id_agent value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data
    data = db_multitable.datapoint_summary()

    # Return
    return jsonify(data)


@DATAPOINTS.route('/datapoints/all/summarylist')
@CACHE.cached(key_prefix=memory.flask_cache_key)
def db_datapoint_summary_list():
    """Get Datapoint summary data from the DB as a list of dicts.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data
    data = db_multitable.datapoint_summary_list()

    # Return
    return jsonify(data)
