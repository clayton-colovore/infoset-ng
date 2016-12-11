<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [About](#about)
- [Conventions](#conventions)
- [Running Tests](#running-tests)
- [Mocks](#mocks)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# About
This is the UnitTest section of the project

# Conventions
There are some conventions to be followed.

1. All files here start with the prefix `test_` that match the name of the file whose classes need to be tested.
2. All unittest methods must start with the string `test_` to be recognized by the unittest class.

# Running Tests
You can run all tests by running `make test` from the root directory

# Mocks
Many of these unittests use Python Mocks. A detailed tutorial on Mocks can be found here: http://www.drdobbs.com/testing/using-mocks-in-python/240168251
