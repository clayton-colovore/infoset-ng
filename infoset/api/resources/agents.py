"""infoset-ng database API. Agent table."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify, request

# Infoset-ng imports
from infoset.db import db_agent
from infoset.utils import general
from infoset.api import CACHE

# Define the AGENTS global variable
AGENTS = Blueprint('AGENTS', __name__)


@AGENTS.route('/agents/<idx_agent>')
def agents(idx_agent):
    """Get Agent data from the DB by idx value.

    Args:
        idx_agent: Agent table idx_agent

    Returns:
        data: JSON data for the selected agent

    """
    # Get data from cache
    key = ('DB/Agent/idx_agent/{}'.format(idx_agent))
    cache_value = CACHE.get(key)

    # Process cache miss
    if cache_value is None:
        query = db_agent.GetIDXAgent(general.integerize(idx_agent))
        data = query.everything()
        CACHE.set(key, data)
    else:
        data = cache_value

    # Return
    return jsonify(data)


@AGENTS.route('/agents')
def agents_query():
    """Get Agent data from the DB by id_agent value.

    Args:
        None

    Returns:
        data: JSON data for the selected agent

    """
    # Initialize key variables
    id_agent = request.args.get('id_agent')

    if bool(id_agent) is True:
        # Process id_datapoint request
        key = ('DB/Agent/id_agent/{}'.format(id_agent))
        cache_value = CACHE.get(key)

        # Process cache miss
        if cache_value is None:
            query = db_agent.GetIDAgent(id_agent)
            data = query.everything()
            CACHE.set(key, data)
        else:
            data = cache_value
    else:
        # Process general request
        key = ('DB/Agent/id_agent')
        cache_value = CACHE.get(key)

        # Process cache miss
        if cache_value is None:
            data = db_agent.get_all_agents()
            CACHE.set(key, data)
        else:
            data = cache_value

    # Return
    return jsonify(data)
