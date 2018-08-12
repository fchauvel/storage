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
        pass


    def test_retry_under_failures(self):
        function = MagicMock(side_effect=Exception("error!"))

        self.assertRaises(RuntimeError,
                         lambda: retry(function, 5))

        self.assertEqual(function.call_count, 5)


    def test_retry_under_success(self):
        function = MagicMock(return_value=6)

        retry(function, 5)

        self.assertEqual(function.call_count, 1)
