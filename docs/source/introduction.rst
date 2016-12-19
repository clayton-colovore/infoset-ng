Introduction
============

``infoset-ng`` is a lightweight Python 3 based REST API that stores
and/or retrieves timestamped data. It runs on Linux.

We strongly recommend that you read everything on this page before
installing ``infoset-ng`` **Table of Contents**

Features
--------

``infoset-ng`` has the following features:

1.  Open source.
2.  Written in python, a modern language.
3.  Easy configuration.
4.  Uses the well known Flask webserver for accepting data and
    responding to requests.
5.  ``infoset-ng`` has a number of fault tolerant features aimed at
    making it resilient in unstable computing environemnts.
6.  MariaDB / MySQL database backend
7.  Database connection pooling to reduce database load.
8.  Ingestion of data supports parallel multiprocessing for maximum
    speed.
9.  The infoset-ng-ng API server can tolerate the loss of communication
    with its database by caching the data locally until the database
    returns online.
10. The ``infoset-ng`` configuration is entirely stored in files. This
    allows it to collect data in the absense of a database, such as
    during maintenance or an outage.
11. Backups are simple. Just save the entire contents of the
    ``infoset-ng`` directory tree including hidden files, and save a
    copy of the database for your performance data.

We are always looking for more contributors!

Inspiration / History
---------------------

The ``infoset-ng`` project originally took inspiration from the
SourceForge based ``switchmap`` project. ``switchmap`` was written in
PERL and designed to create tabular representations of network
topologies. Early versions of ``infoset`` eventually had expanded
features which included the polling of network devices for real time
performance data. This data was presented via a web interface. The code
became cumbersome and the original ``infoset`` was split into three
componet parts.

1. ``infoset-ng``: An API for storing and retrieving real time data.
2. ``garnet``: A network / server performance charting web application
   that uses various types of agents for collecting real time data.
   ``garnet`` uses ``infoset-ng`` to store its data.
3. ``switchmap-ng`` A python 3 based feature equivalent version of
   ``switchmap``.

Each of these projects resides on the University of the West Indies
Computing Society's GitHub account.

Oversight
---------

``infoset-ng`` is a student collaboration between:

1. The University of the West Indies Computing Society. (Kingston,
   Jamaica)
2. The University of Techology, IEEE Student Branch. (Kingston, Jamaica)
3. The Palisadoes Foundation http://www.palisadoes.org

And many others.
