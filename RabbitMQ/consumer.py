import pika

from time import sleep

from src.models import Contact
from MongoDB import connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='sending', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    contacts = Contact.objects()
    contact_id = body.decode()
    sleep(1)
    print(f" [x] Notification sent successfully to the contact ID{contact_id}")
    contacts(id=contact_id)[0].update(send=True)


channel.basic_consume(queue='sending', on_message_callback=callback, auto_ack=True)

if __name__ == '__main__':
    channel.start_consuming()
