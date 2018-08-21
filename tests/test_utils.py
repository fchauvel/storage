#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from unittest import TestCase

from mock import MagicMock

from storage.utils import retry



class RetryTests(TestCase):

    def setUp(self):
        self._fragile_calls = 0
        self._solid_calls = 0

        
    @retry(max_attempts=3, backoff=1)
    def fragile(self):
        self._fragile_calls += 1
        raise ValueError("Failed!")

    
    @retry(max_attempts=3, backoff=1)
    def solid(self):
        self._solid_calls += 1
        return 0

    
    def test_retry_under_failure(self):
        self.assertRaises(RuntimeError, self.fragile)
        self.assertEqual(self._fragile_calls, 3)

        
    def test_retry_under_success(self):
        self.solid()
        self.assertEqual(self._solid_calls, 1)

        
    def test_bidon(self):
        self.assertEqual(2,2)
