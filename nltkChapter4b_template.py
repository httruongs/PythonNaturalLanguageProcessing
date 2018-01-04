from __future__ import division
import nltk, re, pprint

from urllib import urlopen

from nltk import book
from nltk import memoize

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc
from timeit import Timer

#from urllib import request
import urllib
from bs4 import BeautifulSoup

SimpleText='One day, his horse ran away. The neighbors came to express their concern: "Oh, that\'s too bad. How are you going to work the fields now?" The farmer replied: "Good thing, Bad thing, Who knows?" In a few days, his horse came back and brought another horse with her. Now, the neighbors were glad: "Oh, how lucky! Now you can do twice as much work as before!" The farmer replied: "Good thing, Bad thing, Who knows?"'

url = "https://www.cs.utexas.edu/~vl/notes/dijkstra.html"
#response = urllib.urlopen(url) #request.urlopen(url)
html = urlopen(url).read().decode('utf8')
#TestText = nltk.clean_html(html)
TestText = BeautifulSoup(html).get_text() # use bs4.BeautifulSoup since nltk.clean_html() is depricated


def exercise0():
#exercise 0 (0 is a dummy name in this case).Write a function to sort a list of WordNet synsets
# for proximity to a given synset in accordance with their shortest_path_distance(). Report what
# your function produces given the synsets minke_whale.n.01, orca.n.01, novel.n.01, 
#and tortoise.n.01, sorted with respect to  right_whale.n.01.  
	# define list of synsets
	synsets = ['minke_whale.n.01', 'orca.n.01', 'novel.n.01', 'tortoise.n.01']
	sort_key = 'right_whale.n.01'
	
	whales = [wn.synset(s) for s in synsets]
	#whales = [wn.synset(s) for s in "minke_whale.n.01, orca.n.01, novel.n.01, tortoise.n.01".split(', ')]
	print (whales)
	print("synset sort", synset_sort(whales, wn.synset(sort_key)))
	

def synset_sort(sslist, skey):
	result = [(skey.shortest_path_distance(s), s) for s in sslist]
	result = sorted(result)
	return [s for (sm, s) in result]
	

def recursive_catalan(n):
	# http://www.geeksforgeeks.org/program-nth-catalan-number/
	# Base Case
	if n <=1 :
		return 1

	# Catalan(n) is the sum of catalan(i)* catalan(n-i-1)
	result = 0
	for i in range(n):
		result += recursive_catalan(i) * recursive_catalan(n-i-1)

	return result

def dynamic_catalan(n):
	result = 0
	if n <= 1:
		result = 1
	for i in range(2,n):
		for j in range(i):
			result += dynamic_catalan(j)*dynamic_catalan(i-j)
	return result
'''	
def dynamic_catalan(n):
	result = 0
	if n == 0:
		result = 1
	for i in range(n):
		result = recursive_catalan(n)
	return result
'''
def exercise26():
#Report your findings for (c) for  the 10th and 16th Catalan numbers. Template contains the parts 
#utilizing timeit functionality required in  (c). 
	# Example of timer usage:
	# print(Timer(lambda: recursive_catalan(n)).timeit(1))
	
	print('Part 1: sample recursive catalan')
	for i in range(0,10):
		print recursive_catalan(i)
	
	print('Part 2 - sample dyanmic catalan')
	for j in range(0,10):
        	print dynamic_catalan(j)
        	
        print('Part 3 - performance comparation')
        print('n = 5')
        n = 5
        #print('recursive_catalan()', Timer(lambda: recursive_catalan(n)).timeit(1))
        #print('dynamic_catalan()', Timer(lambda: dynamic_catalan(n)).timeit(1))
        
        print('n = 10')
        n = 10
        #print('recursive_catalan()', Timer(lambda: recursive_catalan(n)).timeit(1))
        #print('dynamic_catalan()', Timer(lambda: dynamic_catalan(n)).timeit(1))
        
        print('n = 15')
        n = 15
        #print('recursive_catalan()', Timer(lambda: recursive_catalan(n)).timeit(1))
        #print('dynamic_catalan()', Timer(lambda: dynamic_catalan(n)).timeit(1))

 	#Dynamic performs slower than recursive when n increase

def exercise32():
#Test your function on TestText with n=5, n=10, n=15, n=20, n=30. Does any of this number produce 
#satisfactory/natural results? Include the output of your function for n=7. 
	tokenized_sents = nltk.sent_tokenize(TestText)
	
	highest1 = summarize(TestText, 1)
	print("Sentence with the highest total word frequency (n=1):", tokenized_sents[highest1[0]['pos']])
	
	highest5 = summarize(TestText, 5)
	print("Sentences with 5 highest total word frequency (n=5)")
	for sentence in highest5:
		print(tokenized_sents[sentence['pos']])
		
	highest7 = summarize(TestText, 7)
	print("Sentences with 7 highest total word frequency (n=7)")
	for sentence in highest7:
		print(tokenized_sents[sentence['pos']])
		
	highest10 = summarize(TestText, 10)
	print("Sentences with 10 highest total word frequency (n=10)")
	for sentence in highest10:
		print(tokenized_sents[sentence['pos']])
		
	highest15 = summarize(TestText, 15)
	print("Sentences with 15 highest total word frequency (n=15)")
	for sentence in highest15:
		print(tokenized_sents[sentence['pos']])
		
	highest20 = summarize(TestText, 20)
	print("Sentences with 20 highest total word frequency (n=20)")
	for sentence in highest20:
		print(tokenized_sents[sentence['pos']])
		
	highest30 = summarize(TestText, 30)
	print("Sentences with 30 highest total word frequency (n=30)")
	for sentence in highest30:
		print(tokenized_sents[sentence['pos']])
	
	
	
def summarize(text, n):
	# tokenized words
	tokenized_words = nltk.word_tokenize(text)
	# tokenized sentences
	tokenized_sents = nltk.sent_tokenize(text)
	# word list
	word_list = [word for word in tokenized_words]
	# sentence list
	sent_list = [sent for sent in tokenized_sents]
	# freqdist
	fd = nltk.FreqDist(word_list)

	#print sent_list[1], len(sent_list[1])
	counter = 0
	result = []
	
	# determine score for all sentences
	for sent in sent_list:
		# sent_score = sum(fd[w] for w in sent) #not accurate for some reasons
		sent_score = 0
		sent_tokenized_words = nltk.word_tokenize(sent)
		
		# sum up score of all the words in each sentence
		for w in sent_tokenized_words:
			sent_score += fd[w]
		sent_info = {"pos": counter, "score": sent_score/len(sent)}
		result.append(sent_info)
		# if counter >= 2: break # break point for testing
		counter += 1
	
	# sort by score, descending order
	result = sorted(result, key=lambda k: k['score'], reverse=True) #sorted(result, key=itemgetter('score'), reverse=True) 
	
	# return nth number of result
	return result[:n]

def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    #exercise(0)
    exercise(26)
    #exercise(32)


if __name__ == "__main__":
    main()

