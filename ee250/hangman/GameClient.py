import requests
import paho.mqtt.client as mqtt


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

def main():
	client = mqtt.Client()

	word = getRandomWord()
	# print(word)
	hiddenWord = ''
	while len(hiddenWord) < len(word):
		hiddenWord = hiddenWord + '_'


if __name__ == "__main__":
	main()