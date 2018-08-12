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

from storage.settings import Settings, Command



class SettingsTests(TestCase):

    def setUp(self):
        pass


    def test_parsing_short_queue_address(self):
        ADDRESS = "amqp://my-task-queue:5672"

        settings = Settings.from_command_line(["-q", ADDRESS])

        self.assertEqual(settings.queue_address, ADDRESS)


    def test_parsing_long_queue_address(self):
        ADDRESS = "amqp://my-task-queue:5672"

        settings = Settings.from_command_line(["--task-queue", ADDRESS])

        self.assertEqual(settings.queue_address, ADDRESS)


    def test_parsing_short_version(self):
        settings = Settings.from_command_line(["-v"]);

        self.assertEqual(settings.command, Command.SHOW_VERSION)


    def test_parsing_long_version(self):
        settings = Settings.from_command_line(["--version"]);

        self.assertEqual(settings.command, Command.SHOW_VERSION)


    def test_parsing_short_queue_name(self):
        QUEUE_NAME = "my queue"

        settings = Settings.from_command_line(["-n", QUEUE_NAME]);

        self.assertEqual(settings.queue_name, QUEUE_NAME)


    def test_parsing_long_queue_name(self):
        QUEUE_NAME = "my queue"

        settings = Settings.from_command_line(["--queue-name", QUEUE_NAME]);

        self.assertEqual(settings.queue_name, QUEUE_NAME)

