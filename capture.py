
#!/usr/bin/env python

import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='Squires', exchange_type='direct')
channel.exchange_declare(exchange='Goodwin', exchange_type='direct')
channel.exchange_declare(exchange='Library', exchange_type='direct')



message = ' '.join(sys.argv[1:]) or "info:Hello World!"
channel.basic_publish(exchange='Squires', routing_key='', body=message)

