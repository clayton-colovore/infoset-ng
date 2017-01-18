"""Initialize the API module."""

# Import PIP3 libraries
from flask import Flask

# Import configuration. This has to be done before all other infoset imports.
from infoset.utils import configuration
CONFIG = configuration.Config()

# Setup memcache. Required for all API imports
from infoset.api.common import cache
CACHE = cache.Cache(CONFIG)

# Do remaining infoset-ng importations
from infoset.api.post import POST
from infoset.api.version import VERSION

from infoset.api.resources.agents import AGENTS
from infoset.api.resources.datapoints import DATAPOINTS
from infoset.api.resources.lastcontacts import LASTCONTACTS
from infoset.api.resources.devices import DEVICES
from infoset.api.resources.deviceagents import DEVICEAGENTS


# Define the global URL prefix
API_PREFIX = '/infoset/api/v1'

# Register Blueprints
API = Flask(__name__)
API.register_blueprint(POST, url_prefix=API_PREFIX)
API.register_blueprint(VERSION, url_prefix=API_PREFIX)
API.register_blueprint(DATAPOINTS, url_prefix=API_PREFIX)
API.register_blueprint(AGENTS, url_prefix=API_PREFIX)
API.register_blueprint(LASTCONTACTS, url_prefix=API_PREFIX)
API.register_blueprint(DEVICES, url_prefix=API_PREFIX)
API.register_blueprint(DEVICEAGENTS, url_prefix=API_PREFIX)
