from __future__ import division
import nltk, re, pprint

from urllib import urlopen

from nltk import book

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn

#from nltk.book import *

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

def exercise1():
	#Wh-words in English are used in questions, relative clauses and exclamations.
	#Consider the set of wh-words to consist exactly of the following members: what, where, when, which, who, whom, whose, why.
	text2 = nltk.book.text2
	text7 = nltk.book.text7
	
	# part a
	count1 = 0
	for word in text2:
		if re.findall(r'^(Wh|wh).*(at|ere|en|ich|o|om|ose|y)?$', word):
			count1 = count1 + 1
	print("Total matches:", count1)
	
	#part b
	count2 = 0
	for word in text7:
		if re.findall(r'^(Wh|wh).*(at|ere|en|ich|o|om|ose|y)?$', word):
			count2 = count2 + 1
	print("Total matches:", count2)


def exercise29():
	'''
	Readability measures are used to score the reading difficulty of a text, for the purposes of selecting texts of appropriate difficulty for language learners.
	Let us define avgW to be the average number of letters per word, and avgSen to be the average number of words per sentence, in a given text.
	The Automated Readability Index (ARI) of the text is defined to be: 4.71 avgWord + 0.5 avgSen - 21.43.
	Compute the ARI score for various sections of the Brown Corpus, including section f (popular lore) and j (learned).
	Make use of the fact that nltk.corpus.brown.words() produces a sequence of words, while nltk.corpus.brown.sents() produces a sequence of sentences
	'''

	for category in brown.categories():
		chars = brown.raw(categories=category)
		words = brown.words(categories=category)
		sentences = brown.sents(categories=category)
		
		avgW = len(chars)/len(words) #average number of letters per word
		avgS = len(words)/len(sentences) #average number of words per sentence
		
		print category, "Avg Words", avgW, "Avg Sentences", avgS
		print("ARI", (4.71 * avgW ) + ( 0.5 * avgS ) - 21.43)


def exercise30():
	#Use the Porter Stemmer to normalize some tokenized text, calling the stemmer on each word.
	#Do the same thing with the Lancaster Stemmer and see if you observe any differences
	porter = nltk.PorterStemmer()
	lancaster = nltk.LancasterStemmer()
	tokens = nltk.word_tokenize(SimpleText)
	
	porterlist = []
	lancasterlist = []
	
	#[porter.stem(t) for t in tokens]
	for t in tokens:
		porterlist.append(porter.stem(t))
		
	#[lancaster.stem(t) for t in tokens]
	for t in tokens:
		lancasterlist.append(lancaster.stem(t))
	
	print("Porter list size:", len(porterlist))
	print("Lancaster list size:", len(lancasterlist))
	print("Porter distinct size:", len(set(porterlist)))
	print("Lancaster dinstinct size:", len(set(lancasterlist)))


def exercise40():
	#Obtain raw texts from two or more genres and compute their respective reading difficulty scores as in the earlier exercise on reading difficulty.
	#E.g. compare ABC Rural News and ABC Science News (nltk.corpus.abc). Use Punkt to perform sentence segmentation
	punktTokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	
	#part a
	fileId = 'rural.txt'	
	chars = nltk.corpus.abc.raw(fileId)
	words = nltk.corpus.abc.words(fileId)
	sentences = nltk.corpus.abc.sents(fileId)
	avgW = len(chars)/len(words) #average number of letters per word
	avgS = len(words)/len(sentences) #average number of words per sentence
	
	#raw = nltk.corpus.abc.raw(fileId)
	tokens = nltk.word_tokenize(chars)
	sents = punktTokenizer.tokenize(chars)
	avgW1 = len(chars)/len(tokens)
	avgS1 = len(tokens)/len(sents) 

	print("ARI", (4.71 * avgW ) + ( 0.5 * avgS ) - 21.43)
	print("Punkt ARI", (4.71 * avgW1 ) + ( 0.5 * avgS1 ) - 21.43)
	
	#part b
	fileId = 'science.txt'
	chars = nltk.corpus.abc.raw(fileId)
	words = nltk.corpus.abc.words(fileId)
	sentences = nltk.corpus.abc.sents(fileId)
	avgW = len(chars)/len(words) #average number of letters per word
	avgS = len(words)/len(sentences) #average number of words per sentence
	
	tokens = nltk.word_tokenize(chars)
	sents = punktTokenizer.tokenize(chars)
	avgW1 = len(chars)/len(tokens)
	avgS1 = len(tokens)/len(sents) 

	print("ARI", (4.71 * avgW ) + ( 0.5 * avgS ) - 21.43)
	print("Punkt ARI", (4.71 * avgW1 ) + ( 0.5 * avgS1 ) - 21.43)
	
    

def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(1)
    exercise(29)
    exercise(30)
    exercise(40)


if __name__ == "__main__":
    main()

