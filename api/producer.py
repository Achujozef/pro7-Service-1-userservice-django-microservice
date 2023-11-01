import pika, json

params = pika.URLParameters('amqps://frqdhaxu:jWcYqPPsZ2rM6Ou_jNJS8fEn31ktTnDO@crow.rmq.cloudamqp.com/frqdhaxu')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish():
    print('Rabit on Producer')
    # properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='Doctor', body='hello')
