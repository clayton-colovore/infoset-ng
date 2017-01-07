Installation
============

This section outlines how to install and do basic configuration of ``infoset-ng``.

Pre-Requisites
--------------

``infoset-ng`` has the following requirements:

* python >= 3.4
* MySQL >= 5.5
* MariaDB >= 10.0

It will not work with lower versions.

Dependencies
------------

The dependencies required for successful ``infoset-ng`` installation are
``python3`` and python's ``pip3``.

Ubuntu / Debian / Mint
~~~~~~~~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    # sudo apt-get install python3 python3-pip python3-dev python3-yaml mysql-server
    # pip3 install --user sqlalchemy yaml

Centos / Fedora
~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    # sudo dnf install python3 python3-pip python3-dev python3-yaml mysql-server
    # pip3 install --user sqlalchemy yaml

Installation
------------

Installation is simple. The first thing to do is verify that your system
is running python 3.5 or higher. If not, you will need to upgrade. Use
this command to check:

::

    $ python3 --version

Setup Database
~~~~~~~~~~~~~~

Next create the MySQL or MariaDB database. Make sure the database server is running.

::

    $ mysql -u root -p
    password:
    mysql> create database infoset_ng;
    mysql> grant all privileges on infoset_ng.* to infoset_ng@"localhost" identified by 'PASSWORD';
    mysql> flush privileges;
    mysql> exit;

**Note** Remember the value you select for ``PASSWORD``. It will be required when you edit the ``infoset-ng`` configuration file later.

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

Now clone the repository and copy the sample configuration file to its
final location.

::

    $ git clone https://github.com/PalisadoesFoundation/infoset-ng
    $ cd infoset-ng
    $ export PYTHONPATH=`pwd`


Edit Configuration File
~~~~~~~~~~~~~~~~~~~~~~~

Edit the database credential information in the server section of the ``etc/config.yaml`` file. Update the configured database ``PASSWORD`` that you saved previously.

::

    $ cp examples/etc/config.yaml etc/config.yaml
    $ vim etc/config.yaml

    main:
        db_password: PASSWORD

Run Installation Script
~~~~~~~~~~~~~~~~~~~~~~~

Run the installation script. There are two alternatives:

:Run Interactively: This is the preferred method if you don't have ``root`` access to your system. ``infoset-ng`` `will not` automatically restart on reboot using this method. To make ``infoset-ng`` run with your username, then execute this command:

::

    $ python3 setup.py

:Run as System Daemon: If you want ``infoset-ng`` to be run as a system daemon, then execute these commands. ``infoset-ng`` `will` automatically restart on reboot using this installation method. (**Note**: Do not run setup using ``sudo``. Use ``sudo`` to become the root user first)

This example assumes you have downloaded ``infoset-ng`` in the ``/home/infoset-ng`` directory. Change this to the appropiate directory in your case.

::

    $ pwd
    /home/infoset-ng
    $ sudo su -
    # cd /home/infoset-ng
    # python3 setup.py



Next Steps
----------

It is now time to review the various configuration options.
