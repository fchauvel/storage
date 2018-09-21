#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from requests import get

from storage.utils import retry, FOREVER



class RegistryListener:
    
    def registry_error(self, host, port, error):
        pass


REGISTRY_ERROR = "Registry failure! Got'{status}' from {method} {url}"
    

class Registry:

    def __init__(self, endpoint, listener):
        self._host = endpoint.hostname
        self._port = endpoint.port
        self._url = "http://{host}:{port}/sensors/".format(host=host,
                                                           port=port)
        self._listener = listener


    @retry(FOREVER, 20)
    def knows(self, sensor_id):
        try:
            _, key = sensor_id.split('_', 1)
            url = self._url + key

            response = get(url)
                          
            if response.status_code == 200:
                return True
            elif response.status_code == 204:
                return False
            else:
                raise RuntimeError(REGISTRY_ERROR.format(status=response.status_code,
                                                         url=url,
                                                         method="GET"))
        
        except Exception as error:
            self._listener.registry_error(self._host, self._port, error)
            raise error
