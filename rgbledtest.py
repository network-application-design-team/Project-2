#!/usr/bin/env python3

import sys, time
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

def blueOn():
    blink(bluePin)

def yellowOn():
    blink(redPin)
    blink(greenPin)

def cyanOn():
    blink(greenPin)
    blink(bluePin)

def magentaOn():
    blink(redPin)
    blink(bluePin)

def whiteOn():
    blink(redPin)
    blink(greenPin)
    blink(bluePin)

def redOff():
    turnOff(redPin)

def greenOff():
    turnOff(greenPin)

def blueOff():
    turnOff(bluePin)

def yellowOff():
    turnOff(redPin)
    turnOff(greenPin)

def cyanOff():
    turnOff(greenPin)
    turnOff(bluePin)

def magentaOff():
    turnOff(redPin)
    turnOff(bluePin)

def whiteOff():
    turnOff(redPin)
    turnOff(greenPin)
    turnOff(bluePin)

def main():
    while True:
        cmd = raw_input("Choose an option: ")
        if cmd == "red on":
            redOn()
        elif cmd == "green on":
            greenOn()
        elif cmd == "blue on":
            blueOn()
        elif cmd == "yellow on":
            yellowOn()
        elif cmd == "cyan on":
            cyanOn()
        elif cmd == "magenta on":
            magentaOn()
        elif cmd == "white on":
            whiteOn()
        elif cmd == "red off":
            redOff()
        elif cmd == "green off":
            greenOff()
        elif cmd == "blue off":
            blueOff()
        elif cmd == "yellow off":
            yellowOff()
        elif cmd == "cyan off":
            cyanOff()
        elif cmd == "magenta off":
            magentaOff()
        elif cmd == "white off":
            whiteOff()
        elif cmd == "strobe":
            while True:
                #stop = raw_input("Stop? press y: ")
                #if stop == "y":
                    #redOff()
                    #GPIO.cleanup()
                    #break
                #else:
                    redOn()
                    time.sleep(1)
                    redOff()
                    greenOn()
                    time.sleep(1)
                    greenOff()
                    blueOn()
                    time.sleep(1)
                    blueOff()
                    yellowOn()
                    time.sleep(1)
                    yellowOff()
                    cyanOn()
                    time.sleep(1)
                    cyanOff()
                    magentaOn()
                    time.sleep(1)
                    magentaOff()
                    whiteOn()
                    time.sleep(1)
                    whiteOff()
            return
        elif cmd == "quit":
            redOff()
            GPIO.cleanup()
            break
        else:
            print("Not a valid command")

    return

main()
