#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from influxdb import InfluxDBClient



class DataStoreFactories:

    @staticmethod
    def influxDB(host, port, name):
        return InfluxDB(host, port, name)



class DataStore:

    def connect(self):
        pass


    def store(self, data):
        pass



class InfluxDB(DataStore):


    def __init__(self, host, port, name):
        self._host = host
        self._port = port
        self._name = name
        self._client = None


    def connect(self):
        self._client = InfluxDBClient(host=self._host, port=self._port)
        databases = self._client.get_list_database()
        if not any(db[name] == self._name for db in databases):
            self._client.create_database(self._name)
        client.switch_database(self._name)


    def store(self, data):
        self._client.write_points(data)
