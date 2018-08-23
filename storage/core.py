#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

import json

from signal import signal, SIGINT, SIGTERM

from sys import stdout

from storage.log import Logger
from storage.settings import Command
from storage.utils import retry, FOREVER, relay_to
from storage.queues import QueueListener
from storage.db import DBListener
from storage.sensapp import Registry, RegistryListener



class MessageHandler(QueueListener, DBListener, RegistryListener):

    """
    Handle new messages coming from the message-queue
    """

    def __init__(self, ui, db, registry):
        QueueListener.__init__(self)
        DBListener.__init__(self)
        RegistryListener.__init__(self)
        self._ui = ui
        self._db = db
        self._registry = registry

        
    def new_message(self, body):
        data = json.loads(body.decode("utf-8"))
        sensor = data[0]["measurement"]
        if self._registry.knows(sensor):
            self._db.store(data)
            self._ui.data_accepted(sensor)
        else:
            self._ui.data_rejected(sensor) 

    

class Storage:

    def __init__(self, settings, ui, queue, db, registry):
        self._settings = settings
        self._ui = ui
        self._logger = Logger()
        self._registry = registry(host="registry",
                                  port=4567,
                                  listener=relay_to(self._ui, self._logger))
        self._db = db(settings.db_host,
                      settings.db_port,
                      settings.db_name,
                      relay_to(self._ui, self._logger))
        self._handler = MessageHandler(self._ui,
                                       self._db,
                                       self._registry)
        self._queue = queue(settings.queue_host,
                            settings.queue_port,
                            settings.queue_name,
                            relay_to(self._ui, self._logger, self._handler))
                            

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


    @retry(max_attempts=FOREVER, backoff=20)
    def _connect_to_database(self):
        self._db.connect()

                      
    @retry(max_attempts=FOREVER, backoff=20)
    def _connect_to_queue(self):
        self._queue.connect()


    def _ctrl_c_handler(self, signum, frame):
        self.stop()


    def stop(self):
        self._ui.goodbye()
        stdout.flush()
        exit()

