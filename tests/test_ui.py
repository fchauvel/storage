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

from io import StringIO

from storage import __version__, __copyright__, __program__, __license__
from storage.ui import UI



class UITests(TestCase):

    HOST = "my-test-host",
    PORT = 6667
    NAME = "the_thing"
    ERROR = RuntimeError("This is bad error!")

    
    def setUp(self):
        self._buffer = StringIO()
        self._ui = UI(self._buffer)
        pass


    def test_show_version(self):
        self._ui.show_version()

        self.assertEqual(self._buffer.getvalue(),
                         UI.VERSION.format(version=__version__))

    def test_greetings(self):
        self._ui.greetings()

        self._assert_buffer(UI.GREETINGS,
                            copyright=__copyright__,
                            program=__program__,
                            license=__license__,
                            version=__version__)

    def test_db_connected(self):
        self._ui.db_connected(self.HOST, self.PORT, self.NAME)

        self._assert_buffer(UI.DB_CONNECTED,
                            host=self.HOST,
                            port=self.PORT,
                            name=self.NAME);


    def test_db_connection_failed(self):
        self._ui.db_connection_failed(self.HOST, self.PORT, self.NAME, self.ERROR)

        self._assert_buffer(UI.DB_CONNECTION_FAILED,
                            host=self.HOST,
                            port=self.PORT,
                            name=self.NAME,
                            error=type(self.ERROR).__name__);

    def test_queue_connected(self):
        self._ui.queue_connected(self.HOST, self.PORT, self.NAME)

        self._assert_buffer(UI.QUEUE_CONNECTED,
                            host=self.HOST,
                            port=self.PORT,
                            name=self.NAME);

    def test_queue_connection_failed(self):
        self._ui.queue_connection_failed(self.HOST, self.PORT, self.NAME, self.ERROR)

        self._assert_buffer(UI.QUEUE_CONNECTION_FAILED,
                            host=self.HOST,
                            port=self.PORT,
                            name=self.NAME,
                            error=type(self.ERROR).__name__);

    def _assert_buffer(self, pattern, **kwargs):
        self.assertEqual(self._buffer.getvalue(),
                         pattern.format(**kwargs))
        
        
    def test_waiting_messages(self):
        self._ui.waiting_messages()

        self._assert_buffer(UI.WAITING_MESSAGES)

        
    def test_show_request(self):
        REQUEST = "This is a nice request"
        self._ui.show_request(REQUEST)

        self.assertEqual(self._buffer.getvalue(),
                         UI.REQUEST.format(body=REQUEST))

        
    def test_show_error(self):
        self._ui.show_error(self.ERROR)
        self._assert_buffer(UI.ERROR, error=self.ERROR)

        
    def test_goodbye(self):
        self._ui.goodbye()

        self.assertEqual(self._buffer.getvalue(),
                         UI.GOODBYE)
