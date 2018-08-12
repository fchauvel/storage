#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from signal import signal, SIGINT, SIGTERM

from time import sleep

from sys import stdout

from storage.utils import retry


class Storage:

    def __init__(self, settings, ui, queue_factory, db_factory):
        self._settings = settings
        self._ui = ui
        self._create_queue = queue_factory
        self._create_db = db_factory


    def start(self):
        self._setup_signal_handlers()
        self._ui.show_opening()
        self.connect_to_database()
        if self._settings.command == Command.SHOW_VERSION:
            self._ui.show_version()
        elif self._settings.command == Command.STORE:
            self.store()


    def _setup_signal_handlers(self):
        import os
        signal(SIGINT, self._ctrl_c_handler)
        signal(SIGTERM, self._ctrl_c_handler)
        if os.name == "nt":
            from signal import CTRL_C_EVENT
            signal(CTRL_C_EVENT, self._ctrl_c_handler)


    def connect_to_database(self):
        def do_connect():
            try :
                self._ui.show_connection_to(self._settings.db_host)
                self._db.connect()

            except Exception as error:
                self._ui.show_error(str(error))
                sleep(10)
                raise error

        self._db = self._create_db(self._settings.db_host,
                                   self._settings.db_port,
                                   self._settings.db_name)
        try:
            retry(do_connect, 5)
        except RuntimeError as error:
            self._ui.show_error(str(error))
            self.stop()


    def store(self):
        queue = self._create_queue(self._settings.queue_address, self._request_handler)
        self._ui.show_connection_to(self._settings.queue_address);
        queue.connect_to(self._settings.queue_name)
        self._ui.show_waiting_for_tasks()
        queue.wait_for_task() # Blocking call


    def _request_handler(self, body):
        self._ui.show_request(body)
        self._db.store(body)


    def _ctrl_c_handler(self, signum, frame):
        self.stop()


    def stop(self):
        self._ui.show_epilogue()
        stdout.flush()
        exit()

