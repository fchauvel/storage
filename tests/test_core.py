#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from unittest import TestCase

from mock import MagicMock

from threading import Thread

from storage.settings import Settings, Command
from storage.ui import UI
from storage.core import Storage

from tests.fakes import FakeQueueFactory, FakeDBFactory



class StorageTests(TestCase):

    def setUp(self):
        self._settings = Settings.defaults()
        self._ui = MagicMock(UI)
        self._queue_factory = FakeQueueFactory()
        self._db_factory = FakeDBFactory()
        self._storage = Storage(settings=self._settings,
                                ui=self._ui,
                                queue=self._queue_factory,
                                db=self._db_factory)
        self._consumer = None


    def test_calls_db_on_new_request(self):
        self._start_storage()

        self._send_request("Request 1")
        self._stop_queue()

        self._db_factory.db.store.assert_called_once_with("Request 1")


    def _start_storage(self):
        def do_start():
            self._storage.store()

        self._consumer = Thread(target=do_start)
        self._consumer.start()


    def _send_request(self, body):
        from time import sleep
        #print("Sending ", body, "...")
        sleep(1)
        self._queue_factory.queue.accept_task(body)


    def _stop_queue(self):
        self._queue_factory.queue.stop()
        self._consumer.join()
