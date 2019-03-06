#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from io import StringIO

from unittest import TestCase

from deepdiff import DeepDiff

from storage.settings import Arguments, Settings, Command, EndPoint, PartnerSet




class OverrideSettingsWithArguments(TestCase):

    def setUp(self):
        self.settings = Settings.defaults()

    def _override(self, dictionary):
        self.settings.override_with(type('struct', (object, ), dictionary))

    def test_finds_db_domain_when_it_exists(self):
        self._override({"db_domain": "test"})
        self.assertEqual("test", self.settings.partners.database.domain)

    def test_finds_db_host_when_it_exists(self):
        self._override({"db_host": "test"})
        self.assertEqual("test", self.settings.partners.database.hostname)

    def test_finds_db_port_when_it_exists(self):
        self._override({"db_port": 787878})
        self.assertEqual(787878, self.settings.partners.database.port)

    def test_finds_db_port_when_it_exists(self):
        self._override({"db_port": 787878})
        self.assertEqual(787878, self.settings.partners.database.port)

    def test_finds_message_queue_port_when_it_exists(self):
        self._override({"queue_port": 787878})
        self.assertEqual(787878, self.settings.partners.message_queue.port)

    def test_finds_message_queue_port_when_it_exists(self):
        self._override({"queue_host": "my-test-queue-host"})
        self.assertEqual("my-test-queue-host", self.settings.partners.message_queue.hostname)

    def test_finds_message_queue_port_when_it_exists(self):
        self._override({"queue_host": "my-test-queue-host"})
        self.assertEqual("my-test-queue-host", self.settings.partners.message_queue.hostname)

    def test_finds_message_domain__when_it_exists(self):
        self._override({"queue_domain": "my-test-queue-domain"})
        self.assertEqual("my-test-queue-domain", self.settings.partners.message_queue.domain)

    def test_finds_registry_domain_when_it_exists(self):
        self._override({"registry_domain": "my_new_registry-domain"})
        self.assertEqual("my_new_registry-domain", self.settings.partners.registry.domain)

    def test_finds_registry_host_when_it_exists(self):
        self._override({"registry_host": "my_new_registry_host"})
        self.assertEqual("my_new_registry_host", self.settings.partners.registry.hostname)

    def test_finds_registry_port_when_it_exists(self):
        self._override({"registry_port": 1234567})
        self.assertEqual(1234567, self.settings.partners.registry.port)

    def test_finds_registry_port_when_it_is_None(self):
        self._override({"registry_port": None})
        self.assertEqual(None, self.settings.partners.registry.port)



class CreateSettingsFromArguments(TestCase):


    def _arguments_from(self, **kwargs):
        return type('struct', (object, ), kwargs)


    def test_uses_defaults_when_no_argument_is_given(self):
        arguments = self._arguments_from()
        settings = Settings.from_arguments(arguments)
        self.assertEqual(DeepDiff(Settings.defaults(), settings), {})


    def test_uses_defaults_when_config_file_does_not_exist(self):
        arguments = self._arguments_from(
            configuration_file="does_not_exists.yml")
        settings = Settings.from_arguments(arguments)
        self.assertEqual(DeepDiff(Settings.defaults(), settings), {})


    def test_uses_config_file_when_it_exists(self):
        arguments = self._arguments_from(
            configuration_file="config/storage.yml")

        settings = Settings.from_arguments(arguments)

        with open("config/storage.yml") as source:
            expected = Settings.fromYAML(source)
            self.assertEqual(DeepDiff(expected, settings), {})


    def test_overrides_defaults_with_given_arguments(self):
        arguments = self._arguments_from(
            db_host="test-db-server",
            registry_port=1290)

        settings = Settings.from_arguments(arguments)

        self.assertEqual(len(DeepDiff(Settings.defaults(), settings)["values_changed"]), 2)


    def test_overrides_config_file_with_given_arguments(self):
        arguments = self._arguments_from(
            configuration_file="config/storage.yml",
            db_host="test-db-server",
            registry_port=1290)

        settings = Settings.from_arguments(arguments)

        with open("config/storage.yml") as source:
            expected = Settings.fromYAML(source)
            self.assertEqual(len(DeepDiff(expected, settings)["values_changed"]), 2)



class CreateSettingsFromYAML(TestCase):

    def setUp(self):
        self.domain = "sensapp.org"
        fragment = ("partners: \n"
                    "  message_queue:\n"
                    "    domain: {domain}\n"
                    "    host: message-queue\n"
                    "    port: 8990\n"
                    "    resource: SENSAPP_QUEUE\n"
                    "  registry:\n"
                    "    domain: {domain}\n"
                    "    host: registry\n"
                    "    port: 3303\n"
                    "  database:\n"
                    "    domain: {domain}\n"
                    "    host: storage-db\n"
                    "    port: 1234\n"
                    "    resource: SENSAPP\n"
                    "log_configuration: config/logging.yml\n")
        self.settings = Settings.fromYAML(StringIO(fragment.format(domain=self.domain)))

    def test_finds_the_database_port(self):
        self.assertEqual(1234, self.settings.partners.database.port)

    def test_finds_the_database_domain(self):
        self.assertEqual(self.domain, self.settings.partners.database.domain)

    def test_finds_the_database_host(self):
        self.assertEqual("storage-db", self.settings.partners.database.hostname)

    def test_finds_the_database_name(self):
        self.assertEqual("SENSAPP", self.settings.partners.database.resource)

    def test_finds_the_message_queue_hostname(self):
        self.assertEqual("message-queue", self.settings.partners.message_queue.hostname)

    def test_finds_message_queue_domain(self):
        self.assertEqual(self.domain, self.settings.partners.message_queue.domain)

    def test_finds_message_queue_port(self):
        self.assertEqual(8990, self.settings.partners.message_queue.port)

    def test_finds_message_queue_name(self):
        self.assertEqual("SENSAPP_QUEUE", self.settings.partners.message_queue.resource)

    def test_finds_registry_domain(self):
        self.assertEqual(self.domain, self.settings.partners.registry.domain)

    def test_finds_registry_hostname(self):
        self.assertEqual("registry", self.settings.partners.registry.hostname)

    def test_finds_registry_port(self):
        self.assertEqual(3303, self.settings.partners.registry.port)

    def test_finds_log_configuration(self):
        self.assertEqual("config/logging.yml", self.settings.log_configuration)


class CreatingSettingsFromAnIncompleteYAML(TestCase):

    def test_uses_defaults_when_endpoints_lacks_hostname(self):
        snippet = ("log_configuration: bidon.yaml\n"
                   "partners:\n"
                   "  message_queue:\n"
                   "    domain: sensapp.org\n"
                   # Missing hostname here!
                   "    port: 67183\n"
                   "  registry:\n"
                   "    domain: sensapp.org\n"
                   "    host: registry\n"
                   "    port: 3303\n"
                   "  database:\n"
                   "    domain: sensapp.org\n"
                   "    host: storage-db\n"
                   "    port: 1234\n")
        settings = Settings.fromYAML(StringIO(snippet))
        self.assertEqual(PartnerSet.DEFAULT_MESSAGE_QUEUE.hostname,
                         settings.partners.message_queue.hostname)
        self.assertEqual(67183,
                         settings.partners.message_queue.port)

    def test_uses_defaults_when_endpoints_lacks_port(self):
        snippet = ("log_configuration: bidon.yaml\n"
                   "partners:\n"
                   "  message_queue:\n"
                   "    domain: sensapp.org\n"
                   "    host: message-queue\n"
                   "    port: 8990\n"
                   "  registry:\n"
                   "    domain: sensapp.org\n"
                   "    host: test-registry\n"
                   # Missing port
                   "  database:\n"
                   "    domain: sensapp.org\n"
                   "    host: storage-db\n"
                   "    port: 1234\n")
        settings = Settings.fromYAML(StringIO(snippet))
        self.assertEqual(PartnerSet.DEFAULT_REGISTRY.port,
                         settings.partners.registry.port)
        self.assertEqual("test-registry",
                         settings.partners.registry.hostname)

    def test_uses_defaults_when_endpoints_lacks_resource(self):
        snippet = ("log_configuration: bidon.yaml\n"
                   "partners:\n"
                   "  message_queue:\n"
                   "    domain: sensapp.org\n"
                   "    host: message-queue\n"
                   "    port: 8990\n"
                   # Missing resource
                   "  registry:\n"
                   "    domain: sensapp.org\n"
                   "    host: test-registry\n"
                   "  database:\n"
                   "    domain: sensapp.org\n"
                   "    host: storage-db\n"
                   "    port: 1234\n")
        settings = Settings.fromYAML(StringIO(snippet))
        self.assertEqual(PartnerSet.DEFAULT_MESSAGE_QUEUE.resource,
                         settings.partners.message_queue.resource)
        self.assertEqual("message-queue",
                         settings.partners.message_queue.hostname)


    def test_uses_defaults_when_endpoints_lacks_domain(self):
        snippet = ("log_configuration: bidon.yaml\n"
                   "partners:\n"
                   "  message_queue:\n"
                   "    domain: sensapp.org\n"
                   "    host: message-queue\n"
                   "    port: 8990\n"
                   "  registry:\n"
                   "    domain: sensapp.org\n"
                   "    host: registry\n"
                   "  database:\n"
                   # Missing domain!
                   "    host: storage-db\n"
                   "    port: 12034\n")
        settings = Settings.fromYAML(StringIO(snippet))
        self.assertEqual(PartnerSet.DEFAULT_DATABASE.domain,
                         settings.partners.database.domain)
        self.assertEqual(12034,
                         settings.partners.database.port)


    def test_uses_defaults_when_one_partner_is_missing(self):
        snippet = ("log_configuration: bidon.yaml\n"
                   "partners:\n"
                   "  message_queue:\n"
                   "    domain: sensapp.org\n"
                   "    host: message-queue\n"
                   "    port: 8990\n"
                   "  registry:\n"
                   "    domain: sensapp.org\n"
                   "    host: registry\n"
                   # Missing database!
        )
        settings = Settings.fromYAML(StringIO(snippet))
        self.assertEqual(PartnerSet.DEFAULT_DATABASE.domain,
                         settings.partners.database.domain)
        self.assertEqual(PartnerSet.DEFAULT_DATABASE.hostname,
                         settings.partners.database.hostname)
        self.assertEqual(PartnerSet.DEFAULT_DATABASE.port,
                         settings.partners.database.port)


    def test_uses_defaults_when_all_partners_are_missing(self):
        snippet = ("log_configuration: bidon.yaml\n"
                   # Missing database!
        )
        settings = Settings.fromYAML(StringIO(snippet))
        self.assertEqual(PartnerSet.DEFAULT_DATABASE.domain,
                         settings.partners.database.domain)
        self.assertEqual(PartnerSet.DEFAULT_DATABASE.hostname,
                         settings.partners.database.hostname)
        self.assertEqual(PartnerSet.DEFAULT_DATABASE.port,
                         settings.partners.database.port)


    def test_uses_defaults_when_log_configuration_is_missing(self):
        snippet = ("partners:\n"
                   "  message_queue:\n"
                   "    domain: sensapp.org\n"
                   "    host: message-queue\n"
                   "    port: 8990\n")
        settings = Settings.fromYAML(StringIO(snippet))
        self.assertEqual(Settings.DEFAULT_LOG_CONFIGURATION,
                         settings.log_configuration)


class APartnerSet(TestCase):

    def setUp(self):
        self.database = EndPoint("domain.org", "my-db", 1234)
        self.registry = EndPoint("domain.org", "registry", 4321)
        self.message_queue = EndPoint("domain.org", "mq", 3456)
        self.partners = PartnerSet(self.database,
                                   self.registry,
                                   self.message_queue)

    def test_has_a_database(self):
        self.assertIs(self.database, self.partners.database)

    def test_has_a_registry(self):
        self.assertIs(self.registry, self.partners.registry)

    def test_has_a_message_queue(self):
        self.assertIs(self.message_queue, self.partners.message_queue)



class CreateNewPartnerSet(TestCase):

    def setUp(self):
        self.database = EndPoint("domain.org", "my-db", 1234)
        self.registry = EndPoint("domain.org", "registry", 4321)
        self.message_queue = EndPoint("domain.org", "mq", 3456)

    def test_rejects_none_as_database(self):
        with self.assertRaises(Exception):
            partners = PartnerSet(None, self.registry, self.message_queue)

    def test_rejects_none_as_registry(self):
        with self.assertRaises(Exception):
            partners = PartnerSet(self.database, None, self.message_queue)

    def test_rejects_none_as_message_queue(self):
        with self.assertRaises(Exception):
            partners = PartnerSet(self.database, self.registry, None)



class AnEndpoint(TestCase):

    def setUp(self):
        self.domain = "here.org"
        self.hostname = "machine"
        self.port = 1235
        self.resource = "my-thing"
        self.endpoint = EndPoint(self.domain,
                                 self.hostname,
                                 self.port,
                                 self.resource)


    def test_exports_its_domain(self):
        self.assertEqual(self.domain, self.endpoint.domain)

    def test_exports_its_hostname(self):
        self.assertEqual(self.hostname, self.endpoint.hostname)

    def test_exposes_its_port(self):
        self.assertEqual(self.port, self.endpoint.port)
        self.assertTrue(int(self.endpoint.port))

    def test_exposes_a_resource(self):
        self.assertEqual(self.resource, self.endpoint.resource)

    def test_enables_setting_its_domain(self):
        new_domain = "my-new-test-domain"
        self.endpoint.domain = new_domain
        self.assertEqual(new_domain, self.endpoint.domain)

    def test_enables_setting_its_hostname(self):
        new_hostname = "my-new_test_hostname"
        self.endpoint.hostname = new_hostname
        self.assertEqual(new_hostname, self.endpoint.hostname)

    def test_enables_setting_its_port(self):
        new_port = 1234
        self.endpoint.port = new_port
        self.assertEqual(new_port, self.endpoint.port)

    def test_enables_setting_its_resource(self):
        new_resource = "My wonderfule resources"
        self.endpoint.resource = new_resource
        self.assertEqual(new_resource, self.endpoint.resource)



class CreatingANewEndpoint(TestCase):

    def test_accepts_a_string_as_port(self):
        endpoint = EndPoint("domain.org", "host", "1234", None)
        self.assertEqual(endpoint.port, 1234)

    def test_accepts_none_as_domain(self):
        endpoint = EndPoint(None, "host", 1234, None)
        self.assertIsNone(endpoint.domain)

    def test_rejects_an_non_string_object_as_domain(self):
        with self.assertRaises(Exception):
            endpoint = EndPoint(1234, "host", 1234, None)

    def test_rejects_non_string_object_as_hostname(self):
        with self.assertRaises(Exception):
            endpoint = EndPoint("domain.org", True, 1234, None)



class CreatingArgumentsFromTheCommandLine(TestCase):

    def test_finds_option(self):
        options = [
            (["--version", "-v"], None, "command", Command.SHOW_VERSION),
            (["--queue-host", "-q"], "my-host", "queue_host", "my-host"),
            (["--queue-port", "-p"], "1111", "queue_port", 1111),
            (["--queue-name", "-n"], "my-queue", "queue_name", "my-queue"),
            (["--db-host", "-o"], "my-db", "db_host", "my-db"),
            (["--db-port", "-r"], "1111", "db_port", 1111),
            (["--db-name", "-m"], "my-db", "db_name", "my-db"),
            (["--registry-host", "-t"], "my-registry", "registry_host", "my-registry"),
            (["--registry-port", "-s"], "1111", "registry_port", 1111),
            (["--configuration-file", "-c"], "test_conf.yml", "configuration_file", "test_conf.yml")
        ]

        for markers, value, attribute, expected in options:
            for marker in markers:
                with self.subTest(marker = marker):
                    command_line = [marker]
                    if value:
                        command_line.append(value)
                    arguments = Arguments.from_command_line(command_line)
                    self.assertEqual(expected, getattr(arguments, attribute))
