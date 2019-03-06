#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import yaml

from argparse import ArgumentParser
from copy import deepcopy



class EndPoint:

    @staticmethod
    def from_dictionary(dictionary, default):
        return EndPoint(dictionary.get("domain", default.domain),
                        dictionary.get("host", default.hostname),
                        dictionary.get("port", default.port),
                        dictionary.get("resource", default.resource))


    def __init__(self, domain, hostname, port, resource=None):
        assert domain is None or isinstance(domain, str), "'domain' must be a string"
        assert isinstance(hostname, str), "'hostname' must be a string"
        self._domain = domain
        self._hostname = hostname
        self._port = int(port)
        self._resource = resource

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, new_domain):
        self._domain = new_domain

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, new_hostname):
        self._hostname = new_hostname

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_port):
        self._port = new_port


    @property
    def resource(self):
        return self._resource

    @resource.setter
    def resource(self, new_resource):
        self._resource = new_resource



class PartnerSet:

    DEFAULT_REGISTRY = EndPoint("sensapp.org",
                                "registry",
                                4567)

    DEFAULT_DATABASE = EndPoint("sensapp.org",
                                "storage-db",
                                8086,
                                "sensapp")

    DEFAULT_MESSAGE_QUEUE = EndPoint("sensapp.org",
                                     "task-queue",
                                     5672,
                                     "SENSAPP_TASKS")

    @staticmethod
    def from_dictionary(dictionary):

        def fetch(key, default):
            endpoint = deepcopy(default)
            if key in dictionary:
                endpoint = EndPoint.from_dictionary(dictionary[key], default)
            return endpoint

        registry = fetch("registry", PartnerSet.DEFAULT_REGISTRY)
        database = fetch("database", PartnerSet.DEFAULT_DATABASE)
        message_queue = fetch("message_queue", PartnerSet.DEFAULT_MESSAGE_QUEUE)

        return PartnerSet(database, registry, message_queue)


    @staticmethod
    def defaults():
        return PartnerSet(deepcopy(PartnerSet.DEFAULT_DATABASE),
                          deepcopy(PartnerSet.DEFAULT_REGISTRY),
                          deepcopy(PartnerSet.DEFAULT_MESSAGE_QUEUE))


    def __init__(self, database, registry, message_queue):
        assert database, "database must be an endpoint (None found)"
        assert registry, "registry must be an endpoint (None found)"
        assert message_queue, "message queue must be an endpoint (None found)"
        self._database = database
        self._registry = registry
        self._message_queue = message_queue

    @property
    def database(self):
        return self._database

    @property
    def registry(self):
        return self._registry

    @property
    def message_queue(self):
        return self._message_queue



class Settings:

    DEFAULT_LOG_CONFIGURATION = "config/logging.yml"

    @staticmethod
    def defaults():
        return Settings(PartnerSet.defaults(),
                        Settings.DEFAULT_LOG_CONFIGURATION)

    @staticmethod
    def from_arguments(arguments):
        settings = Settings.defaults()

        if hasattr(arguments, "configuration_file") \
           and arguments.configuration_file:
            try :
                with open(arguments.configuration_file) as source:
                    settings = Settings.fromYAML(source)
            except FileNotFoundError as error:
                pass

        settings.override_with(arguments)

        return settings

    @staticmethod
    def fromYAML(source):
        data = yaml.load(source)
        return Settings.from_dictionary(data)

    @staticmethod
    def from_dictionary(dictionary):
        partners = PartnerSet.defaults()
        if "partners" in dictionary:
            partners = PartnerSet.from_dictionary(dictionary["partners"])

        logging = dictionary.get("log_configuration",
                                 Settings.DEFAULT_LOG_CONFIGURATION)
        return Settings(partners, logging)

    def __init__(self, partners, logging):
        self.partners = partners
        self.log_configuration = logging


    def override_with(self, arguments):
        mapping = [
            ("db_domain", self.partners.database, "domain"),
            ("db_host", self.partners.database, "hostname"),
            ("db_port", self.partners.database, "port"),
            ("queue_port", self.partners.message_queue, "port"),
            ("queue_host", self.partners.message_queue, "hostname"),
            ("queue_domain", self.partners.message_queue, "domain"),
            ("registry_domain", self.partners.registry, "domain"),
            ("registry_host", self.partners.registry, "hostname"),
            ("registry_port", self.partners.registry, "port"),
        ]

        for key, entity, attribute in mapping:
            if hasattr(arguments, key):
                setattr(entity, attribute, getattr(arguments, key))




class Command:
    SHOW_VERSION=1
    STORE=2


class Arguments:

    DEFAULT_COMMAND = Command.STORE
    DEFAULT_QUEUE_HOST = "task-queue"
    DEFAULT_QUEUE_PORT = "5672"
    DEFAULT_QUEUE_NAME = "SENSAPP_TASKS"
    DEFAULT_DB_HOST = "storage-db"
    DEFAULT_DB_PORT = "8086"
    DEFAULT_DB_NAME = "sensapp"
    DEFAULT_REGISTRY_HOST = "registry"
    DEFAULT_REGISTRY_PORT = 3303
    DEFAULT_CONFIGURATION_FILE = "config/storage.yml"

    HELP_VERSION = "show the version number and exit"
    HELP_QUEUE_HOST = "set the host name of the message queue (default: " + DEFAULT_QUEUE_HOST + ")"
    HELP_QUEUE_NAME = "set the name of the message queue (default: " + DEFAULT_QUEUE_NAME + ")"
    HELP_QUEUE_PORT = "set the port of the message queue (default: " + DEFAULT_QUEUE_PORT + ")"
    HELP_DB_HOST = "set the host name of the database (default: " + DEFAULT_DB_HOST + ")"
    HELP_DB_PORT = "set the port of the database (default: " + DEFAULT_DB_PORT + ")"
    HELP_DB_NAME = "set the name of the database (default: " + DEFAULT_DB_NAME + ")"

    def __init__(self, **kwargs):
        self._command = kwargs["command"] or  self.DEFAULT_COMMAND
        self._queue_host = kwargs["queue_host"] or self.DEFAULT_QUEUE_HOST
        self._queue_port = kwargs["queue_port"] or self.DEFAULT_QUEUE_PORT
        self._queue_name = kwargs["queue_name"] or self.DEFAULT_QUEUE_NAME
        self._db_host = kwargs["db_host"] or self.DEFAULT_DB_HOST
        self._db_port = kwargs["db_port"] or self.DEFAULT_DB_PORT
        self._db_name = kwargs["db_name"] or self.DEFAULT_DB_NAME
        self._registry_host = kwargs["registry_host"] \
                              or self.DEFAULT_REGISTRY_HOST
        self._registry_port = kwargs["registry_port"] \
                              or self.DEFAULT_REGISTRY_PORT
        self._configuration_file = kwargs["configuration_file"] \
                                   or self.DEFAULT_CONFIGURATION_FILE

    @property
    def command(self):
        return self._command

    @property
    def queue_host(self):
        return self._queue_host

    @property
    def queue_port(self):
        return int(self._queue_port)

    @property
    def queue_name(self):
        return self._queue_name

    @property
    def db_host(self):
        return self._db_host

    @property
    def db_port(self):
        return int(self._db_port)

    @property
    def db_name(self):
        return self._db_name

    @property
    def registry_host(self):
        return self._registry_host

    @property
    def registry_port(self):
        return int(self._registry_port)

    @property
    def configuration_file(self):
        return self._configuration_file

    @staticmethod
    def from_command_line(command_line):
        parser = ArgumentParser(prog="sensapp-storage",
                                description="Stores data sent by sensors")
        parser.add_argument("-v", "--version", help=Arguments.HELP_VERSION,
                            action="store_const", dest="command", const=Command.SHOW_VERSION)
        parser.add_argument("-q", "--queue-host", help= Arguments.HELP_QUEUE_HOST)
        parser.add_argument("-p", "--queue-port", help= Arguments.HELP_QUEUE_PORT)
        parser.add_argument("-n", "--queue-name", help= Arguments.HELP_QUEUE_NAME)
        parser.add_argument("-o", "--db-host", help=Arguments.HELP_DB_HOST)
        parser.add_argument("-r", "--db-port", help=Arguments.HELP_DB_PORT)
        parser.add_argument("-m", "--db-name", help=Arguments.HELP_DB_NAME)
        parser.add_argument("-t", "--registry-host", help="set the host name of the registry service")
        parser.add_argument("-s", "--registry-port", help="set the porto of the registry service")
        parser.add_argument("-c", "--configuration-file", help="set the file that contains the configuration")
        arguments = parser.parse_args(command_line)
        return Arguments(**vars(arguments))

    @staticmethod
    def defaults():
        return Arguments(command=Command.STORE,
                        queue_host=None,
                        queue_port=None,
                        queue_name=None,
                        db_host=None,
                        db_port=None,
                        db_name=None)
