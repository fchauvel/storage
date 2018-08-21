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

from influxdb import InfluxDBClient



class DataStoreFactories:

    @staticmethod
    def influxDB(host, port, name, listener):
        return InfluxDB(host, port, name, listener)



class DataStore:

    def connect(self):
        pass


    def store(self, data):
        pass


    
class DBListener:

    def db_connected(self, host, port, name):
        pass

    def db_connection_failed(self, host, port, name, error):
        pass

    def db_inserted(self, data):
        pass
    
    def db_insertion_failed(self, data, error):
        pass



class InfluxDB(DataStore):


    def __init__(self, host, port, name, listener):
        self._host = host
        self._port = port
        self._name = name
        self._listener = listener
        self._client = None


    def connect(self):
        try:
            self._client = InfluxDBClient(host=self._host, port=self._port)
            databases = self._client.get_list_database()
            if not any(db["name"] == self._name for db in databases):
                self._client.create_database(self._name)
            self._client.switch_database(self._name)
            self._listener.db_connected(self._host, self._port, self._name)
            
        except Exception as error:
            self._listener.db_connection_failed(self._host, self._port, self._name, error)
            raise


    def store(self, text):
        data = json.loads(text.decode("utf-8"))
        try:
            self._client.write_points(data)
            self._listener.db_inserted(data)

        except Exception as error:
            self._listener.db_insertion_error(data, error)
            raise error
