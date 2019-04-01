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


hash = sys.argv[4]

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
    post,
    squiresRooms,
    squiresFood,
    squiresMeetings,
    libraryNoise,
    librarySeating,
    libraryWishes,
    goodwinAuditorium,
    goodwinClassrooms,
):

    if post["Place"] == "Squires":
        if post["Subject"] == "Rooms":
            post_ID = squiresRooms.insert_one(post).inserted_id
            documentInserted = squiresRooms.find_one({"_id": post_ID})
#            print("I executed correctly")
        elif post["Subject"] == "Food":
            post_ID = squiresFood.insert_one(post).inserted_id
            documentInserted = squiresFood.find_one({"_id": post_ID})
        elif post["Subject"] == "Meetings":
            post_ID = squiresMeetings.insert_one(post).inserted_id
            documentInserted = squiresMeetings.find_one({"_id": post_ID})
    elif post["Place"] == "Library":
        if post["Subject"] == "Noise":
            post_ID = libraryNoise.insert_one(post).inserted_id
            documentInserted = libraryNoise.find_one({"_id": post_ID})
        elif post["Subject"] == "Seating":
            post_ID = librarySeating.insert_one.inserted_id
            documentInserted = librarySeating.find_one({"_id": post_ID})
        elif post["Subject"] == "Wishes":
            post_ID = libraryWishes.insert_one(post).inserted_id
            documentInserted = libraryWishes.find_one({"_id": post_ID})
    elif post["Place"] == "Goodwin":
        if post["Subject"] == "Classrooms":
            post_ID = goodwinClassrooms.insert_one(post).inserted_id
            documentInserted = goodwinClassrooms.find_one({"_id": post_ID})
        elif post["Subject"] == "Auditorium":
            post_ID = goodwinAuditorium.insert_one(post).inserted_id
            documentInserted = goodwinAuditorium.find_one({"_id": post_ID})
    return


returnMessage = ""

# Twitter class:
class listener(tweepy.StreamListener):
    def __init__(self):
        # Turn white LED on
        whiteOn()

        # Mongodb
        mongoClient = pymongo.MongoClient()

        # Get the 'warehouses'
        squires = mongoClient.Squires
        library = mongoClient.Library
        goodwin = mongoClient.Goodwin

        # Get the 'collections'
        self.squiresFood = squires.Food
        self.squiresRooms = squires.Rooms
        self.squiresMeetings = squires.Meetings

        self.libraryNoise = library.Noise
        self.librarySeating = library.Seating
        self.libraryWishes = library.Wishes

        self.goodwinClassrooms = goodwin.Classrooms
        self.goodwinAuditorium = goodwin.Auditorium

        node = sys.argv[2]
        username = "Honaker"
        password = "buse"

        credentials = pika.PlainCredentials(username, password)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(node, 5672, "/", credentials)
        )
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange="Squires", exchange_type="direct")
        self.channel.exchange_declare(exchange="Goodwin", exchange_type="direct")
        self.channel.exchange_declare(exchange="Library", exchange_type="direct")

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        tweeter = tweet.replace("#ECE4564T20 ", "")
        action = "p"
        message = ""
        if tweeter[0] == "p" or tweeter[1] == "p":
            if "#ECE4564T20" in tweeter:
                tweeter = tweeter.replace("#ECE4564T20", "")
            location = substr.substringByChar(tweeter, startChar=":", endChar="+")
            location = location[1:-1]
 #           print("location:")
  #          print(location)
            command = substr.substringByChar(tweeter, startChar="+", endChar=u"\u0020")
            command = command.rstrip()
            command = command[1:]
   #         print("command:")
    #        print(command)
            message = re.findall(r'"([^"]*)"', tweeter)
            message = message[0]
            print(
                "[ Checkpoint 01 "
                + str(datetime.datetime.now())
                + " ] Tweet captured: "
                + tweet
            )
           

        elif tweeter[0] == "c" or tweeter[1] == "c":
            action = "c"
            if "#ECE4564T20" in tweeter:
                tweeter = tweeter.replace("#ECE4564T20", "")
                command = substr.substringByChar(
                    tweeter, startChar="+", endChar=u"\u0020"
                )
                command = command[1:]
            else:
                command = tweeter.split("+", 1)
                command = command[1]

            location = substr.substringByChar(tweeter, startChar=":", endChar="+")
            location = location[1:-1]
     #       print("c location:")
      #      print(location)
            command = command.rstrip()
       #     print("c command:")
        #    print(command)
            print(
                "[ Checkpoint 01 "
                + str(datetime.datetime.now())
                + " ] Tweet captured: "
                + tweet
            )
           
        msgID = "20" + "$" + str(time.time())
        post = {
            "Action": action,
            "Place": location,
            "MsgID": msgID,
            "Subject": command,
            "Message": message,
        }
        t1 = threading.Thread(
            target=mongoInsert,
            args=(
                post,
                self.squiresRooms,
                self.squiresFood,
                self.squiresMeetings,
                self.libraryNoise,
                self.librarySeating,
                self.libraryWishes,
                self.goodwinAuditorium,
                self.goodwinClassrooms,
            ),
        )
        t1.start()
        print(
            "[ Checkpoint 02 "
            + str(datetime.datetime.now())
            + " ] Store command in MongoDB instance: "
            + str(post)
        )
        print("[ Checkpoint 03 " + str(datetime.datetime.now()) + " ] GPIO LED")
        if action == 'p':
            whiteOff()
            redOn()
            time.sleep(1)
        elif action == 'c':
            whiteOff()
            greenOn()
            time.sleep(1)

        if action == 'p':
            self.channel.basic_publish(
                exchange=location, routing_key=command, body=message
            )
            print(
            "[ Checkpoint 04 "
            + str(datetime.datetime.now())
            + " ] Print out RabbitMQ command sent to the Repository RPi: "
            + "channel.basic_publish(exchange=" + action + ", routing_key="
            + command + ", body=" + message + ")"
            )
        else:
            
            x, y, returnMessage = self.channel.basic_get(command)
            

            print(
            "[ Checkpoint 04 "
            + str(datetime.datetime.now())
            + " ] Print out RabbitMQ command sent to the Repository RPi: "
            + "channel.basic_get(" + command + ")"
            )


        if action == 'p':
            print(
            "[ Checkpoint 05 "
            + str(datetime.datetime.now())
            + " ] Print statements generated by the RabbitMQ instance "
            + "in queue " + command
            )
        else:
            print(
            "[ Checkpoint 05 "
            + str(datetime.datetime.now())
            + " ] Print statements generated by the RabbitMQ instance "
            + "message recieved " + str(returnMessage.decode("utf-8"))
            )

        
        # Check white on, turn on again
        whiteOn()
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
#print("Connected to Twitter")
try:
    twitterStream = tweepy.Stream(auth, listener())
    twitterStream.filter(track=[hash])
    # End Twitter Section
except KeyboardInterrupt:
    whiteOff()
    GPIO.cleanup()
    exit()
# connection.close()
