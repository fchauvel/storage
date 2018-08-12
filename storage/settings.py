#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

from argparse import ArgumentParser


class Command:
    SHOW_VERSION=1
    STORE=2


class Settings:
    """Hold the parameters given through the command line.
    """

    DEFAULT_COMMAND = Command.STORE
    DEFAULT_QUEUE_HOST = "task-queue"
    DEFAULT_QUEUE_PORT = "5672"
    DEFAULT_QUEUE_NAME = "SENSAPP_TASKS"
    DEFAULT_DB_HOST = "storage-db"
    DEFAULT_DB_PORT = "8086"
    DEFAULT_DB_NAME = "sensapp"

    HELP_VERSION = "show the version number and exit"
    HELP_QUEUE_HOST = "set the host name of the message queue (default: " + DEFAULT_QUEUE_HOST + ")"
    HELP_QUEUE_NAME = "set the name of the message queue (default: " + DEFAULT_QUEUE_NAME + ")"
    HELP_QUEUE_PORT = "set the port of the message queue (default: " + DEFAULT_QUEUE_PORT + ")"
    HELP_DB_HOST = "set the host name of the database (default: " + DEFAULT_DB_HOST + ")"
    HELP_DB_PORT = "set the port of the database (default: " + DEFAULT_DB_PORT + ")"
    HELP_DB_NAME = "set the name of the database (default: " + DEFAULT_DB_NAME + ")"
    
    def __init__(self, **kwargs):
        self._command = kwargs["command"] or  self.DEFAULT_COMMAND
        self._queue_address = kwargs["queue_host"] or self.DEFAULT_QUEUE_HOST
        self._queue_port = kwargs["queue_port"] or self.DEFAULT_QUEUE_PORT
        self._queue_name = kwargs["queue_name"] or self.DEFAULT_QUEUE_NAME
        self._db_host = kwargs["db_host"] or self.DEFAULT_DB_HOST
        self._db_port = kwargs["db_port"] or self.DEFAULT_DB_PORT
        self._db_name = kwargs["db_name"] or self.DEFAULT_DB_NAME
        
    @property
    def command(self):
        return self._command

    @property
    def queue_address(self):
        return self._queue_address

    @property
    def queue_port(self):
        return int(self._queue_port)
    
    @property
    def queue_name(self):
        return self._queue_name

    @property
    def db_host(self):
        return self._db_host

    @property
    def db_port(self):
        return int(self._db_port)

    @property
    def db_name(self):
        return self._db_name

    @staticmethod
    def from_command_line(command_line):
        parser = ArgumentParser(prog="sensapp-storage",
                                description="Stores data sent by sensors")
        parser.add_argument("-v", "--version", help=Settings.HELP_VERSION,
                            action="store_const", dest="command", const=Command.SHOW_VERSION)
        parser.add_argument("-q", "--queue-host", help= Settings.HELP_QUEUE_HOST)
        parser.add_argument("-p", "--queue-port", help= Settings.HELP_QUEUE_PORT)
        parser.add_argument("-n", "--queue-name", help= Settings.HELP_QUEUE_NAME)
        parser.add_argument("-o", "--db-host", help=Settings.HELP_DB_HOST)
        parser.add_argument("-r", "--db-port", help=Settings.HELP_DB_PORT)
        parser.add_argument("-m", "--db-name", help=Settings.HELP_DB_NAME)
        arguments = parser.parse_args(command_line)
        return Settings(**vars(arguments))

    @staticmethod
    def defaults():
        return Settings(command=Command.STORE,
                        queue_host=None,
                        queue_port=None,
                        queue_name=None,
                        db_host=None,
                        db_port=None,
                        db_name=None)
