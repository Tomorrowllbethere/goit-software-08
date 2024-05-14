import pika, json, sys, configparser
from model import Contact
from faker import Faker
from datetime import datetime
from connect import connect

conn = connect

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='email_queue', exchange_type='direct')
channel.queue_declare(queue='email_queue')
channel.queue_bind(exchange='email_queue', queue='email_queue')

def create_fake_contacts(n):
    fake = Faker()
    for _ in range(n):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
        )
        contact.save()
        yield str(contact.id)

def send_to_queue(contact_id):
    channel.basic_publish(exchange='email_queue',
                          routing_key='email_queue',
                          body=json.dumps({'contact_id': contact_id}).encode())
    
if __name__ == '__main__':
    for contact_id in create_fake_contacts(10):  # Генеруємо 10 контактів
        print(f'\n-------\nITS A {contact_id}\n--------')
        send_to_queue(contact_id)
    
    connection.close()