Installation and Configuration
==============================

This section outlines how to install and configure ``infoset-ng``.

Dependencies
------------

The dependencies required for successful ``infoset-ng`` installation are
``python3`` and python's ``pip3``.

Ubuntu / Debian / Mint
~~~~~~~~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    # sudo apt-get install python3 python3-pip python3-dev python3-yaml
    # pip3 install --user sqlalchemy

Fedora
~~~~~~

The commands for installing the dependencies are:

::

    # sudo dnf install python3 python3-pip python3-dev python3-yaml
    # pip3 install --user sqlalchemy

Installation
------------

Installation is simple. The first thing to do is verify that your system
is running python 3.5 or higher. If not, you will need to upgrade. Use
this command to check:

::

    $ python3 --version

Next create the MySQL or MariaDB database.

::

    $ mysql -u root -p
    password:
    mysql> create database infoset-ng;
    mysql> grant all privileges on infoset-ng.* to infoset-ng@"localhost" identified by 'PASSWORD';
    mysql> flush privileges;
    mysql> exit;

Now clone the repository and copy the sample configuration file to its
final location.

::

    $ git clone https://github.com/PalisadoesFoundation/infoset-ng
    $ cd infoset-ng
    $ export PYTHONPATH=`pwd`
    $ cp examples/etc/* etc/

Edit the database credential information in the server section of the
``etc/config.yaml`` file. Update the configured database password.

::

    $ vim etc/config.yaml

Create the directories that ``infoset-ng`` will use for its working
files.

::

    $ sudo mkdir -p /opt/infoset-ng
    $ sudo chown -R $USER /opt/infoset-ng
    $ mkdir -p /opt/infoset-ng/log
    $ mkdir -p /opt/infoset-ng/cache

Run the install scripts.

::

    $ pip3 install --user sqlalchemy
    $ python3 setup.py
    $ source ~/.bashrc
    $ sudo make
    $ source venv/bin/activate
    $ sudo make install

Start the ``infoset-ng`` API.

::

    $ ./server.py

Testing Installation
~~~~~~~~~~~~~~~~~~~~

It is important to have a valid configuration file in the ``etc/``
directory before starting data collection. See the ``Configuration``
section of this document.

You can test whether your configuration works by:

1. Starting the API (Important, see the ``Operation`` section of this
   document)
2. Running the ``bin/tools/test_installation.py`` script

Here is an example of a successful test:

::

    $ bin/tools/test_installation.py
    2016-12-03 18:12:56,640 - infoset_console - INFO - [peter] (1054S): Successfully posted test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749
    2016-12-03 18:12:56,656 - infoset_console - INFO - [peter] (1054S): Successfully retrieved test data for agent ID 558bb0055d7b4299c2ebe6abcc53de64a9ec4847b3f82238b3682cad575c7749

    OK

    $