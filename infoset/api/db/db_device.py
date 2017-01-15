"""infoset-ng database API. Device table."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.utils import general
from infoset.db import db_device
from infoset.api import CACHE

# Define the DB_DEVICE global variable
DB_DEVICE = Blueprint('DB_DEVICE', __name__)


@DB_DEVICE.route('/db/device/getidxdevice/<value>')
def db_getidxdevice(value):
    """Get device data from the DB by idx value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/device/getidxdevice/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_device.GetIDXDevice(general.integerize(value))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)
