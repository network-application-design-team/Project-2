
#!/usr/bin/env python
import socket
import pika
import sys
import time

def fetch_ip():
    return((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())\
      for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])

node = fetch_ip()
username = "Honaker"
password = "buse"

credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(pika.ConnectionParameters(node, 
	5672, '/', credentials))
channel = connection.channel()

channel.exchange_declare(exchange='Squires', exchange_type='direct')
channel.exchange_declare(exchange='Goodwin', exchange_type='direct')
channel.exchange_declare(exchange='Library', exchange_type='direct')



message = ' '.join(sys.argv[1:]) or "info:Hello World!"
channel.basic_publish(exchange='Squires', routing_key='Squires', body=message)
channel.basic_publish(exchange='Goodwin', routing_key='Goodwin', body=message)
channel.basic_publish(exchange='Library', routing_key='Library', body=message)


connection.close()