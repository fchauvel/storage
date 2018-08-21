#
# SensApp::Storage
#
# Copyright (C) 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#

import pika


class QueueFactories:

    @staticmethod
    def rabbitMQ(host, port, name, listener):
        return RabbitMQ(host, port, name, listener)


    
class QueueListener:

    def connected(self, host, port, name):
        pass

    def connection_failed(self, host, port, name, error):
        pass

    def waiting_messages(self):
        pass

    def new_message(self, body):
        pass


    
class Queue:

    def __init__(self, host, port, name, listener):
        self._host = host
        self._port = port
        self._name = name
        self._listener = listener

        
    def connect(self):
        raise RuntimeError("Should be overriden!")


    def wait_messages(self):
        raise RuntimeError("Should be overriden!")
    

    
class RabbitMQ(Queue):

    
    def __init__(self, host, port, name, listener):
        super().__init__(host, port, name, listener)

              
    def connect(self):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))
            self._channel = connection.channel()
            self._channel.queue_declare(queue=self._name, durable=True)
            self._channel.basic_qos(prefetch_count=1)
            self._channel.basic_consume(self._on_new_message, queue=self._name)
            self._listener.connected(self._host, self._port, self._name)
            
        except Exception as error:
            self._listener.connection_failed(self._host, self._port, self._name, error)
            raise
            
            
    def wait_messages(self):
        self._listener.waiting_messages()
        self._channel.start_consuming()


    def _on_new_message(self, channel, method, properties, body):
        self._listener.new_message(body)
        channel.basic_ack(delivery_tag = method.delivery_tag)
    
