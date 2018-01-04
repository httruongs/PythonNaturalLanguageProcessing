from __future__ import division
import nltk, re, pprint

from urllib import urlopen

from nltk import book

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc
from collections import Counter
#from urllib import request
import urllib
#pip install beautifulsoup4
from bs4 import BeautifulSoup

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

url = "https://www.cs.utexas.edu/~vl/notes/dijkstra.html"
#response = urllib.urlopen(url) #request.urlopen(url)
html = urlopen(url).read().decode('utf8')
#TestText = nltk.clean_html(html)
TestText = BeautifulSoup(html, "html.parser").get_text() # use bs4.BeautifulSoup since nltk.clean_html() is depricated

def exercise14():
	# Write a function novel10(text) that prints any word that appeared in the last 10% of a text that had not been encountered earlier.
	#Use nltk.word_tokenize() to tokenize the text. Assume each token returned by tokenizer to represent the word.
	#Recall, that, for instance, "The" and "the" are the same words.  In this question, use TestText for testing.
	#Sort the resulting words alphabetically. Report first ten elements in your results
	
	#text = nltk.corpus.nps_chat.words()
	
	tokens = nltk.word_tokenize(TestText)
	lowerlist = [w.lower() for w in tokens]
	result = novel10(lowerlist)
	result = sorted(result)[:10]

	print(result)

def novel10(text):
	# used the last 10%
	cut = int(0.9 * len(text))
	# cuts the text
	first_part, second_part = text[:cut], text[cut:]
	# unique words of each set
	unique_first_part = set(first_part)
	unique_second_part = set(second_part)

	# list of words only in the last 10%
	return [word for word in unique_second_part if word not in unique_first_part]

def exercise17():
	# Test your function on TestText with n=20, n=35, n=50, n=65 . 
	#a) How readable is the output for every n?  
	#b) Report the outcome of your function on the following snippet from TestText:
	
	snippet = "to begin with I would like to thank the College of Natural Sciences for the most honouring Invitation to address its newest flock of Bachelors on this most festive day. I shall do my best"
	
	print("Part a")
	print shorten(TestText, 20)
	print ("n = 35")
	print shorten(TestText, 35)
	print ("n = 50")
	print shorten(TestText, 50)
	print ("n = 65")
	print shorten(TestText, 65)
	
	print("Part b")
	print shorten(snippet, 20)
	print ("n = 35")
	print shorten(snippet, 35)
	#print shorten(TestText[snippet], 50)
	#print shorten(TestText[snippet], 65)

def shorten(text, n):
	# create the n most common words in a text to be omitted
	fd = nltk.FreqDist(text)
	#most_common doesn't work, so we need to find another way
	most_common = []
	for i in range(0,n):
		most_common.append(fd.max())
		fd.pop(fd.max())
	words_to_omit = [word for word in most_common]
	#fd.most_common(n)]
	#
	# build new text omitting the most common words
	new_text = []
	blurred_text = "" # blank

	for word in text:
		if word not in words_to_omit:
			new_text.append(word)
		else:
			new_text.append(blurred_text)
			
	new_text = ' '.join(new_text)
	
	return new_text


def exercise30():
	#With the help of the trie data structure, write a recursive function that processes text,
	#locating the uniqueness point in each word, and discarding the remainder of each word.
	#How much compression does this give? How readable is the resulting text?
	#Print the output of your function for SimpleText. Compute compression using the following formula: length of the text resulting from the application of your function (considered as a string) divided by the length of the original text (considered as a string)
	

		
	tokens = nltk.word_tokenize("Child Chick Chum")
	lowerlist = [w.lower() for w in tokens]
	trie = {}
	key = []
	
	for word in tokens:
		insert(trie, word, '')
		
	trie = dict(trie)               # for nicer printing
	pprint.pprint(trie)
	
	unique_chars = [] #define a list of unique character output
	for word in tokens:
		chars = retrieve(dict(trie), word, 0)
		print word, '=>', chars
		if chars is not None and chars[0] != 'value': 
			size = len(chars)
			output = word[:size]
			unique_chars.append(output)
			#result = ','.join(chars)
			print word, '=>', 'output', output
	compression = len(unique_chars) / len(SimpleText)
	print unique_chars
	print 'compression', compression			
    

def insert(trie, key, value):
    if key:
        first, rest = key[0], key[1:]
        if first not in trie:
            trie[first] = {}
        insert(trie[first], rest, value)
    else:
        trie['value'] = value

def retrieve(trie, key,curIndex):
	#print 'processing', key
	
	if len(trie[key[curIndex]]) <= 3:
		return trie[key[curIndex]].keys()
	else:
		return
		
'''def recursive(trie, key, curIndex):
	unique = []
	if len(trie[key]) <= 1: #or len(trie[key[curIndex+1]]) == 0:
		return unique.append(trie[key].keys())
	else:
		if curIndex < len(key):
			return recursive(trie, key, curIndex+1)
		else:
			return		'''


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    #exercise(14)
    #exercise(17)
    exercise(30)


if __name__ == "__main__":
    main()

