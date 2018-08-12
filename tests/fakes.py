#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from threading import Thread, Event

from mock import MagicMock

from storage.db import DataStore



class FakeQueue:
    """
    Let a third party trigger the reception of requests
    """

    def __init__(self, queue_address, callback):
        self._callback = callback
        self._request_data = None
        self._new_request = Event()
        self._stop = Event()

    def connect_to(self, queue_name):
        pass

    def wait_for_task(self):
        while not self._stop.is_set():
            # print("Waiting for requests ...")
            self._new_request.wait(timeout=5)
            if self._new_request.is_set():
                self._callback(self._request_body)
                self._new_request.clear()


    def accept_task(self, body):
        self._request_body = body
        self._new_request.set()


    def stop(self):
        self._stop.set()



class FakeQueueFactory:
    """
    Memorize and expose the queue it has built.
    """

    def __init__(self):
        self._queue = None

    def __call__(self, queue_address, callback):
        self._queue = FakeQueue(queue_address, callback)
        return self._queue

    @property
    def queue(self):
        return self._queue



class FakeDBFactory:

    def __init__(self):
        self._db = None

    def __call__(self):
        self._db = MagicMock(DataStore)
        return self._db

    @property
    def db(self):
        return self._db
