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
	usage: sensapp-storage [-h] [-v] [-n QUEUE_NAME] [-q TASK_QUEUE]

	Stores data sent by sensors
	
	optional arguments:
	  -h, --help            show this help message and exit
      -v, --version         show the version number
      -n QUEUE_NAME, --queue-name QUEUE_NAME
                            set the name of the task queue (default: 'SENSAPP_TASKS')
      -q TASK_QUEUE, --task-queue TASK_QUEUE
                            set the URL of the source task queue (default: amqp://task-queue:5672)
							
							
