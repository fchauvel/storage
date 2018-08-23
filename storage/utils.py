#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import logging

import sys

from time import sleep



FOREVER = -1

RETRY_LOG = "Retrying action '{}' in {} seconds ({} / {})"


def retry(max_attempts, backoff):

    def wrap(action):

        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts or max_attempts < 0:
                attempt += 1
                try:
                    return action(*args, **kwargs)
                except:
                    logging.error(sys.exc_info()[0])
                    logging.info(RETRY_LOG.format(action.__name__, backoff, attempt, max_attempts))
                    sleep(backoff)
                
            raise RuntimeError("All %d attempts failed!" % max_attempts)

        return wrapper
    
    return wrap




def relay_to(*listeners):
    return Relay(*listeners)


class Relay:

    def __init__(self, *listeners):
        self._listeners = listeners


    def __getattr__(self, name):

        candidates = []
        for each_listener in self._listeners:
            if hasattr(each_listener, name) and callable(getattr(each_listener, name)):
                candidates.append(each_listener)
        
        def relay(*args, **kwargs):
            for each_listener in candidates:
                method = getattr(each_listener, name)
                method(*args, **kwargs)
                
        if candidates:
            return relay
        
        raise AttributeError("None of the listeners have attribute '%s'!" % name)
                    

                    


