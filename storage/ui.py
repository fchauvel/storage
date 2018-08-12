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
    OPENING = ("{program} -- v{version} ({license})\n"
               "{copyright}\n\n")
    CONNECTION = "Contacting '{address}' ...\n"
    WAITING_FOR_TASKS = "Waiting for tasks (Ctrl+C to exit) ...\n"
    REQUEST = "New request: {body}\n"
    EPILOGUE = "That's all folks!\n"

    ERROR = " /!\ Error: {error}\n"
    
    def __init__(self, output):
        self._output = output


    def show_version(self):
        self._print(self.VERSION, version=__version__)

    def show_opening(self):
        self._print(self.OPENING,
                    version=__version__,
                    copyright=__copyright__,
                    program=__program__,
                    license=__license__)

    def show_connection_to(self, address):
        self._print(self.CONNECTION, address=address);

    def show_waiting_for_tasks(self):
        self._print(self.WAITING_FOR_TASKS)

    def show_request(self, body):
        self._print(self.REQUEST, body=body)

    def show_error(self, error):
        self._print(self.ERROR, error=error)
        
    def show_epilogue(self):
        self._print(self.EPILOGUE)
        
    def _print(self, text, **values):
        self._output.write(text.format(**values))
