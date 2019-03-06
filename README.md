[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77ca19b7e1d540269f63879e5fc33ed8)](https://app.codacy.com/app/fchauvel/storage?utm_source=github.com&utm_medium=referral&utm_content=fchauvel/storage&utm_campaign=Badge_Grade_Settings)
[![Build Status](https://travis-ci.org/fchauvel/storage.svg?branch=master)](https://travis-ci.org/fchauvel/storage)
[![Test Coverage](https://img.shields.io/codecov/c/github/fchauvel/storage.svg)](https://codecov.io/gh/fchauvel/storage)
![GitHub tag](https://img.shields.io/github/tag/fchauvel/storage.svg)


# SensApp::Storage

This SensApp's storage, the service that persists data received from
the sensors.


# Installation

This is a Python 3 application. To install it, run the followings
commands (assuming you are running a Linux-like OS):

	$> git clone git@github.com:fchauvel/storage.git
	$> cd storage
	$> pip install .

Note that if you want to develop or modify the code, you may want to
install it using the `-e` option of pip, as:

	$> pip install -e .

# Testing

SensApp Storage comes with a test suite that checks its basic
functionalities. You can run it with the following commands:

	$> python setup.py test

Alternatively, you can run a specific test suite using

	$> python setup.py test -s tests.test_settings

# Usage

SensApp::Storage is a simple command-line program that you start as
follows:

	$> $ sensapp-storage -q localhost
	SensApp::Storage -- v0.0.0 (MIT)
	Copyright (C) 2018 SINTEF

	Contacting 'localhost' ...
	Waiting for tasks (Ctrl+C to exit) ...
	New request: b'Au revoir les amis'

	That's all folks

You can configure several options through the command line, as explain
in the help:

	$> sensapp-storage --help
	usage: sensapp-storage [-h] [-v] [-q QUEUE_HOST] [-p QUEUE_PORT] [-n QUEUE_NAME] [-o DB_HOST]
						   [-r DB_PORT] [-m DB_NAME]

	Stores data sent by sensors

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --version         show the version number and exit
	  -q QUEUE_HOST, --queue-host QUEUE_HOST
							set the host name of the message queue (default: task-queue)
	  -p QUEUE_PORT, --queue-port QUEUE_PORT
							set the port of the message queue (default: 5672)
	  -n QUEUE_NAME, --queue-name QUEUE_NAME
							set the name of the message queue (default: SENSAPP_TASKS)
	  -o DB_HOST, --db-host DB_HOST
							set the host name of the database (default: storage-db)
	  -r DB_PORT, --db-port DB_PORT
							set the port of the database (default: 8086)
	  -m DB_NAME, --db-name DB_NAME
							set the name of the database (default: sensapp)

# Change Log

  * v0.2.1
	* Fix issue with failing int convertion when no arguments were given (on registry port)
