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

from sys import stdout

from storage.log import Logger
from storage.settings import Command
from storage.utils import retry
from storage.queues import QueueListener
from storage.db import DBListener



class DBHandler(DBListener):
    """
    Handle events from the database: log and forward them to the UI.
    """

    def __init__(self, ui, logger):
        self._ui = ui
        self._logger = logger
    
    def connected(self, host, port, name):
        self._logger.db_connected(host, port, name)
        self._ui.db_connected(host, port, name)

    def connection_failed(self, host, port, name, error):
        self._logger.db_connection_failed(host, port, name, error)
        self._ui.db_connection_failed(host, port, name, type(error).__name__)

    def inserted(self, data):
        pass
    
    def insertion_failed(self, data, error):
        self._ui.show_error(error)

    

class QueueHandler(QueueListener):

    """
    Handle events comming from the message queue. Log and forward them to the UI."
    """

    def __init__(self, ui, db, logger):
        self._ui = ui
        self._db = db
        self._logger = logger

    def connected(self, host, port, name):
        self._logger.queue_connected(host, port, name)
        self._ui.queue_connected(host, port, name)

    def connection_failed(self, host, port, name, error):
        self._logger.queue_connection_failed(host, port, name, error)
        self._ui.queue_connection_failed(host, port, name, type(error).__name__)

    def waiting_messages(self):
        self._ui.waiting_messages()

    def new_message(self, body):
        self._ui.show_request(body)
        self._db.store(body)

    

class Storage:

    def __init__(self, settings, ui, queue, db):
        self._settings = settings
        self._ui = ui
        self._logger = Logger()
        self._db = db(settings.db_host,
                      settings.db_port,
                      settings.db_name,
                      DBHandler(self._ui, self._logger))
        self._queue = queue(settings.queue_host,
                            settings.queue_port,
                            settings.queue_name,
                            QueueHandler(self._ui, self._db, self._logger))
                            

    def start(self):
        self._logger.starting_up()
        self._setup_signal_handlers()

        self._ui.greetings()
        
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

        
    def store(self):
        self._connect_to_database()
        self._connect_to_queue()
        self._queue.wait_messages() # Blocking call


    @retry(max_attempts=-1, backoff=20)
    def _connect_to_database(self):
        self._db.connect()

                      
    @retry(max_attempts=-1, backoff=20)
    def _connect_to_queue(self):
        self._queue.connect()


    def _ctrl_c_handler(self, signum, frame):
        self.stop()


    def stop(self):
        self._ui.goodbye()
        stdout.flush()
        exit()

