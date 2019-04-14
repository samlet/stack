import pika
import sys

class Blackboard(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='topic_logs',
                                 exchange_type='topic')
        # self.serve('anonymous.info')

    def send(self, message, routing_key='anonymous.info'):
        # routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
        # message = ' '.join(sys.argv[2:]) or 'Hello World!'
        self.channel.basic_publish(exchange='topic_logs',
                              routing_key=routing_key,
                              body=message)
        print(" [x] Sent %r:%r" % (routing_key, message))

    def close(self):
        self.connection.close()


class BlackboardReceiver(object):
    def __init__(self):

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange='topic_logs',
                                 exchange_type='topic')

    # def serve(self, *binding_keys):
    def serve(self, binding_keys=None):
        if binding_keys is None:
            binding_keys = ['anonymous.info']
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        # binding_keys = sys.argv[1:]

        for binding_key in binding_keys:
            self.channel.queue_bind(exchange='topic_logs',
                               queue=queue_name,
                               routing_key=binding_key)

        print(' [*] Waiting for logs ...')

        def callback(ch, method, properties, body):
            print(" [x] %r:%r" % (method.routing_key, body))

        self.channel.basic_consume(callback,
                              queue=queue_name,
                              no_ack=True)

        self.channel.start_consuming()


