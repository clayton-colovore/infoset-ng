"""Initialize the API module."""

# Import PIP3 libraries
from flask import Flask

# Import configuration
from infoset.utils import configuration
CONFIG = configuration.Config()

# Setup memcache
from infoset.api import cache
CACHE = cache.Cache(CONFIG)

# Do remaining infoset-ng importations
from infoset.api.db.db_data import DB_DATA
from infoset.api.db.db_agent import DB_AGENT
from infoset.api.db.db_datapoint import DB_DATAPOINT
from infoset.api.db.db_device import DB_DEVICE
from infoset.api.db.db_deviceagent import DB_DEVICEAGENT
from infoset.api.post import POST
from infoset.api.version import VERSION

# Define the global URL prefix
API_PREFIX = '/infoset/api/v1.0'

API = Flask(__name__)
API.register_blueprint(DB_DATA, url_prefix=API_PREFIX)
API.register_blueprint(DB_AGENT, url_prefix=API_PREFIX)
API.register_blueprint(DB_DATAPOINT, url_prefix=API_PREFIX)
API.register_blueprint(DB_DEVICE, url_prefix=API_PREFIX)
API.register_blueprint(DB_DEVICEAGENT, url_prefix=API_PREFIX)
API.register_blueprint(POST, url_prefix=API_PREFIX)
API.register_blueprint(VERSION, url_prefix=API_PREFIX)
