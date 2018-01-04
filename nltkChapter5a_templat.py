from __future__ import division
import nltk, re, pprint

from urllib import urlopen

#from nltk import collections
from collections import defaultdict

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'


def exercise1():
	news_tagged_sents = brown.tagged_sents(categories='news')
	news_sents = brown.sents(categories='news')
	unigram_tagger = nltk.UnigramTagger(news_tagged_sents)
	#part a
	lore_tagged_sents = brown.tagged_sents(categories='lore')
	lore_sents = brown.sents(categories='lore')
	unigram_tagger = nltk.UnigramTagger(lore_tagged_sents)
	unigram_tagger.tag(lore_sents[len(lore_sents)-1])
	evaluate_lore_tagged_sents = unigram_tagger.evaluate(lore_tagged_sents)
	print("Part a: Brown corpus with the category lore is ", evaluate_lore_tagged_sents)
		
	#part b
	#news_tagged_sents = brown.tagged_sents(categories='news')
	#news_sents = brown.sents(categories='news')
	#unigram_tagger = nltk.UnigramTagger(news_tagged_sents)
	
	evaluate_news_tagged_sents = unigram_tagger.evaluate(news_tagged_sents)
	print ("Part b: Brown corpus with the category news is " , evaluate_news_tagged_sents)
	print("Compare the news and lore evaluate numbers: ", evaluate_lore_tagged_sents, 'vs.', evaluate_news_tagged_sents)
	
	#part c
	unigram_tagger_200 = unigram_tagger.tag(lore_sents[199])
	print("Part C: Unigram of tagger on the 200th sentence of the lore category", unigram_tagger_200)


def exercise2():
	category_list = {'humor', 'romance', 'government'}
	#print brown.categories()
	
	print("Part 1")
	for category in category_list:
		tagged_words = brown.tagged_words(categories=category)
		distinct_tagged_words = set(tagged_words)
		cfd = nltk.ConditionalFreqDist(distinct_tagged_words)
		conditions = cfd.conditions()
		words = [condition for condition in conditions if cfd[condition]['JJ'] != 0]
		words = sorted(words)
		print(category, ', '.join(words[:5]))
	
	print("Part 2")
	for category in category_list:
		tagged_words = brown.tagged_words(categories=category)
		distinct_tagged_words = set(tagged_words)
		cfd = nltk.ConditionalFreqDist(distinct_tagged_words)
		conditions = cfd.conditions()
		words = [condition for condition in conditions if cfd[condition]['NNS'] != 0 and cfd[condition]['VBZ'] != 0]
		sorted_words = sorted(words)
		print(category, ', '.join(sorted_words[:10]))
	
	print("Part 3")
	for category in category_list:
		tagged_words = nltk.corpus.brown.tagged_words(categories=category)
		trigrams = list(nltk.trigrams(tagged_words))
		counter = 0
		
		for trigram in trigrams:
			words = [t for t in zip(*trigram)]
			if words[1] == ('IN', 'AT', 'NN'):
				print(category, words[0])
				counter = counter + 1
				if counter > 3:
					break;

	print("Part 4")
	for category in category_list:
		#brown_category_words = brown.words(categories=category)
		tagged_words = brown.tagged_words(categories=category)
		##brown_category_tag_pairs = nltk.bigrams(tagged_words)
		##brown_tagged_pp = list(nltk.FreqDist(a[1] for (a, b) in brown_category_tag_pairs if b[1] == 'PP'))
		#fd = nltk.FreqDist(brown_category_words)
		masculine = ['himself', 'his', 'him' , 'he', "he's", "he'd", "he'll"]
		feminine = ['herself', 'her', 'hers', 'she', "she's", "she'd", "she'll"]
		
		cfd = nltk.ConditionalFreqDist(tagged_words)
		conditions = cfd.conditions()
		#conditions = [contag for (condi, contag) in tagged_words if re.search('^p+.$', contag)]
		words = [condition for condition in conditions]

		mcount = 0
		fcount = 0
		for word in words:
			#if re.search('^pp+.$', word)
			if word in masculine:
				mcount = mcount + 1
			#if	re.search('^pp+.$, word)
			if word in feminine:
				fcount = fcount + 1
		print("Ratio male/female", category, mcount / fcount)
	

def exercise3():
	print("Part 1")
	#tagged_words = brown.tagged_words()
	#pos = [val for key, val in tagged_words]
	#fd = nltk.FreqDist(pos)
	#tags = fd.most_common(5)
	tagged_words = brown.tagged_words()
	cfd = nltk.ConditionalFreqDist(((word.lower(), tag) for (word, tag) in tagged_words))
	
	# gather all avaialble tagged words that have 5 tags
	#matched_tagged_words = []
	for word in cfd.conditions():
		if len(cfd[word]) == 5:
			tags = cfd[word].keys()
			print word, ' '.join(tags)
			#matched_tagged_words.append((word, len(cfd[word])))
	
	

	print("Part 2")
	from collections import Counter
	tagged_words = brown.tagged_words()
	tagged_sentences = brown.tagged_sents()
	counts = nltk.defaultdict(int)
	#fd = nltk.FreqDist(brown.words())
	#cfd = nltk.ConditionalFreqDist(tagged_words)
	#most_freq_words = cfd.keys()
	#likely_tags = dict((word, cfd[word].max()) for word in most_freq_words)
	words = [wor for (wor, tag) in tagged_words]
	tags = [tag for (word, tag) in tagged_words]
	#max_tag = nltk.FreqDist(tags).max()
	
	word_tags = []
	
	for sentence in tagged_sentences:
		uniqwords = sorted(set(sentence))
		tag = cfd[sentence].keys()
		listtag = ' '.join(tag)
		print uniqwords, " ",  listtag
		
		#max_tag = nltk.FreqDist(count).max()
		
		#any , " ", max_tag
	

	
		#print tag_tags(counts)
		#print word, counter
		#word_tags.append({'word':word,'count':counter})
		#print sorted(word_tags.item(1), key = itemgetter(1), reverse = True)
	
	
def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    exercise(1)
    #exercise(2)
    #exercise(3)


if __name__ == "__main__":
    main()

