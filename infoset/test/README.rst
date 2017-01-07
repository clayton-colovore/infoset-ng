About Unittests
===============


This is the UnitTest section of the project. All modifications to code
must have an associated functional unittest to reduce the risk of bugs.


Conventions
-----------

There are some conventions to be followed.

1. All files here start with the prefix ``test_`` that match the name of
   the file in a module whose classes, methods and functions need to be
   tested.
2. All unittest methods must start with the string ``test_`` to be
   recognized by the unittest class.
3. All unittest scripts must be able to successfully run independently
   of all others.
4. Database tests must:
5. Only be able to run on a database whose name begins with the string
   ``test_``. This is because database tests may be desctructive.
6. Create the required initial database state for tests to run
   correctly.

Prequisites
-----------

You will need to create a test database named ``test_infoset`` with a username ``travis`` prior to testing. The SQL commands to this are:

::

    create database test_infoset;
    grant all privileges on test_infoset.* to travis@"localhost" identified by password '';
    flush privileges;

This is an important step. Our unittests are run automatically with each pull request. These names, and passwords need to be maintained.

Running Tests
-------------

There are some important things to know beforehand.

1. Run the ``infoset/test/create_test_config.py`` script once before running the unittests. This will create a temporary test configuration in a directory referenced by the system environment variable ``INFOSET_CONFIGDIR``. The script will tell you how to set this correctly.
2. You can run all tests by running ``_do_all_tests.py`` from the
   ``infoset/test`` directory
3. The database tests are destructive. You will need to create a
   separate ``infoset-ng`` database to run the tests. The database name
   ``test_infoset`` must be used.


Mocks
-----

Many of these unittests use Python Mocks. A detailed tutorial on Mocks
can be found here:
http://www.drdobbs.com/testing/using-mocks-in-python/240168251
