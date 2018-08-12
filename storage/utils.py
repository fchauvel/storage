#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



def retry(target, attempts):
    for _ in range(attempts):
        try:
            return target()

        except Exception:
            pass

    raise RuntimeError("All {count} attempts failed".format(count=attempts))

