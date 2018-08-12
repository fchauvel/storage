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
    def rabbitMQ(queue_host, callback):
        return RabbitMQ(queue_host, callback)


class RabbitMQ:

    def __init__(self, address, callback):
        self._address = address
        self._callback = RabbitMQ.wrap(callback)

              
    def connect_to(self, queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._address))
        self._channel = connection.channel()

        self._channel.queue_declare(queue=queue, durable=True)
        self._channel.basic_qos(prefetch_count=1)
        self._channel.basic_consume(self._callback, queue=queue)

    def wait_for_task(self):
        self._channel.start_consuming()


    @staticmethod
    def wrap(callback):
        def rabbitmq_callback(channel, method, properties, body):
            callback(body)
            channel.basic_ack(delivery_tag = method.delivery_tag)
        return rabbitmq_callback
    
