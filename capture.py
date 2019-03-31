#!/usr/bin/env python
import socket
import pika
import sys
import time
import pymongo
import threading
import subprocess
import datetime

# Imports for twitter
import tweepy
import json
import re
import substring as substr
import captureKeys
import threading

# Import and pin setup for GPIO
# Make sure to use GPIO.cleanup()
# Commands: redOn(), redOff(), time.sleep(2)
import RPi.GPIO as GPIO
redPin = 11
greenPin = 13
bluePin = 15

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(redPin)

def greenOn():
    blink(greenPin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def redOff():
    turnOff(redPin)

def greenOff():
    turnOff(greenPin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)

def mongoInsert(
    action,
    place,
    subject,
    message,
    squiresRooms,
    squiresFood,
    squiresMeetings,
    libraryNoise,
    librarySeating,
    libraryWishes,
    goodwinAuditorium,
    goodwinClassrooms,
):
    # Test Data
    # action = "p"
    # place = "Squires"
    msgID = "20" + "$" + str(time.time())
    # subject = "Rooms"
    # message = "I like to be comfortable"
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
    return


# Twitter Section
# Keys for twitter dev api
ckey = captureKeys.ckey
csecret = captureKeys.csecret
atoken = captureKeys.atoken
asecret = captureKeys.asecret
# setting up authentication
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
print("Connected to Twitter")

# Twitter class:
class listener(tweepy.StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        tweeter = tweet.replace("#ECE4564T20 ", "")

        if tweeter[0] == "p" or tweeter[1] == "p":
            if "#ECE4564T20" in tweeter:
                tweeter = tweeter.replace("#ECE4564T20", "")
            location = substr.substringByChar(tweeter, startChar=":", endChar="+")
            location = location[1:-1]
            print("location:")
            print(location)
            command = substr.substringByChar(tweeter, startChar="+", endChar=u"\u0020")
            command = command.rstrip()
            command = command[1:]
            print("command:")
            print(command)
            message = re.findall(r'"([^"]*)"', tweeter)
            message = message[0]
            print("message:")
            print(message)

        elif tweeter[0] == "c" or tweeter[1] == "c":
            if "#ECE4564T20" in tweeter:
                tweeter = tweeter.replace("#ECE4564T20", "")
                command = substr.substringByChar(
                    tweeter, startChar="+", endChar=u"\u0020"
                )
            else:
                command = substr.substringByChar(tweeter, startChar="+")

            location = substr.substringByChar(tweeter, startChar=":", endChar="+")
            location = location[1:-1]
            print(location)
            command = command.rstrip()
            command = command[1:]
            print(command)

        return True

    def on_error(self, status):
        print(status)


#
# Area of interest
#
# Keys for twitter dev api
ckey = captureKeys.ckey
csecret = captureKeys.csecret
atoken = captureKeys.atoken
asecret = captureKeys.asecret

# setting up authentication
auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
print("Connected to Twitter")

twitterStream = tweepy.Stream(auth, listener())
twitterStream.filter(track=["#ECE4564T20"])
# End Twitter Section


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


channel.queue_declare(queue="SendtoCapt")
channel.queue_bind(exchange="Commands", queue="SendtoCapt", routing_key="SendtoCapt")


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

Checkpoint = 1
print(
    "["
    + str(datetime.datetime.now())
    + "] [ Checkpoint "
    + str(Checkpoint)
    + "Timestamp ] Tweet captured: "
    + message
)
Checkpoint += 1

print(
    "["
    + str(datetime.datetime.now())
    + "] [ Checkpoint "
    + str(Checkpoint)
    + "Timestamp ] Store command in MongoDB instance: "
    + str(documentInserted)
)
Checkpoint += 1

print(
    "["
    + str(datetime.datetime.now())
    + "] [ Checkpoint "
    + str(Checkpoint)
    + "Timestamp ] GPIO LED"
)
Checkpoint += 1

print(
    "["
    + str(datetime.datetime.now())
    + "] [ Checkpoint "
    + str(Checkpoint)
    + "Timestamp ] Print out RabbitMQ command sent to the Repository RPi: "
)
Checkpoint += 1

print(
    "["
    + str(datetime.datetime.now())
    + "] [ Checkpoint "
    + str(Checkpoint)
    + "Timestamp ] Print statements generated by the RabbitMQ instance "
)
Checkpoint += 1


def callback1(ch, method, properties, body):
    print("cold")


channel.basic_consume(callback1, queue="SendtoCapt", no_ack=True)

channel.start_consuming()
