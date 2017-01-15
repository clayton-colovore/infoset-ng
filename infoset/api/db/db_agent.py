"""infoset-ng database API. Agent table."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify

# Infoset-ng imports
from infoset.db import db_agent
from infoset.utils import general
from infoset.api import CACHE

# Define the DB_AGENT global variable
DB_AGENT = Blueprint('DB_AGENT', __name__)


@DB_AGENT.route('/db/agent/getidxagent/<value>')
def db_getidxagent(value):
    """Get Agent data from the DB by idx value.

    Args:
        None

    Returns:
        data: JSON data for the selected agent

    """
    # Get data from cache
    key = ('infoset.api.api:db/agent/getidxagent/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_agent.GetIDXAgent(general.integerize(value))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DB_AGENT.route('/db/agent/getidagent/<value>')
def db_agent_getid_agent(value):
    """Get Agent data from the DB by id_agent value.

    Args:
        None

    Returns:
        Home Page

    """
    # Get data from cache
    key = ('infoset.api.api:db/agent/getidagent/{}'.format(value))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_agent.GetIDAgent(value)
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@DB_AGENT.route('/db/agent/getallagents')
def db_agent_get_all_agents():
    """Get all agent data from the DB.

    Args:
        None

    Returns:
        Agent data

    """
    # Get data from cache
    key = ('infoset.api.api:db/agent/getallagents')
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        data = db_agent.get_all_agents()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)
