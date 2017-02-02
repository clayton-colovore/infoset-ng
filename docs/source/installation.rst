Installation
============

This section outlines how to install and do basic configuration of ``infoset-ng``.

Dependencies
------------

``infoset-ng`` has the following requirements:

* python >= 3.5
* python3-pip
* MySQL >= 5.7 OR MariaDB >= 10.0

It will not work with lower versions.

Ubuntu / Debian / Mint
~~~~~~~~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    $ sudo apt-get -y install python3 python3-pip python3-dev memcached

Select either of these commands to install MySQL server or MariaDB server 

::

    $ sudo apt-get -y install mysql-server
    $ sudo apt-get -y install mariadb-server
    

Centos / Fedora
~~~~~~~~~~~~~~~

The commands for installing the dependencies are:

::

    $ sudo dnf -y install python3 python3-pip python3-dev memcached

Select either of these commands to install MySQL server or MariaDB server 

::

    $ sudo dnf -y install mysql-server
    $ sudo dnf -y install mariadb-server

Installation
------------

Installation is simple. Follow these steps

Verify Dependencies
~~~~~~~~~~~~~~~~~~~

The first thing to do is verify that your system has the correct prerequisites. Run this command to make sure all is OK:

::

    $ pip3 install --user setuptools
    $ bin/tools/prerequisites.py

Do the appropriate remediation to fix any reported issues. Run any commands this script suggests.

Be prepared to install ``infoset-ng`` on a newer version of your operating system.

Setup the Database
~~~~~~~~~~~~~~~~~~

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
