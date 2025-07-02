#Generates strong, mostly-easy to remeber passwords for personal use
import requests
from random import randint

# TODO: make these cli arguments
#settings for password
num_passwords = 10	#how many passwords to generate
num_words = 5		#how many words to put in the password
num_numbers = 0		#how many numbers to put in the password
num_symbols = 0		#how many special symbols to include
max_word_length = 5	#filter out nouns that are too long
min_number = 10		#minumum value for generated numbers
max_number = 99		#maximum value for generated numbers

#load a list of english nouns
nouns = requests.get("http://www.desiquintans.com/downloads/nounlist/nounlist.txt").text.split('\n')

#select words that are below the maximum length, and capitalize the first letter
nouns = [noun.capitalize() for noun in nouns if len(noun) <= max_word_length]
special_symbols = '!@#$%^&*()=+_-~<>,.?'

for i in range(num_passwords):
	#create lists of words, numbers, and symbols to put in the password
	random_words = [nouns[randint(0, len(nouns)-1)] for i in range(num_words)]
	random_numbers = [str(randint(min_number, max_number)) for i in range(num_numbers)]
	random_symbols = [special_symbols[randint(0, len(special_symbols)-1)] for i in range(num_symbols)]
	
	#combine above into single list of all tokens to appear in password
	tokens = random_words + random_numbers + random_symbols
	
	#produce a permutation of the list of indices in tokens
	indices = []
	indices_added = set()
	while len(indices) < len(tokens):
		i = randint(0, len(tokens)-1)
		if (i not in indices_added):
			indices_added.add(i)
			indices.append(i)

	#shuffle tokens with the permuted indices list
	tokens = [tokens[indices[i]] for i in range(len(tokens))]

	#combine the permuted tokens to get the password
	print(''.join(tokens))