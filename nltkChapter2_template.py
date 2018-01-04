import nltk, re, pprint

from nltk import book

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn


def exercise2():
	austenPersuasion = len(nltk.corpus.gutenberg.words('austen-persuasion.txt'))
	print "Word count:", len(austenPersuasion)
	print "Word types:", len(set(austenPersuasion))

	
def exercise5():
	words = ["tree.n.01", "human.n.01", "family.n.01", "mammal.n.01", "family.n.01", "vehicle.n.01", "nation.n.01", "kingdom.n.01", "book.n.01", "car.n.01"]
	for word in words:
		wn.synset(word).member_meronyms()
		wn.synset(word).part_meronyms()
		wn.synset(word).substance_meronyms()
		wn.synset(word).member_holonyms()
		wn.synset(word).part_holonyms()
		wn.synset(word).substance_holonyms()
	
def exercise9():
    text1 = book.text1
	text7 = book.text7
	print("text1 types:", len(set(text1)))
	print("text7 types:", len(set(text7)))
	
	fdist1 = FreqDist([w.lower() for w in text1 if len(w) > 6])
	sorted(fdist1.items()[:50])
	fdist7 = FreqDist([w.lower() for w in text7 if len(w) > 6])
	sorted(fdist7.items()[:50])
	
	# matching pairs
	limit = 3
	idx = 0
	matches = []
	
	for word1 in fdist1:
		for word7 in fdist7:
			if word7 == word7:
				idx++
				matches.append(word7)
			
			if idx >= limit:
				break
	
	for match in matches:
		text1.concordance(match)
		text7.concordance(match)
		

def exercise11():
	#Investigate the table of modal distributions and look for other patterns.
	#Try to explain them in terms of your own impressionistic understanding of the different genres.
	#Can you find other closed classes of words that exhibit significant differences across different genres?
	cfd = nltk.ConditionalFreqDist(
		genre, word)
		for genre in brown.categories()
		for word in brown.words(categories=genre))	
	genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
	modals = ['a', 'an', 'the']
	fd.tabulate(conditions=genres, samples=modals)


def exercise13():
	#What percentage of noun synsets have no hyponyms? You can get all noun synsets using wn.all_synsets('n')
	allNounSynsets = wn.all_synsets('n')
	nounceSynsets = len([synset for synset in list(allNounSynsets)])
	nonHypSynsets = len([synset for synset in list(allNounSynsets) if len(list(synset.hyponyms()))==0])
	print()"Percentage of non-hyponym noun synsets:", nonHypSynsets/nounceSynsets)

def exercise18():
	#Write a program to print the 50 most frequent bigrams (pairs of adjacent words) of a text, omitting bigrams that contain stopwords
	#In addition to omitting stopwords, also omit punctuation. Run your function on Brown corpus. What are the first 5 bigrams your function outputs.
	
	bigrams = nltk.bigrams(nltk.corpus.brown.words(categories="news"))
	fdist = FreqDist(bigrams)
	# print 50 most frequent bigrams
	fdist.items()[:50]
	#fdist = FreqDist([w for w in bigrams if w[0] not in stopwords])
	fdist = FreqDist([w for w in bigrams if w[0] not in stopwords and w[1] not in stopwords])
	fdist.items()[:50]

def exercise27():
    #The polysemy of a word is the number of senses it has. Using WordNet, we can determine that the noun dog has 7 senses with: len(wn.synsets('dog', 'n')).
	#Compute the average polysemy of nouns, verbs, adjectives and adverbs according to WordNet.
	#wn.all_synsets('n')
		
	synsets = list(wn.all_synsets('n'))
	count = 0
	lemma_list = []
	for synset in synsets:
		lemma_list.extend(synset.lemma_names) 
	for lemma in lemma_list:
		count = count + len(wn.synsets(lemma, 'n')) 
	print("Average polysemy:", count/len(synsets)

def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(2)
    exercise(5)
    #exercise(9)
    #exercise(11)
    #exercise(13)
    #exercise(18)
    #exercise(27)


if __name__ == "__main__":
    main()

