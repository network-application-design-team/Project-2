import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='Squires', exchange_type='direct')
channel.exchange_declare(exchange='Goodwin', exchange_type='direct')
channel.exchange_declare(exchange='Library', exchange_type='direct')



result = channel.queue_declare(exclusive=True)
Food = result.method.queue
channel.queue_bind(exchange='Squires', queue=Food)

result1 = channel.queue_declare(exclusive=True)
Meetings = result.method.queue
channel.queue_bind(exchange='Squires', queue=Meetings)

result2 = channel.queue_declare(exclusive=True)
Rooms = result.method.queue
channel.queue_bind(exchange='Squires', queue=Rooms)

Classrooms = result.method.queue
Auditorium = result.method.queue
channel.queue_bind(exchange='Goodwin', queue=Classrooms)
channel.queue_bind(exchange='Goodwin', queue=Auditorium)

Noise = result.method.queue
Seating = result.method.queue
Wishes = result.method.queue
channel.queue_bind(exchange='Library', queue=Noise)
channel.queue_bind(exchange='Library', queue=Seating)
channel.queue_bind(exchange='Library', queue=Wishes)


def callback(ch, method, properties, body):
    print(" hot")
    #all of the code to display on screen

channel.basic_consume(callback, queue=Food, no_ack=True)

channel.start_consuming()
