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

from storage.utils import retry, relay_to



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


        
class RelayTest(TestCase):

    def setUp(self):
        self._listener_1 = type("test", (), {})()
        self._listener_1.common = MagicMock()
        self._listener_1.only1 = MagicMock()
        
        self._listener_2 = type("test", (), {})()
        self._listener_2.common = MagicMock()
        
        self._relay = relay_to(self._listener_1,
                               self._listener_2)

    def test_relay_method_calls(self):
        self._relay.common()

        self.assertEqual(self._listener_1.common.call_count, 1)
        self.assertEqual(self._listener_2.common.call_count, 1)

        
    def test_relay_calls_only_to_valid_listeners(self):
        self._relay.only1()

        self.assertEqual(self._listener_1.only1.call_count, 1)


    def test_raise_attribute_error_when_no_listener_is_valid(self):
        with self.assertRaises(AttributeError):
            self._relay.does_not_exist

        
        
    

    
