"""Initialize the API module."""

# Import PIP3 libraries
from flask import Flask
from flask_caching import Cache

#############################################################################
# Import configuration.
# This has to be done before all other infoset imports.
#############################################################################
from infoset.utils import configuration
CONFIG = configuration.Config()
#############################################################################
#############################################################################

# Configure the cache
CACHE = Cache(config={
    'CACHE_TYPE': 'memcached',
    'CACHE_DEFAULT_TIMEOUT': CONFIG.interval()})

# Define the global URL prefix
from infoset.constants import API_PREFIX

# Import API Blueprints
from infoset.api.post import POST
from infoset.api.status import STATUS

from infoset.api.resources.agents import AGENTS
from infoset.api.resources.datapoints import DATAPOINTS
from infoset.api.resources.lastcontacts import LASTCONTACTS
from infoset.api.resources.devices import DEVICES
from infoset.api.resources.deviceagents import DEVICEAGENTS

# Setup API and intialize the cache
API = Flask(__name__)
CACHE.init_app(API)

# Register Blueprints
API.register_blueprint(POST, url_prefix=API_PREFIX)
API.register_blueprint(STATUS, url_prefix=API_PREFIX)
API.register_blueprint(DATAPOINTS, url_prefix=API_PREFIX)
API.register_blueprint(AGENTS, url_prefix=API_PREFIX)
API.register_blueprint(LASTCONTACTS, url_prefix=API_PREFIX)
API.register_blueprint(DEVICES, url_prefix=API_PREFIX)
API.register_blueprint(DEVICEAGENTS, url_prefix=API_PREFIX)
