import pika
import sys
import time
import socket
import datetime

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
channel.exchange_declare(exchange='Commands', exchange_type='direct')


#result = channel.queue_declare(exclusive=True)
#Food = result.method.queue
channel.queue_declare(queue='Food')
channel.queue_bind(exchange='Squires', queue='Food', routing_key='Food')

#result1 = channel.queue_declare(exclusive=True)
#Meetings = result.method.queue
channel.queue_declare(queue='Meetings')
channel.queue_bind(exchange='Squires', queue='Meetings', routing_key='Meetings')

#result2 = channel.queue_declare(exclusive=True)
#Rooms = result.method.queue
channel.queue_declare(queue='Rooms')
channel.queue_bind(exchange='Squires', queue='Rooms', routing_key='Rooms')

#Classrooms = result.method.queue
#Auditorium = result.method.queue
channel.queue_declare(queue='Classrooms')
channel.queue_declare(queue='Auditorium')

channel.queue_bind(exchange='Goodwin', queue='Classrooms', routing_key='Classrooms')
channel.queue_bind(exchange='Goodwin', queue='Auditorium', routing_key='Auditorium')

#Noise = result.method.queue
#Seating = result.method.queue
#Wishes = result.method.queue
channel.queue_declare(queue='Noise')
channel.queue_declare(queue='Seating')
channel.queue_declare(queue='Wishes')

channel.queue_bind(exchange='Library', queue='Noise', routing_key='Noise')
channel.queue_bind(exchange='Library', queue='Seating', routing_key='Seating')
channel.queue_bind(exchange='Library', queue='Wishes', routing_key='Wishes')



checkpoint = 1

def callback(ch, method, properties, body):
    checkpoint = 1
    print(" hot")
    #all of the code to display on screen
    print("[" + str(datetime.datetime.now())  + "] [Checkpoint " + str(checkpoint).zfill(2) + "]")
    checkpoint += 1


response = "GPIO message"

channel.basic_publish(exchange='Commands',
                 routing_key='SendtoCapt',
                 body=str(response))
   

channel.basic_consume(callback, queue='Food', no_ack=True)
channel.basic_consume(callback, queue='Meetings', no_ack=True)
channel.basic_consume(callback, queue='Rooms', no_ack=True)
channel.basic_consume(callback, queue='Auditorium', no_ack=True)
channel.basic_consume(callback, queue='Noise', no_ack=True)
channel.basic_consume(callback, queue='Seating', no_ack=True)
channel.basic_consume(callback, queue='Wishes', no_ack=True)



channel.start_consuming()
