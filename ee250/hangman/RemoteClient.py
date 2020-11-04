"""EE 250L Lab 04 Starter Code

Team members: Frederick Zhang
Github: http://github.com/usc-ee250-fall2020/lab05-lab5_fred

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
#import grovepi
#import grove_rgb_lcd

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("fyzhang/correct")
    client.message_callback_add("fyzhang/correct", correctCallback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#callback to check correctness
def correctCallback(client, userdata, msg):
    if str(msg.payload, "utf-8") == "CORRECT":
        print("Right")
    elif str(msg.payload, "utf-8") == "INCORRECT":
        print("Wrong")

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
    client.loop_start()

    while True:
        guess = input()
        client.publish("fyzhang/guess", guess)
        print("done")
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
            

