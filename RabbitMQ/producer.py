import pika

from seeds import seed_contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.exchange_declare(exchange='mailing', exchange_type='direct')
    channel.queue_declare(queue='sending', durable=True)
    channel.queue_bind(exchange='mailing', queue='sending')

    for _id in seed_contact():
        channel.basic_publish(
            exchange='mailing',
            routing_key='sending',
            body=str(_id),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))
        print(f" [x] Sent notification to the contact ID{str(_id)}")
    connection.close()


if __name__ == '__main__':
    main()
