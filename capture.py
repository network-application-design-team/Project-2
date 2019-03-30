#!/usr/bin/env python
import socket
import pika
import sys
import time
import pymongo
import threading
import subprocess


def fetch_ip():
    return (
        (
            [
                ip
                for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                if not ip.startswith("127.")
            ]
            or [
                [
                    (s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                    for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
                ][0][1]
            ]
        )
        + ["no IP found"]
    )[0]


if (sys.argv != 3):
    print("Not enough arguments")


node = sys.argv[2]
username = "Honaker"
password = "buse"

credentials = pika.PlainCredentials(username, password)
connection = pika.BlockingConnection(
    pika.ConnectionParameters(node, 5672, "/", credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange="Squires", exchange_type="direct")
channel.exchange_declare(exchange="Goodwin", exchange_type="direct")
channel.exchange_declare(exchange="Library", exchange_type="direct")
channel.exchange_declare(exchange="Commands", exchange_type="direct") 

message = "info:Hello World!"
channel.basic_publish(exchange="Squires", routing_key="Food", body=message)
channel.basic_publish(exchange="Goodwin", routing_key="Goodwin", body=message)
channel.basic_publish(exchange="Library", routing_key="Library", body=message)


channel.queue_declare(queue='SendtoCapt')
channel.queue_bind(exchange='Commands', queue='SendtoCapt', routing_key='SendtoCapt')


# connection.close()

# Mongodb
mongoClient = pymongo.MongoClient()

# Get the 'warehouses'
squires = mongoClient.Squires
library = mongoClient.Library
goodwin = mongoClient.Goodwin

# Get the 'collections'
squiresFood = squires.Food
squiresRooms = squires.Rooms
squiresMeetings = squires.Meetings

libraryNoise = library.Noise
librarySeating = library.Seating
libraryWishes = library.Wishes

goodwinClassrooms = goodwin.Classrooms
goodwinAuditorium = goodwin.Auditorium


# Test Data
action = "p"
place = "Squires"
msgID = "20" + "$" + str(time.time())
subject = "Rooms"
message = "I like to be comfortable"
post = {
    "Action": action,
    "Place": place,
    "MsgID": msgID,
    "Subject": subject,
    "Message": message,
}


if place is "Squires":
    if subject is "Rooms":
        post_ID = squiresRooms.insert_one(post).inserted_id
        documentInserted = squiresRooms.find_one({"_id": post_ID})
    elif subject is "Food":
        post_ID = squiresFood.insert_one(post).inserted_id
        documentInserted = squiresFood.find_one({"_id": post_ID})
    elif subject is "Meetings":
        post_ID = squiresMeetings.insert_one(post).inserted_id
        documentInserted = squiresMeetings.find_one({"_id": post_ID})
elif place is "Library":
    if subject is "Noise":
        post_ID = libraryNoise.insert_one(post).inserted_id
        documentInserted = libraryNoise.find_one({"_id": post_ID})
    elif subject is "Seating":
        post_ID = librarySeating.insert_one.inserted_id
        documentInserted = librarySeating.find_one({"_id": post_ID})
    elif subject is "Wishes":
        post_ID = libraryWishes.insert_one(post).inserted_id
        documentInserted = libraryWishes.find_one({"_id": post_ID})
elif place is "Goodwin":
    if subject is "Classrooms":
        post_ID = goodwinClassrooms.insert_one(post).inserted_id
        documentInserted = goodwinClassrooms.find_one({"_id": post_ID})
    elif subject is "Auditorium":
        post_ID = goodwinAuditorium.insert_one(post).inserted_id
        documentInserted = goodwinAuditorium.find_one({"_id": post_ID})
