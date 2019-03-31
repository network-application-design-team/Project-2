#1/usr/bin/env python3

import tweepy
import json
import re
import substring as substr
# Consumer key and  access tokens
ckey = 'j08viXdK9qZynvEUWULZrASyy'
csecret = 'YuS9jcDLp5dcXmFk9yQlekhEj6dgvjIAIA07VryxO7SguNnN45'
atoken = '1109845060764553216-SfyVkOqlVNCWTkkdNr6j0N1Fn9t1bB'
asecret = 'HDXcmd6kwWrQhUNSVPfpw1loDXEqaw1MuZM4Pz2Eq94k4'

class listener(tweepy.StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]
        tweeter = tweet.replace('#ECE4564T20 ', '')

        if tweeter[0] == 'p' or tweeter[1] == 'p':
            if "#ECE4564T20" in tweeter:
                tweeter = tweeter.replace('#ECE4564T20', '')
            location = substr.substringByChar(tweeter, startChar=":", endChar="+")
            location = location[1:-1]
            print('location:')
            print(location)
            command = substr.substringByChar(tweeter, startChar="+", endChar=u'\u0020')
            command = command.rstrip()
            command = command[1:]
            print('command:')
            print(command)
            message = re.findall(r'"([^"]*)"', tweeter)
            message = message[0]
            print('message:')
            print(message)

        elif tweeter[0] == 'c' or tweeter[1] == 'c':
            if "#ECE4564T20" in tweeter:
                tweeter = tweeter.replace('#ECE4564T20', '')
                command = substr.substringByChar(tweeter, startChar="+", endChar=u'\u0020')
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

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
print('Connected to Twitter')
#api = tweepy.API(auth)

twitterStream = tweepy.Stream(auth, listener())
twitterStream.filter(track=["#ECE4564T20"])

