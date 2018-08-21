#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


from storage import __version__, __program__, __copyright__, __license__


class UI:

    
    VERSION = "{version}\n"

    GREETINGS = ("{program} -- v{version} ({license})\n"
                 "{copyright}\n\n")

    DB_CONNECTED = "Connected to DB '{name}' on {host}:{port}.\n"

    DB_CONNECTION_FAILED = ("/!\ Cannot connect to DB '{name}' on {host}:{port}! ({error})\n"
                            "    Check log file for details.\n\n")
    
    QUEUE_CONNECTED = "Connected to message-queue '{name}' on {host}:{port}.\n"

    QUEUE_CONNECTION_FAILED = ("/!\ Cannot connect to message-queue '{name}' on {host}:{port}! ({error})\n"
                               "    Check log file for details.\n\n")

    
    CONNECTION = "Contacting '{address}' ...\n"

    WAITING_MESSAGES = "Waiting for messages (Ctrl+C to exit) ...\n"

    REQUEST = "New request: {body}\n"

    GOODBYE = "That's all folks!\n"

    ERROR = " /!\ Error: {error}\n"

    
    def __init__(self, output):
        self._output = output


    def show_version(self):
        self._print(self.VERSION, version=__version__)

    def greetings(self):
        self._print(self.GREETINGS,
                    version=__version__,
                    copyright=__copyright__,
                    program=__program__,
                    license=__license__)

    def db_connected(self, host, port, name):
        self._print(self.DB_CONNECTED, port=port, host=host, name=name)

    def db_connection_failed(self, host, port, name, error):
        self._print(self.DB_CONNECTION_FAILED,
                    port=port,
                    host=host,
                    name=name,
                    error=error)

    def queue_connected(self, host, port, name):
        self._print(self.QUEUE_CONNECTED, port=port, host=host, name=name)

    def queue_connection_failed(self, host, port, name, error):
        self._print(self.QUEUE_CONNECTION_FAILED,
                    port=port,
                    host=host,
                    name=name,
                    error=error)

    def waiting_messages(self):
        self._print(self.WAITING_MESSAGES)

    def show_request(self, body):
        self._print(self.REQUEST, body=body)

    def show_error(self, error):
        self._print(self.ERROR, error=error)
        
    def goodbye(self):
        self._print(self.GOODBYE)
        
    def _print(self, text, **values):
        self._output.write(text.format(**values))
