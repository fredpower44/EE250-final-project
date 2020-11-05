import paho.mqtt.client as mqtt
import time
import sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi
import grove_rgb_lcd as lcd
import threading

lock = threading.Lock()

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("fyzhang/correct")
    client.message_callback_add("fyzhang/correct", correctCallback)
    client.subscribe("fyzhang/quit", quitCallback)
    client.message_callback_add("fyzhang/quit", quitCallback)

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#callback to check correctness
def correctCallback(client, userdata, msg):
    if str(msg.payload, "utf-8") == "CORRECT":
        print("Right!")
        correctBuzzer()
    elif str(msg.payload, "utf-8") == "INCORRECT":
        print("Wrong!")
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
    with lock:
        grovepi.digitalWrite(PORT_BUZZER, 1)
        time.sleep(0.5)
        grovepi.digitalWrite(PORT_BUZZER, 0)

#buzzer for correct guess
def correctBuzzer():
    with lock:
        grovepi.digitalWrite(PORT_BUZZER, 1)
        time.sleep(0.05)
        grovepi.digitalWrite(PORT_BUZZER, 0)
        time.sleep(0.03)
        grovepi.digitalWrite(PORT_BUZZER, 1)
        time.sleep(0.05)
        grovepi.digitalWrite(PORT_BUZZER, 0)

if __name__ == '__main__':
    # try:
        client = mqtt.Client()
        client.on_message = on_message
        client.on_connect = on_connect
        client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
        client.loop_start()

        PORT_BUTTON = 4 #D4
        PORT_ROTARY = 0 #A0
        PORT_BUZZER = 3 #D3
        with lock:
            lcd.setRGB(0,32,0)
            grovepi.digitalWrite(PORT_BUZZER, 0)

        letter = chr(0)
        while True:
            with lock:
                letterValue = int(grovepi.analogRead(PORT_ROTARY) / 39.385)
                nextLetter = chr(97 + letterValue)
                if nextLetter != letter:
                    letter = nextLetter
                    lcd.setText_norefresh("Your guess: " + letter)
                if grovepi.digitalRead(PORT_BUTTON):
                    client.publish("fyzhang/guess", str(letter))
                    while grovepi.digitalRead(PORT_BUTTON):
                        time.sleep(0.1)
    # except KeyboardInterrupt:
    #     lcd.setText('')
    #     lcd.setRGB(0,0,0)
    #     grovepi.digitalWrite(PORT_BUZZER, 0)