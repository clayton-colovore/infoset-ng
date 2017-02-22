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

Installation is simple. There are three basic steps.


1. Clone the Repository
2. Setup the Database
3. Run the Installation Script

This will now be explained in more detail.


Clone the Repository
~~~~~~~~~~~~~~~~~~~~

Now clone the repository and copy the sample configuration file to its
final location.

::

    $ git clone https://github.com/PalisadoesFoundation/infoset-ng
    $ cd infoset-ng


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


Run Installation Script
~~~~~~~~~~~~~~~~~~~~~~~

Run this command and follow the prompts.

::

    $ bin/infoset-ng-cli install


**Note** The setup script will make ``infoset-ng`` to be a system daemon if it is run as the ``root`` user (`System Daemon Mode`). If it is not run as root you will have to manually start the ``infoset-ng`` processes after each reboot. (`Interactive Mode`)


Next Steps
----------

It is now time to review the various configuration options.
