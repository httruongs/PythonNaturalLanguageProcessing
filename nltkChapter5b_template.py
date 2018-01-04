from __future__ import division
import nltk, re, pprint

from urllib import urlopen

#from nltk import book

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc
from collections import Counter

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

# Unsimplified Tags section - http://www.nltk.org/book_1ed/ch05.html
def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].keys()) for tag in cfd.conditions())

def exercise1():
	print("Part a")
	#Which nouns are more common in their plural form, rather than their singular form
	#(Use the parts of speech tags in the corpus to identify plural versus singular nouns
	# and use nltk.WordNetLemmatizer() to get the singular form of a noun from its plural form).
	# List the five most frequent nouns that feature this property.
	brown_words = brown.words()
	brown_tags = brown.tagged_words()
	tagdict = findtags('NNS', brown_tags)   # a dictionary with a list of words have 'NNS' tag

	lem = nltk.WordNetLemmatizer()
	words = []
	cf = nltk.FreqDist(brown_words)
    #print brown_words[:50]
    
	tag = 'NNS'
	for plural in tagdict[tag]:
		singular = lem.lemmatize(plural)
	#print plural, singular
		freq_sing = cf[singular]
		freq_plur = cf[plural]
		if freq_plur > freq_sing:
			words.append(plural)
			words.sort(key=lambda a: cf[a], reverse=True)
			print tag, "5 plural nouns more common:", words[:5] # last elements
	#print cf['years'], cf['yaks']


	print("Part b")
	# List the 5 most frequent tags in order of decreasing frequency. What do the tags represent?
	tags = [b[1] for (a, b) in nltk.ibigrams(brown_tags)]
	fd = nltk.FreqDist(tags)
	print fd.keys()[:10]
	print fd.values()[:10]
	i = 0
	for i in range(0, 5):
		print fd.keys()[i], fd.values()[i]
	#print " 'NN' is Noun, 'AT' prepositions, 'IN' prepositions, 'JJ' adverb"
	#for key in fd.keys():
	#if key != '.' or key != ',':
		#print key, fd.values()[counter]
		#counter = counter + 1
	#if counter > 5:
		#break

	print("The tags represent the decrease in frequency.")

	print("Part c")
	# Which three tags precede nouns tagged with the 'NN' tag most commonly? What do these three tags represent?
	# Report your findings separately for the following categories of Brown corpus: humor, romance, government.
	categories = ['humor', 'romance', 'government']

	for category in categories:

	#tagged_dict = findtags('NN', brown.tagged_words(categories=category))
		category_tags = brown.tagged_words(categories=category)
		tagList = [b[1] for (a, b) in nltk.ibigrams(category_tags) if b[1].startswith('N') and b[1] != 'N']
	#print category, tagList[:20]
		fd = nltk.FreqDist(tagList)       
		print category, ', '.join(fd.keys()[:3])
	#print category, fd.values()
 

def exercise2():
	news_tagged_sents = brown.tagged_sents(categories='news')
	#brown_sents = brown.sents(categories='news')
	size = int(len(news_tagged_sents)*0.9)
	train_sents = news_tagged_sents[:size]
	test_sents = news_tagged_sents[size:]
	t0 = nltk.DefaultTagger('NN')
	t1 = nltk.UnigramTagger(train_sents, backoff=t0)
	t2 = nltk.BigramTagger(train_sents, backoff=t1)
	t3 = nltk.TrigramTagger(train_sents, backoff=t2)
	print t3.evaluate(test_sents)
    
	print("Part a")
	lore_tagged_sents = brown.tagged_sents(categories='lore')
	lore_size = int(len(lore_tagged_sents)*0.9)
	lore_train_sents = lore_tagged_sents[:lore_size]
	lore_test_sents = lore_tagged_sents[lore_size:]
	t0 = nltk.DefaultTagger('NN')
	t1 = nltk.UnigramTagger(lore_train_sents, backoff=t0)
	t2 = nltk.BigramTagger(lore_train_sents, backoff=t1)
	t3 = nltk.TrigramTagger(lore_train_sents, backoff=t2)
	print "Compare DefaultTagger of lore and news:", t0.evaluate(lore_test_sents), t0.evaluate(test_sents)
	print "UnigramTagger val of lore", t1.evaluate(lore_test_sents)
	print "Compare the UnigramTagger from lore and news: ", t1.evaluate(lore_test_sents), t1.evaluate(test_sents)
	print "BigramTagger val of lore", t2.evaluate(lore_test_sents)
	print "Compare the BigramgramTagger from lore and news: ",t2.evaluate(lore_test_sents), t2.evaluate(test_sents)
	print "TrigramTagger val of lore", t3.evaluate(lore_test_sents)
	print "Compare the TrigramTagger from lore and news: ", t3.evaluate(lore_test_sents), t3.evaluate(test_sents)

	print("Part b")
	lore_size = 199 # 200th sentence
	lore_train_sents = lore_tagged_sents[:lore_size]
	lore_test_sents = lore_tagged_sents[lore_size:]

	unigram_tagger = nltk.UnigramTagger(lore_tagged_sents)
	unigram_val = unigram_tagger.evaluate(lore_tagged_sents)

	bigram_tagger = nltk.BigramTagger(lore_train_sents)
	bigram_val = bigram_tagger.evaluate(lore_test_sents)

	trigram_tagger = nltk.BigramTagger(lore_train_sents)
	trigram_val = trigram_tagger.evaluate(lore_test_sents)

	print(brown.sents(categories='lore')[199])    
	print("Unigram", unigram_val, 'vs.Bigram', bigram_val, 'vs.Trigram', trigram_val)
	# would not tag the sentence the same manner because of low matching


def exercise3():
    # Compare the given TrigramTagger from the previous question with a TrigramTagger where no backoff is provided.
    # Train this tagger on all of the sentences from the Brown corpus with the category news.
    # Then evaluate your tagger using "evaluate" function on  all of the sentences from the Brown corpus with the category lore.
    # Report the numbers. Which tagger performs better? Why?
	news_tagged_sents = brown.tagged_sents(categories='news')
	size = int(len(news_tagged_sents))
	train_sents = news_tagged_sents[:size]
	test_sents = news_tagged_sents[size:]
	t0 = nltk.DefaultTagger('NN')
	t1 = nltk.UnigramTagger(train_sents)
	t2 = nltk.BigramTagger(train_sents)
	t3 = nltk.TrigramTagger(train_sents)
	news_trigram_val = t3.evaluate(test_sents)
	print("trigram without backoff", news_trigram_val)
	print ("Trigram with backoff ", t3.evaluate(test_sents))

	# category lore
	lore_tagged_sents = brown.tagged_sents(categories='lore')
	lore_test_sents = lore_tagged_sents[size:]
	lore_trigram_val = t3.evaluate(lore_test_sents)
	print("Brown corpus category lore value", lore_trigram_val)

	print "Category news tagger peforms better because it evaluates tags of the same category," 
	print "thus yielding more accurate results. It performs better if evaluate tags in the same category"


def exercise4():
    # The majority of WordNet's senses are marked by four POS categories: noun, verb, adjective, and adverb.
    # Determine the percentage of words from the WordNet corpus that have senses in more than one of these categories.
    # For example, type has senses which connect to both "noun" and "verb" POS (positive case),
    # whereas typewriter has only senses which connect to "noun" POS (negative case)

    # get all words in WordNet
    wn_words = [w for w in wn.words()]                      #list of words
    wn_text = nltk.Text(word.lower() for word in wn_words)  # plain text
    #print wn_text
    pos_tags = nltk.pos_tag(wn_text)                        # tag of word (word, tag)
    
    # convert to WordNet's senses
    wn_pos_tags = []
    for pos_tag in pos_tags:
        if pos_tag[1].startswith('J'):
            wn_pos_tags.append((pos_tag[0], 'ADJ'))
        if pos_tag[1].startswith('V'):
            wn_pos_tags.append((pos_tag[0], 'VERB'))
        if pos_tag[1].startswith('N'):
            wn_pos_tags.append((pos_tag[0], 'NOUN'))
        if pos_tag[1].startswith('R'):
            wn_pos_tags.append((pos_tag[0], 'ADV'))

    
    
    count = 0
    data = nltk.ConditionalFreqDist((word, tag) for (word, tag) in wn_pos_tags)
    for word in data.conditions():
        if len(data[word]) > 1:                 # more than one sense
            count = count + 1
            tags = data[word].keys()
            print word, ' '.join(tags)
    
    print("The percentage of words that have more than one senses", count/len(wn_pos_tags))


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(1)
    #exercise(2)
    #exercise(3)
    #exercise(4)


if __name__ == "__main__":
    main()

