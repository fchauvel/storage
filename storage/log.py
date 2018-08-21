#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import yaml

import logging
import logging.config

STARTING_UP = "Starting ..."
DB_CONNECTED = "Connected to DB '{name}' on {host}:{port}."
QUEUE_CONNECTED = "Connected to message-queue '{name}' on {host}:{port}."


class Logger:

    def __init__(self):
        with open("logging.yml", "r") as source:
            yamlConfig = yaml.load(source)
            logging.config.dictConfig(yamlConfig)

    def starting_up(self):
        logging.info(STARTING_UP);
            

    def db_connected(self, host, port, name):
        logging.info(DB_CONNECTED.format(host=host, port=port, name=name));


    def db_connection_failed(self, host, port, name, error):
        logging.error(str(error))

 
    def queue_connected(self, host, port, name):
        logging.info(QUEUE_CONNECTED.format(host=host, port=port, name=name));


    def queue_connection_failed(self, host, port, name, error):
        logging.error(str(error))


   
