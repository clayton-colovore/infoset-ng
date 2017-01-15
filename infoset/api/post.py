"""infoset-ng database API. Posting Routes."""

# Standard imports
import json

# Flask imports
from flask import Blueprint, request, abort

# Infoset-ng imports
from infoset.utils import general
from infoset.api import CONFIG


# Define the POST global variable
POST = Blueprint('POST', __name__)


@POST.route('/receive/<id_agent>', methods=['POST'])
def receive(id_agent):
    """Function for handling /infoset/api/v1.0/receive/<id_agent> route.

    Args:
        id_agent: Unique Identifier of an Infoset Agent

    Returns:
        Text response of Received

    """
    # Initialize key variables
    found_count = 0

    # Read configuration
    cache_dir = CONFIG.ingest_cache_directory()

    # Get JSON from incoming agent POST
    data = request.json

    # Make sure all the important keys are available
    keys = ['timestamp', 'id_agent', 'devicename']
    for key in keys:
        if key in data:
            found_count += 1

    # Do processing
    if found_count == 3:
        # Extract key values from posting
        try:
            timestamp = int(data['timestamp'])
        except:
            abort(404)
        id_agent = data['id_agent']
        devicename = data['devicename']

        # Create a hash of the devicename
        device_hash = general.hashstring(devicename, sha=1)
        json_path = (
            '%s/%s_%s_%s.json') % (cache_dir, timestamp, id_agent, device_hash)

        with open(json_path, "w+") as temp_file:
            json.dump(data, temp_file)

        # Return
        return 'OK'

    else:
        abort(404)
