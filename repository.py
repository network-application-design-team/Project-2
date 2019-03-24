import pika
import sys
import time
import socket

def fetch_ip():
    return((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())\
      for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])


ip = fetch_ip()
username = "Honaker"
password = "buse"

credentials = pika.PlainCredentials(username, password)

connection = pika.BlockingConnection(pika.ConnectionParameters(ip, 5672, '/', credentials))
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
channel.basic_consume(callback, queue=Meetings, no_ack=True)
channel.basic_consume(callback, queue=Rooms, no_ack=True)
channel.basic_consume(callback, queue=Auditorium, no_ack=True)
channel.basic_consume(callback, queue=Noise, no_ack=True)
channel.basic_consume(callback, queue=Seating, no_ack=True)
channel.basic_consume(callback, queue=Wishes, no_ack=True)



channel.start_consuming()
