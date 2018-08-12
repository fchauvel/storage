# SensApp::Storage 

This SensApp's storage, the service that persists data received from
the sensors.


# Installation & Usage

This is a Python 3 application. To install it, run the followings
commands (assuming you are running a Linux-like OS):

	$> git clone git@github.com:SINTEF-9012/arcadia-mock.git
	$> cd arcadiamock
	$> pip install .
	$> arcadiamock
	
Note that if you want to develop or modify the code, you may want to
install it using the `-e` option of pip, as:
	
	$> pip install -e .

# Testing

SensApp Storage comes with a test suite that checks its basic
functionalities. You can run it with the following commands:

	$> python setup.py test

