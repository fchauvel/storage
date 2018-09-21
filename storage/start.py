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

from storage.settings import Arguments, Settings, Command
from storage.ui import UI
from storage.queues import QueueFactories
from storage.core import Storage
from storage.db import DataStoreFactories
from storage.sensapp import Registry



def main():
    arguments = Arguments.from_command_line(argv[1:])

    settings = Settings.from_arguments(arguments)
    
    
    storage = Storage(settings,
                      UI(stdout),
                      QueueFactories.rabbitMQ,
                      DataStoreFactories.influxDB,
                      Registry)

    storage.start(arguments.command)
