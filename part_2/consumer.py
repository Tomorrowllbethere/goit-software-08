import pika
from model import Contact
from mongoengine import connect
import time
import json
from connect import connect

conn = connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    data = json.loads(body)
    contact_id = data['contact_id']
    contact = Contact.objects(id=contact_id).first()
    if contact: 
        print(f"Sending email to {contact.email}...")
        contact.message_sent = True
        contact.save()
    print(f'{contact.full_name}')
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')

    channel.basic_consume(queue='email_queue',
                          on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
   main()
