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

    def setUp(self):
        self._buffer = StringIO()
        self._ui = UI(self._buffer)
        pass


    def test_show_version(self):
        self._ui.show_version()

        self.assertEqual(self._buffer.getvalue(),
                         UI.VERSION.format(version=__version__))

    def test_show_opening(self):
        self._ui.show_opening()

        self.assertEqual(self._buffer.getvalue(),
                         UI.OPENING.format(copyright=__copyright__,
                                           program=__program__,
                                           license=__license__,
                                           version=__version__))

    def test_show_connection(self):
        ADDRESS = "amqp://my-queue:5672"

        self._ui.show_connection_to(ADDRESS)

        self.assertEqual(self._buffer.getvalue(),
                         UI.CONNECTION.format(address=ADDRESS));

    def test_show_waiting(self):
        self._ui.show_waiting_for_tasks()

        self.assertEqual(self._buffer.getvalue(),
                         UI.WAITING_FOR_TASKS)

    def test_show_request(self):
        REQUEST = "This is a nice request"
        self._ui.show_request(REQUEST)

        self.assertEqual(self._buffer.getvalue(),
                         UI.REQUEST.format(body=REQUEST))

    def test_show_error(self):
        ERROR = "UNknown error"
        self._ui.show_error(ERROR)
        self.assertEqual(self._buffer.getvalue(),
                         UI.ERROR.format(error=ERROR))

    def test_show_epilogue(self):
        self._ui.show_epilogue()

        self.assertEqual(self._buffer.getvalue(),
                         UI.EPILOGUE)
