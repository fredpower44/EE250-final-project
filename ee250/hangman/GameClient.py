import requests
import paho.mqtt.client as mqtt
import time



def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("fyzhang/guess")
    client.message_callback_add("fyzhang/guess", guessCallback)

def guessCallback(client, userdata, msg):
	guess = str(msg.payload, "utf-8")
	global guessQueue
	guessQueue.append(guess)
	print(guessQueue)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#Uses wordnik randomWords API to generate a random word
def getRandomWord():
	word = '-'
	while not word.isalnum():
		params = {
			'hasDictionaryDef': True,
			'minCorpusCount': 100,
			'limit': 1,
			'api_key': 'a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5'
		}
		response = requests.get('http://api.wordnik.com/v4/words.json/randomWords', params)
		if response.status_code == 200:
			data = response.json()
			word = data[0]['word']
	return word

#reveals letters in hiddenWord if guess is correct
def guessLetter(guess):
	global word
	global hiddenWord
	print(word)
	while guess in word:
		ind = int(word.find(guess))
		hiddenWord = hiddenWord[0:ind] + word[ind] + hiddenWord[ind+1:len(word)]
		word = word[0:ind] + '*' + word[ind+1:len(word)]

#main method
if __name__ == "__main__":
	#initialize all global variables
	global guessQueue
	global word
	global hiddenWord
	global fullWord
	word = getRandomWord()
	word = 'ruffled'
	fullWord = word
	print(word)
	hiddenWord = ''
	while len(hiddenWord) < len(word):
		hiddenWord = hiddenWord + '_'
	guessQueue = []

	#initialize mqtt client
	client = mqtt.Client()
	client.on_message = on_message
	client.on_connect = on_connect
	client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
	client.loop_start()
	time.sleep(2)

	#pull from the guessQueue and apply the guesses
	lives = 6
	while lives > 0:
		print("You have " + str(lives) + " guesses left. Guess any letter:")
		print(hiddenWord)
		while len(guessQueue) == 0:
			time.sleep(0.1)
		# guess = input()
		guess = guessQueue.pop(0)
		if guess in word:
			guessLetter(guess)
			client.publish("fyzhang/correct", "CORRECT")
		else:
			lives -= 1
			client.publish("fyzhang/correct", "INCORRECT")
		if hiddenWord == fullWord:
			break

	#Print win/lose game message
	if lives == 0:
		print("You have no more lives. You lost.")
	else:
		print("Congratulations! You won!")
	print("The word was: " + fullWord)