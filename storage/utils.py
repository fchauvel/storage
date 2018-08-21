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

from time import sleep


RETRY_LOG = "Retying in {} seconds ({} / {})"


def retry(max_attempts, backoff):

    def wrap(action):

        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts or max_attempts < 0:
                attempt += 1
                try:
                    return action(*args, **kwargs)
                except Exception as error:
                    logging.info(RETRY_LOG.format(backoff, attempt, max_attempts))
                    sleep(backoff)
                
            raise RuntimeError("All %d attempts failed!" % max_attempts)

        return wrapper
    
    return wrap





