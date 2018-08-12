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
    SHOW_VERSION=0
    STORE=2


class Settings:
    """Hold the parameters given through the command line.
    """

    DEFAULT_COMMAND = Command.STORE
    DEFAULT_QUEUE = "amqp://task-queue:5672"
    DEFAULT_QUEUE_NAME = "SENSAPP_TASKS"

    def __init__(self, command, queue_address, queue_name):
        self._command = command if command is not None else self.DEFAULT_COMMAND
        self._queue_address = queue_address or self.DEFAULT_QUEUE
        self._queue_name = queue_name or self.DEFAULT_QUEUE_NAME

    @property
    def command(self):
        return self._command

    @property
    def queue_address(self):
        return self._queue_address

    @property
    def queue_name(self):
        return self._queue_name

    @staticmethod
    def from_command_line(command_line):
        parser = ArgumentParser(prog="sensapp-storage",
                                description="Stores data sent by sensors")
        parser.add_argument("-v", "--version",
                            help="show the version number",
                            action="store_const", dest="command",
                            const=Command.SHOW_VERSION)
        parser.add_argument("-n", "--queue-name",
                            help="set the name of the task queue (default: '"+ Settings.DEFAULT_QUEUE_NAME +"')")
        parser.add_argument("-q", "--task-queue",
                            help="set the URL of the source task queue (default: " + Settings.DEFAULT_QUEUE + ")")
        arguments =parser.parse_args(command_line)
        return Settings(command=arguments.command,
                        queue_address=arguments.task_queue,
                        queue_name = arguments.queue_name)

