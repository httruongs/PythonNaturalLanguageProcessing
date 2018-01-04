from __future__ import division
import nltk, re, pprint

from urllib import urlopen

from nltk import book

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc

from nltk.corpus import names
from nltk.classify.util import apply_features

class ConsecutivePosTagger(nltk.TaggerI): # [_consec-pos-tagger]

    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = pos_features(untagged_sent, i, history)
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.NaiveBayesClassifier.train(train_set)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = pos_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

#nltk.org/book_1ed/ch06.html
# for exercise 2
def gender_features(name):
	features = {}
	features["firstletter"] = name[0].lower()
	features["lastletter"] = name[-1].lower()
	for letter in 'abcdefghijklmnopqrstuvwxyz':
		features["count(%s)" % letter] = name.lower().count(letter)
		features["has(%s)" % letter] = (letter in name.lower())
	return features

# for exercise 4
def document_features(document):
	document_words = set(document)
	features = {}
	for word in word_features:
		features['contains(%s)' % word] = (word in document_words)
	return features
	
# exercise 7
def pos_features(sentence, i, history): # [_consec-pos-tag-features]
	features = {
			"suffix(1)": sentence[i][-1:],
			"suffix(2)": sentence[i][-2:],
			"suffix(3)": sentence[i][-3:]
		}
	if i == 0:
		features["prev-word"] = "<START>"
		features["prev-tag"] = "<START>"
	else:
		features["prev-word"] = sentence[i-1]
		features["prev-tag"] = history[i-1]
	return features
	
# for exercise 9
def noun_features(inst):
	features = {}
	features['noun1'] = inst.noun1
	# features['noun2'] = inst.noun2
	# features['verb'] = inst.verb
	return features

def exercise2():
	#Design at least 5 features and report what these features capture.
	#Additionally, use three classifiers, namely, nltk.NaiveBayesClassifier, nltk.DecisionTreeClassifier,  nltk.MaxentClassifier.
	#Compare the performance of the three classifiers by analyzing the accuracy.
	#Report the accuracy  of each classifier built using all of the features that you designed
	'''
	Using any of the three classifiers described in this chapter, and any features you can think of, build the best name gender classifier you can. Begin by splitting the Names Corpus into three subsets: 500 words for the test set, 500 words for the dev-test set, and the remaining 6900 words for the training set. Then, starting with the example name gender classifier, make incremental improvements. Use the dev-test set to check your progress. Once you are satisfied with your classifier, check its final performance on the test set. How does the performance on the test set compare to the performance on the dev-test set? Is this what you'd expect?
	'''
	from nltk.corpus import names
	names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
	
	train_names = names[:500]
	devtest_names = names[500:2000]
	test_names = names[2000:]
	
	featuresets = [(gender_features(n), g) for (n,g) in names]
	train_set, test_set = featuresets[:500], featuresets[500:1500], 
	
	# Naive Bayes Classifier
	classifier1 = nltk.NaiveBayesClassifier.train(train_set)
	
	# Decision Tree Classifier
	classifier2 = nltk.DecisionTreeClassifier.train(train_set)
	
	# Maxent Classifier
	#classifier3 = nltk.MaxentClassifier(train_set)
	algorithm = nltk.classify.MaxentClassifier.ALGORITHMS[0]
	classifier3 = nltk.classify.MaxentClassifier.train(train_set, algorithm, trace=0, max_iter=5)
	
	print classifier1.show_most_informative_features(5)
	
	print "Naive Bayes Classifier"
	print "Train set", nltk.classify.accuracy(classifier1, train_set), 'vs. test set', nltk.classify.accuracy(classifier1, test_set)
	print "Decision Tree Classifier"
	print "Train set", nltk.classify.accuracy(classifier2, train_set), 'vs. test set', nltk.classify.accuracy(classifier2, test_set)
	print "Maxent Classifier"
	print "Train set", nltk.classify.accuracy(classifier3, train_set), 'vs. test set', nltk.classify.accuracy(classifier3, test_set)
	
def exercise4():
	#Using the movie review document classifier discussed in this chapter, generate a list of the 30 features
	#that the classifier finds to be most informative. Can you explain why these particular features are informative?
	#Do you find any of them surprising?
	#To report, pick any 5 features out of the computed 30 and describe their relevance
	from nltk.corpus import movie_reviews
	documents = [(list(movie_reviews.words(fileid)), category)
		for category in movie_reviews.categories()
		for fileid in movie_reviews.fileids(category)]
		
	all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
	#word_features = all_words.keys()[:2000][1]
	word_features = set(all_words.keys()[:30])

	print(word_features)
	
def exercise7():
	'''The dialog act classifier assigns labels to individual posts, without considering the context in which the post is found. However, dialog acts are highly dependent on context, and some sequences of dialog act are much more likely than others. For example, a ynQuestion dialog act is much more likely to be answered by a yanswer than by a greeting. Make use of this fact to build a consecutive classifier for labeling dialog acts. Be sure to consider what features might be useful. See the code for the consecutive classifier for part-of-speech tags in 6.7 to get some ideas
	'''
	#Design at least 5 features and report what these features capture.
	#Report the accuracy of your classifier. Place your classifier code into the report
	tagged_sents = brown.tagged_sents(categories='news')
	size = int(len(tagged_sents) * 0.1)
	train_sents, test_sents = tagged_sents[size:], tagged_sents[:size]
	tagger = ConsecutivePosTagger(train_sents)
	print tagger.evaluate(test_sents)
	print()

def synsets(words):
	syns = set()
	for w in words:
		syns.update(str(s) for s in nltk.corpus.wordnet.synsets(w))

	return syns

def document_features(document):
	document_words = set(document)
	document_synsets = synsets(document_words)

	for word in document_words:
		document_synsets.update(str(s) for s in nltk.corpus.wordnet.synsets(word))

	features = dict()

	# for word in word_features:
	#     features['contains({})'.format(word)] = (word in document_words)
	
	all_words = nltk.FreqDist(w.lower() for w in nltk.corpus.movie_reviews.words())
	word_features = all_words.keys()[:2000]
	synset_features = synsets(word_features)

	for synset in synset_features:
		features[synset] = (synset in document_synsets)

	return features
		
def exercise0():
	# part a
	

	# part b
	# reference https://github.com/mikeholler/CSC499-NLP/blob/master/ch_6/exercises/improved_movie_review_classifier.py
	# by mjholler
	
	# retrieve all movie reviews in the form of (wordlist, category)
	documents = [(list(nltk.corpus.movie_reviews.words(fileid)), category)
		for category in nltk.corpus.movie_reviews.categories()
		for fileid in nltk.corpus.movie_reviews.fileids(category)
	]
	

	#all_words = nltk.FreqDist(w.lower() for w in nltk.corpus.movie_reviews.words())
	#word_features = all_words.keys()[:2000]

	# Get the top synsets in the document from the top 2000 words
	#synset_features = synsets(word_features)

	train_set = apply_features(document_features, documents[100:])
	test_set = apply_features(document_features, documents[:100])

	print 'training classifier'
	classifier = nltk.NaiveBayesClassifier.train(train_set)

	print 'accuracy', nltk.classify.accuracy(classifier, test_set)
	print '10 features', classifier.show_most_informative_features(10)

	
def exercise9():
	#Design at least 5 features and explain them.  Use nltk.NaiveBayesClassifier.
	#Report the accuracy of your classifier built using all of the features that you designed.
	#Use show_most_inforamtive_feautures(5) functionality from the classifier to inspect the individual feature performance.
	#Which of your features seem to be most influential?
	print('Extra Credit')
	
	from nltk.corpus import ppattach

	training_ppattach_corpus = ppattach.attachments('training')
	noun_ppattach_corpus = [inst for inst in training_ppattach_corpus if inst.attachment == 'N']

	features = [(noun_features(inst), inst.prep) for inst in noun_ppattach_corpus]
	cutoff = int(len(features) / 4)
	train_set, test_set = features[:cutoff], features[cutoff:]

	# Naive Bayes Classifier
	classifier1 = nltk.NaiveBayesClassifier.train(train_set)

	#Decision Tree Classifier
	classifier2 = nltk.DecisionTreeClassifier.train(train_set)

	print("Naive Bayes classifier")
	print("Accuracy", nltk.classify.accuracy(classifier1, test_set))
	print("team", classifier1.classify({'noun1': 'team'}), "researchers")
	print("Decision Tree classifier")
	print("Accuracy", nltk.classify.accuracy(classifier2, test_set))
	print("team", classifier2.classify({'noun1': 'team'}), "researchers")
	
	print("5 features:")
	print classifier1.show_most_informative_features(5)


def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    #exercise(2)
    #exercise(4)
    #exercise(7)
    exercise(0)
    #exercise(9)


if __name__ == "__main__":
    main()

