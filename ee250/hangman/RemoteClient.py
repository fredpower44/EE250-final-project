"""EE 250L Lab 04 Starter Code

Team members: Frederick Zhang
Github: http://github.com/usc-ee250-fall2020/lab05-lab5_fred

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi
import grove_rgb_lcd as lcd

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("fyzhang/correct")
    client.message_callback_add("fyzhang/correct", correctCallback)
    client.subscribe("fyzhang/quit", quitCallback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#callback to check correctness
def correctCallback(client, userdata, msg):
    if str(msg.payload, "utf-8") == "CORRECT":
        correctBuzzer()
    elif str(msg.payload, "utf-8") == "INCORRECT":
        incorrectBuzzer()

#callback for the win/lose message
def quitCallback(client, userdata, msg):
    if str(msg.payload, "utf-8") == "WIN":
        print("Win")
    elif str(msg.payload, "utf-8") == "LOSE":
        print("Lose")
        incorrectBuzzer()

#buzzer for incorrect guess
def incorrectBuzzer():
    grovepi.digitalWrite(PORT_BUZZER, 1)
    time.sleep(0.5)
    grovepi.digitalWrite(PORT_BUZZER, 0)

#buzzer for correct guess
def correctBuzzer():
    grovepi.digitalWrite(PORT_BUZZER, 1)
    time.sleep(0.05)
    grovepi.digitalWrite(PORT_BUZZER, 0)
    time.sleep(0.025)
    grovepi.digitalWrite(PORT_BUZZER, 1)
    time.sleep(0.025)
    grovepi.digitalWrite(PORT_BUZZER, 0)

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    PORT_BUTTON = 4 #D4
    PORT_ROTARY = 0 #A0
    PORT_BUZZER = 3 #D3

    lcd.setRGB(0,32,0)

    letter = chr(0)
    while True:
        letterValue = int(grovepi.analogRead(PORT_ROTARY) / 39.385)
        nextLetter = chr(97 + letterValue)
        if nextLetter != letter:
            letter = nextLetter
            lcd.setText_norefresh("Your guess: " + letter)
        if grovepi.digitalRead(PORT_BUTTON):
            client.publish("fyzhang/guess", str(letter))
            while grovepi.digitalRead(PORT_BUTTON):
                time.sleep(0.1)

    # #defining the ports
    # Ranger = 4
    # LED = 3
    # Button = 2

    # #setting background to light blue for lcd
    # grove_rgb_lcd.setRGB(0, 64, 32)
    # grove_rgb_lcd.textCommand(1)

    # while True:
    #     client.publish("RPI_fyzhang/ultrasonicRanger", str(grovepi.ultrasonicRead(Ranger)))

    #     if grovepi.digitalRead(Button) == 1:
    #         client.publish("RPI_fyzhang/button", "Button pressed!")

    #     time.sleep(1)
            

