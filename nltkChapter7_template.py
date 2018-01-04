from __future__ import division
import nltk, re, pprint

from urllib import urlopen

from nltk import book

from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk.corpus import abc

from nltk import word_tokenize, pos_tag
from nltk.corpus import conll2000
from nltk.chunk.util import conlltags2tree
from nltk.chunk import *
from nltk.chunk.util import *
from nltk.chunk.regexp import *
from nltk import Tree


# Natural Language Toolkit: code_unigram_chunker
#chunk_parser = RegexpChunkParser([chunk_rule], chunk_label='NP')
class UnigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents): # [_code-unigram-chunker-constructor]
        train_data = [[(t,c) for w,t,c in nltk.chunk.util.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.UnigramTagger(train_data) # [_code-unigram-chunker-buildit]

    def parse(self, sentence): # [_code-unigram-chunker-parse]
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.util.conlltags2tree(conlltags)


# BigramChunker
class BigramChunker(nltk.ChunkParserI):
    def __init__(self, train_sents): # [_code-unigram-chunker-constructor]
        train_data = [[(t,c) for w,t,c in nltk.chunk.util.tree2conlltags(sent)]
                      for sent in train_sents]
        self.tagger = nltk.BigramTagger(train_data) # [_code-bigram-chunker-buildit]

    def parse(self, sentence): # [_code-unigram-chunker-parse]
        pos_tags = [pos for (word,pos) in sentence]
        tagged_pos_tags = self.tagger.tag(pos_tags)
        chunktags = [chunktag for (pos, chunktag) in tagged_pos_tags]
        conlltags = [(word, pos, chunktag) for ((word,pos),chunktag)
                     in zip(sentence, chunktags)]
        return nltk.chunk.util.conlltags2tree(conlltags)


# Natural Language Toolkit: code_classifier_chunker

class ConsecutiveNPChunkTagger(nltk.TaggerI): # [_consec-chunk-tagger]

    def __init__(self, train_sents):
        train_set = []
        for tagged_sent in train_sents:
            untagged_sent = nltk.tag.untag(tagged_sent)
            history = []
            for i, (word, tag) in enumerate(tagged_sent):
                featureset = npchunk_features(untagged_sent, i, history) # [_consec-use-fe]
                train_set.append( (featureset, tag) )
                history.append(tag)
        self.classifier = nltk.MaxentClassifier.train( # [_consec-use-maxent]
            train_set, algorithm='megam', trace=0)

    def tag(self, sentence):
        history = []
        for i, word in enumerate(sentence):
            featureset = npchunk_features(sentence, i, history)
            tag = self.classifier.classify(featureset)
            history.append(tag)
        return zip(sentence, history)

class ConsecutiveNPChunker(nltk.ChunkParserI): # [_consec-chunker]
    def __init__(self, train_sents):
        tagged_sents = [[((w,t),c) for (w,t,c) in
                         nltk.chunk.util.tree2conlltags(sent)]
                        for sent in train_sents]
        self.tagger = ConsecutiveNPChunkTagger(tagged_sents)

    def parse(self, sentence):
        tagged_sents = self.tagger.tag(sentence)
        conlltags = [(w,t,c) for ((w,t),c) in tagged_sents]
        return nltk.chunk.util.conlltags2tree(conlltags)


def pos_features(sentence, i, history): # [_consec-pos-tag-features]
     features = {"suffix(1)": sentence[i][-1:],
                 "suffix(2)": sentence[i][-2:],
                 "suffix(3)": sentence[i][-3:]}
     if i == 0:
         features["prev-word"] = "<START>"
         features["prev-tag"] = "<START>"
     else:
         features["prev-word"] = sentence[i-1]
         features["prev-tag"] = history[i-1]
     return features
     

def npchunk_features(sentence, i, history):
	word, pos = sentence[i]
	if i == 0:
		prevword, prevpos = "<START>", "<START>"
	else:
		prevword, prevpos = sentence[i-1]
	if i == len(sentence)-1:
		nextword, nextpos = "<END>", "<END>"
	else:
		nextword, nextpos = sentence[i+1]
	return {"pos": pos,
		"word": word,
		"prevpos": prevpos,
		"nextpos": nextpos,
		"prevpos+pos": "%s+%s" % (prevpos, pos),
		"pos+nextpos": "%s+%s" % (pos, nextpos),
		"tags-since-dt": tags_since_dt(sentence, i)} 


def tags_since_dt(sentence, i):
	tags = set()
	for word, pos in sentence[:i]:
		if pos == 'DT':
			tags = set()
		else:
			tags.add(pos)
	return '+'.join(sorted(tags))


def exercise1():
	#The IOB format categorizes tagged tokens as I, O and B. Why are three tags necessary?
	print """
	It's because IOB tags have become the standard way to represent chunk structures in files.
	In the IOB representation, there is one token per line, each with its part-of-speech tag and its chunk tag. The IOB format permits us to represent more than one chunk type, so long as the chunks do not overlap. This file format was developed as part of the chunking evaluation task run by the Conference on Natural Language Learning in 2000, and a section of Wall Street Journal text has been annotated in this format.
	Chunk structures can also be represented using trees, which have the benefit that each chunk is a constituent that can be manipulated directly. NLTK uses trees for its internal representation of chunks, and provides methods for reading and writing
such trees to the IOB format.

	What problem would be caused if we used I and O tags exclusively?
	In IOB format, tokens are tagged with one of three special chunk tags, I (inside), O (outside), or B (begin). If we use I and O exclusively, extracted information is no longer accurate. The beginnings of the chunks or sentences are missing.
	
	Provide a sentence to illustrate your point.
	Example: saw yellow cat
	"""
	print('not implemented')
	
	
def exercise2():
	chunk = [("many", "JJ"), ("researchers", "NNS"), ("two", "CD"), ("weeks", "NNS"), ("both","DT"), ("new", "JJ"), ("positions", "NNS")]
	sentenceSample = [("Many", "JJ"), ("little", "JJ"),   ("dogs", "NNS"), ("barked", "VBD"), ("at", "IN"), ("cats", "NNS")]

	# define grammar of plural noun "NP" tag
	grammar = "NP:{<DT>?<CD>?<JJ>*<NNS>}"
	
	cp = nltk.RegexpParser(grammar)
	result = cp.parse(chunk)
	print(result)
	result.draw()
	
	# Redefine the 'cp' object from this example to use your new grammar. Use this object to parse sentenceSample
	print('sentence sample:')
	grammar2 = "NP:{<DT>?<CD>?<JJ>*<NNS>}"
	result2 = cp.parse(sentenceSample)
	print(result2)
	result2.draw()
	
	
def exercise3():
	#Carry out the following evaluation tasks for the chunker you have developed in question 2
	# set variables
	chunk_types = ['NP', 'NNS'] #'JJ', 'NNS', 'VBD', 'IN'
	test_sents = "Many little dogs barked at cats"
	#test_sents = conll2000.chunked_sents('test.txt', chunk_types=chunk_types)
	train_sents = conll2000.chunked_sents('train.txt', chunk_types=chunk_types)
	
	# establishing a baseline for the trivial chunk parser cp that creates no chunks
	cp = nltk.RegexpParser("")
	test_sents = conll2000.chunked_sents('test.txt', chunk_types=chunk_types)
	print("Baseline with no chunks", cp.evaluate(test_sents))


	grammar = r"NP: {<[CDJNP].*>+}" #tags beginning with letters that are characteristic of noun phrase tags (e.g. CD, DT, and JJ)
	cp = nltk.RegexpParser(grammar)
	print("IOB tag evaluation", cp.evaluate(test_sents))
	
	# UnigramChunker
	unigram_chunker = UnigramChunker(train_sents)
	print("UnigramChunker", unigram_chunker.evaluate(test_sents))
	
	# BiGramChunker
	bigram_chunker = BigramChunker(train_sents)
	print("BigramChunker", bigram_chunker.evaluate(test_sents))
	
	# ConsecutiveNPChunker
	ngram_chunker = ConsecutiveNPChunker(train_sents)
	print("ConsecutiveNPChunker", ngram_chunker.evaluate(test_sents))

	
	
def exercise(exNum):
    print("Exercise {}".format(exNum))

    globals()["exercise"+str(exNum)]()
    print("")


def main():
    #exercise(1)
    exercise(2)
    #exercise(3)


if __name__ == "__main__":
    main()

