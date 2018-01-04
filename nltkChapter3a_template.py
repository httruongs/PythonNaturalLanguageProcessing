from __future__ import division
import nltk, re, pprint

from urllib import urlopen

from nltk import book

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

def exercise6():
	regexText = 'One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?"'
	regexText = regexText + '\rIn a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

	print("part b")
	print("[A-Z][a-z]*", "matches patterns start with an upper case, following an optional lower case.")
	nltk.re_show(r'[A-Z][a-z]*', regexText)
	print("part c")
	print("p[aeiou]{,2}t", "matches patterns start with p, end with t, and may contain 2 vowels (aeiou) in between position 0 to 2")
	nltk.re_show(r'p[aeiou]{,2}t', regexText)
	print("part f")
	print("\w+|[^\w\s]+", "matches patterns of non-space characters")
	print(nltk.re_show(r'\w+|[^\w\s]+', regexText))


def exercise7():
	#Write regular expressions to match the following classes of strings
    print("part a", "A single determiner (assume that a, an, and the are the only determiners)")
    nltk.re_show(r'\b(a|an|the)\b', SimpleText)


def exercise18():
    print("not implemented")

	
def exercise21():
	#What kind of differences do you see in the tokens you retrieve if you use nltk.word_tokenize instead of re.findall().
	#Use nltk.WordNetLemmatizer() on your tokens before checking them against the Words Corpus. Do you find fewer or more unknown words? Why?
	uri = "https://www.cs.utexas.edu/~vl/notes/dijkstra.html"
	unknowns = unknown(uri)
	print(unknowns.tabulate("")
	print("Using re.findall()", len(unknowns))
	
	#using tokenize & nltk.WordNetLemmatizer()
	raw = nltk.clean_html(urlopen(uri).read())
	tokens = nltk.word_tokenize(raw)
	
	words = sorted(set([w for w in tokens]))
	
	lemmatizedWords = []
	wnl = nltk.WordNetLemmatizer()
	#lemmatizedWords = [wnl.lemmatize(w) for w in words]
	for w in words:
		lemmatizedWords.append(wnl.lemmatize(w))
	unknowns = sorted(set([w for w in lemmatizedWords]))
	print(unknowns.tabular()
	print("Using nltk.word_tokenize", len(unknowns))
	
	print("The WordNet lemmatizer removes affixes and converts the resulting word in its dictionary.")

	
def unknown(uri):
	#Write a function unknown() that takes a URL as its argument, and returns a list of unknown words that occur on that webpage.
	#In order to do this, extract all substrings consisting of lowercase letters (using re.findall())
	#and remove any items from this set that occur in the Words Corpus (nltk.corpus.words).
	#Try to categorize these words manually and discuss your findings.
	contentText = nltk.clean_html(urlopen(uri).read())
	matches = re.findall(r'\w+', contentText) #findall
	
	corpusWords = nltk.corpus.words.words()
	
	words = sorted(set([w.lower() for w in matches if w.isalpha()]))
	unknownWords = [w for w in words if not w in corpusWords]
	return unknownWords
    

def exercise25():
	#Are you able to write a regular expression to tokenize text in such a way that the word don't is tokenized into do and n't?
	#Explain why this regular expression won't work: n't|\w+.
	nltk.re_show(r"n't|\w+", SimpleText)
	print("n't|\w+ is incorrect expression to tokenize the word don't into do and n't")
	print("Correct expression:")
	nltk.re_show(r"\w+(?=n't)|'\w+|n't|\w+|[^\s\w]", SimpleText)


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(6)
    exercise(7)
    exercise(18)
    exercise(21)
    exercise(25)


if __name__ == "__main__":
    main()

