"""infoset-ng database API. Multi-table queries."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.db import db_multitable
from infoset.api import CACHE

# Define the DB_MUTLTITABLE global variable
DB_MUTLTITABLE = Blueprint('DB_MUTLTITABLE', __name__)


@DB_MUTLTITABLE.route('/db/multitable/datapoint_summary_list')
def db_datapoint_summary_list():
    """Get Agent data from the DB by idx value.

    Args:
        None

    Returns:
        data: JSON data for the selected agent

    """
    # Get data from cache
    key = ('infoset.api.api:db/multitable/datapoint_summary_list')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_multitable.datapoint_summary_list()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DB_MUTLTITABLE.route('/db/multitable/datapoint_summary')
def db_datapoint_summary():
    """Get Agent data from the DB by id_agent value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/multitable/datapoint_summary')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_multitable.datapoint_summary()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)
