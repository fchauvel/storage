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


    def test_parsing_version(self):
        for marker in ["-v", "--version"]:
            settings = Settings.from_command_line(["-v"]);
            self.assertEqual(settings.command, Command.SHOW_VERSION)


    def test_parsing_queue_host(self):
        HOST = "my-super-queue"
        for marker in ["-q", "--queue-host"]:
            settings = Settings.from_command_line([marker, HOST])
            self.assertEqual(settings.queue_address, HOST)


    def test_parsing_queue_port(self):
        PORT = "5567"
        for marker in ["-p", "--queue-port"]:
            settings = Settings.from_command_line([marker, PORT])
            self.assertEqual(settings.queue_port, int(PORT))


    def test_parsing_queue_name(self):
        QUEUE_NAME = "my queue"
        for marker in ["-n", "--queue-name"]:
            settings = Settings.from_command_line([marker, QUEUE_NAME]);
            self.assertEqual(settings.queue_name, QUEUE_NAME)


    def test_parsing_db_host(self):
        DB_HOST = "my-storage-db"
        for marker in ["-o", "--db-host"]:
            settings = Settings.from_command_line([marker, DB_HOST]);
            self.assertEqual(settings.db_host, DB_HOST)


    def test_parsing_db_port(self):
        DB_PORT = "4545"
        for marker in ["-r", "--db-port"]:
            settings = Settings.from_command_line([marker, DB_PORT]);
            self.assertEqual(settings.db_port, int(DB_PORT))


    def test_parsing_db_name(self):
        DB_NAME = "sensors"
        for marker in ["-m", "--db-name"]:
            settings = Settings.from_command_line([marker, DB_NAME]);
            self.assertEqual(settings.db_name, DB_NAME)
