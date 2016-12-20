Operation
=========

``infoset-ng`` has two major components. These are:

1. **The Ingester**: Periodically retrieves data from the cache files
   and places it in the database.
2. **The API**: Stores and retrieves data from the database via REST API
   calls. Received data is placed in the cache directory defined in the
   configuration.

Explanations of how to permanently run each component will be given shortly, but first we'll cover how to test your installation.

Testing Operation After Installation
------------------------------------

There are a number of steps to take to make sure you have installed ``infoset-ng`` correctly. This section explains how to do basic testing before putting ``infoset-ng`` into production.

Start the API Interactively
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Start the ``infoset-ng`` API interactively. This will start an interactive session that can be stopped with a ``^C`` keystroke combination.

::

    $ bin/infoset-ng-api


Start the Ingester
~~~~~~~~~~~~~~~~~~
The ingester will need to be running prior to testing.

::

    $ bin/infoset-ng-ingester --start


Test API Functionality
~~~~~~~~~~~~~~~~~~~~~~

Now that both the API and ingester are running, it's time to test functionality by running the ``bin/tools/test_installation.py`` script

Here is an example of a successful test:

::

    $ bin/tools/test_installation.py
    2016-12-03 18:12:56,640 - infoset_console - INFO - [peter] (1054S): Successfully posted test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749
    2016-12-03 18:12:56,656 - infoset_console - INFO - [peter] (1054S): Successfully retrieved test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749

    OK

    $

Refer to the Troubleshooting section of this page to rectify any issues.

Stop After Successful Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now that it have tested the functionality successsfully it is time to stop the interactive API session and the ingester so that you can operate them as system daemons. 

::

    $ bin/infoset-ng-api
    ^C
    $ bin/infoset-ng-ingester --stop


The procedures to do operate the system daemons will be covered next.


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
