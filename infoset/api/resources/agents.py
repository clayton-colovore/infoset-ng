"""infoset-ng database API. Agent table."""

# Standard imports

# Flask imports
from flask import Blueprint, jsonify, request

# Infoset-ng imports
from infoset.db import db_agent
from infoset.utils import general
from infoset.utils import memory
from infoset.api import CACHE

# Define the AGENTS global variable
AGENTS = Blueprint('AGENTS', __name__)


@AGENTS.route('/agents/<idx_agent>')
@CACHE.cached(key_prefix=memory.flask_cache_key)
def agents(idx_agent):
    """Get Agent data from the DB by idx value.

    Args:
        idx_agent: Agent table idx_agent

    Returns:
        data: JSON data for the selected agent

    """
    # Get data
    query = db_agent.GetIDXAgent(general.integerize(idx_agent))
    data = query.everything()

    # Return
    return jsonify(data)


@AGENTS.route('/agents')
@CACHE.cached(key_prefix=memory.flask_cache_key)
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
        query = db_agent.GetIDAgent(id_agent)
        data = [query.everything()]
    else:
        data = db_agent.get_all_agents()

    # Return
    return jsonify(data)
