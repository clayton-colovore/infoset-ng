Operation
=========

``infoset-ng`` has two major components. These are:

1. **The Ingester**: Periodically retrieves data from the cache files
   and places it in the database.
2. **The API**: Stores and retrieves data from the database via REST API
   calls. Received data is placed in the cache directory defined in the
   configuration.

Explanations of how run each component will be given next.

**NOTE!** You must have a valid configuration file placed in the
``etc/`` directory before activating data collection.

Ingester Operation
------------------

The ``ingester`` can be operated in one of two modes:

#.  **System Daemon**: As a system daemon which will automatically restart after a reboot.
#.  **User Daemon**: Run by a user from the CLI. The ``ingester`` will not automatically restart after a reboot.


Usage of the ``ingester`` in each mode will be discussed next.


The Ingester as a System Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is the preferred mode of operation.

The ``examples/linux/systemd`` directory has a sample ``systemd`` startup file named ``infoset-ng-ingester.service``. Follow the instructions in this file to activate and start your system ``ingester`` daemon.

The Ingester as a User Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This mode is available if you want to run the ``ingester`` in a standalone mode. The ``ingester`` can be started like this:

::

    $ bin/infoset-ng-ingester --start

The ingester can be stopped like this:

::

    $ bin/infoset-ng-ingester --stop

You can get the status of the ingester like this:

::

    $ bin/infoset-ng-ingester --status

You may want to make sure that the ingester is running correctly. This will be covered next.


API Operation
-------------
The ``API`` can be operated in one of two modes:

#.  **System Daemon**: As a system daemon which will automatically restart after a reboot.
#.  **User Process**: Run by a user from the CLI. The ``API`` will not automatically restart after a reboot.

Usage of the ``API`` in each mode will be discussed next.


The API as a System Daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is the preferred mode of operation.

The ``examples/linux/systemd`` directory has a sample ``systemd`` startup file named ``infoset-ng-api.service``. Follow the instructions in this file to activate and start your system ``ingester`` daemon.

The API as a User Process
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``infoset-ng-api`` script controls the API. The script can be started
like this:

::

    $ bin/infoset-ng-api

**Note:** There will be no visible output when this command is run. It is used primarily for quick troubleshooting. The system daemon method is preferred.

There are also examples of system startup scripts in the
``examples/linux/systemd`` and ``examples/linux/systemd`` to allow you
to run the API as a system service.
