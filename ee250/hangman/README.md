Team: Frederick Zhang
Github: github.com/fredpower44/EE250-final-project
Demo Video:
External libraries: Paho MQTT Client, Requests, Grove Pi, Grove RGB LCD

Execution instructions:
1. SSH into RPi and clone the github repo from the above link anywhere in the RPi.
2. On the VM, make sure that the above libraries are installed and Python. 
3. On the VM clone the github repo from the above link into any directory.
4. Run GameClient.py on the VM. (Uncomment line 53 if you want to show the word before playing)
5. Run RemoteClient.py on the RPi.
6. Use the RPi controller to play the game!

Note:
The RPi has the grove shield attached. Here are the ports to connect sensors/actuators:
Button: D4
Buzzer: D3
LCD: I2C
Potentiometer: A0
