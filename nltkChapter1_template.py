from nltk import book
from nltk.book import *

def exercise4():
	result = len(text2)
	result2 = len(set(text2))
	print "Words in text2 are: ", result
	print "The distinct words are:", result2

def exercise5():
	lex_humor = 82345/11935
	lex_ficRomance = 70022/8452
	#print "The humor lexically diversity is 4.3"
	#print "The fiction: romance lexically diversity is 8.3"
	print "The fiction: romance is the genre which is", max(lex_humor, lex_ficRomance), "more lexically diversity"

def exercise6():
	text2.dispersion_plot(["Elinor","Marianne","Edward","Willoughby"])
    
def exercise7():
	print "the collocation in text5 is: ", text5.collocations()

def exercise17():
	
	matches = []
	sentence = ""
	idx = 0
	print "The first index of sunset is at ", text9.index('sunset')
	for word in text9:
		match = {}
		idx = idx + 1
		sentence = sentence + ("" if word in (',', ':', ';', '-', '--', '.', '?', '!') else " ") + word
		
		if word in ('.', '?', '!'):
			match = {'index': idx-1, 'text': sentence}
			matches.append(match)
			match = {}
			sentence = ""
	
	for item in matches:
		if 'sunset' in item['text']:
			print item['text']
			print "sunset index at ", item['index']

def exercise18():
	vocabularyList = []

	for word in [sent1, sent2, sent3, sent4, sent5, sent6, sent7, sent8]:
		vocabularyList = vocabularyList + word
		sorted(set(vocabularyList))
		print "The size of the vocabulary of sentence is: ", len(set(word))	
	print "The size of the computed vocabulary: ", len(set(vocabularyList))

	print "The vocabulary in the list: "

	for vocabulary in set(vocabularyList):
		print vocabulary, "|size: ", len(vocabulary)


def exercise22():

	import collections
	from nltk import book
	from nltk.book import *

	fdist = FreqDist([w for w in text5 if len(w)==4])
	for sample in fdist:
		print "The reverse list of frequency is: " , sample

	freqword = collections.defaultdict(list)
	for word, freq in collections.Counter(fdist).items():
		freqword[freq].append(word)
	
	print "The five most frequency are: "		
	for count in sorted(freqword):
		check = count > 170 
		if check == True:			
			print count, '=>', ','.join(freqword[count])
			
	
def exercise(exNum):
	
	print("Exercise {}".format(exNum))

	globals()["exercise"+str(exNum)]()
	print("")


def main():
    #exercise(4)
    exercise(5)
    #exercise(6)
    #exercise(7)
    #exercise(17)
    #exercise(18)
    #exercise(22)


if __name__ == "__main__":
    main()

