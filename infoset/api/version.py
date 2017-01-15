"""infoset-ng database API. Get Version."""

# Flask imports
from flask import Blueprint

# Define the VERSION global variable
VERSION = Blueprint('VERSION', __name__)


@VERSION.route('/')
def index():
    """Function for handling home route.

    Args:
        None

    Returns:
        Home Page

    """
    # Return
    return 'Infoset API v1.0 Operational.\n'
