#!/usr/bin/env python

#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from sys import argv, stdout

from signal import signal, SIGINT, SIGTERM

from storage.settings import Settings, Command
from storage.ui import UI
from storage.task_queue import RabbitMQ




class Storage:

    SENSAPP_QUEUE = "SENSAPP_TASK_QUEUE"
    
    def __init__(self, settings, ui):
        self._settings = settings
        self._ui = ui

        
    def start(self):
        self._setup_signal_handlers()
        if self._settings.command == Command.SHOW_VERSION:
            self._ui.show_version()
        elif self._settings.command == Command.STORE:
            self.store()

            
    def _setup_signal_handlers(self):
        import os
        signal(SIGINT, self.stop)
        signal(SIGTERM, self.stop)
        if os.name == "nt":
            from signal import CTRL_C_EVENT
            signal(CTRL_C_EVENT, self.stop)

            
    def store(self):
        self._ui.show_opening()
        queue = RabbitMQ(self._settings.queue_address, self._request_handler)
        self._ui.show_connection_to(self._settings.queue_address);
        queue.connect_to(self.SENSAPP_QUEUE)
        self._ui.show_waiting()
        queue.consume()

        
    def _request_handler(self, body):
        self._ui.show_request(body)

        
    def stop(self, signum, frame):
        self._ui.show_epilogue()
        stdout.flush()
        exit()


def main():
    settings = Settings.from_command_line(argv[1:])
    storage = Storage(settings, UI(stdout))
    storage.start()
    

    
