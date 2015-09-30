#!/usr/bin/python3
import sys
import timeit
from math import log
import traceback

INPUT_FILENAME = ""
MODEL_FILENAME = ""
VOCABULARY_SIZE = 0
vocabulary = set() # unique words across all examples
classes = dict() # list of classes
class_names = []
total_documents = 0

class Class:
	"Class details" #__doc__ - doc string
	def __init__(self, class_name):
		self.name = class_name
		self.total_words = 0
		self.vocabulary = dict()
		self.rate_of_occurrence = 0	

def handle_exception(message):
	print(message)
	sys.exit(1)

def print_stats(classes):
	try:
		for c_name in classes.keys():
			cc = classes[c_name]
			print("Class name ", cc.name)
			print("Total words ", cc.total_words)
			print("ROC ", cc.rate_of_occurrence)
			print("Vocab size ", len(cc.vocabulary.items()))
			"""for word in cc.vocabulary.keys():
				print(word, " ", cc.vocabulary[word])
			"""
	except:
		raise

def create_model():
	try:
		MODEL_FILE_HANDLER = open(MODEL_FILENAME, 'w')
		MODEL_FILE_HANDLER.write(str(total_documents) + " # total documents\n")
		MODEL_FILE_HANDLER.write(str(VOCABULARY_SIZE) + " # Vocabulary size\n")
		for c_name in class_names:
			corpus_class = classes[c_name]
			MODEL_FILE_HANDLER.write(corpus_class.name + " " + str(corpus_class.rate_of_occurrence) + " " + str(corpus_class.total_words) + " " + str(log(corpus_class.rate_of_occurrence)-log(total_documents)) +"\n")
		# calculate prob.
		for token in vocabulary:
			token_prob = token
			for c_name in class_names: # list always preserves the order
				corpus_class = classes[c_name]
				word_frequency = 1 #for add-one smoothing
				if token in corpus_class.vocabulary:
					word_frequency+= corpus_class.vocabulary[token]
				token_prob+=" " + str(log(word_frequency) - log(corpus_class.total_words + VOCABULARY_SIZE))
			MODEL_FILE_HANDLER.write(token_prob+"\n")
		MODEL_FILE_HANDLER.close()
	except:
		raise

def train():
	try:
		global total_documents
		global VOCABULARY_SIZE
		for line in open(INPUT_FILENAME, 'r'):
			total_documents+=1
			#print("Processing doc #", total_documents)
			c_name, features = line.rstrip().split(None, 1)
			if c_name not in class_names:		
				class_names.append(c_name)
				classes[c_name] = Class(c_name)
			classes[c_name].rate_of_occurrence+=1 #increment the rate of occurence
			class_vocabulary = classes[c_name].vocabulary
			for feature in features.split(): # for all features
				feature_num, feature_frequency = feature.split(":")
				feature_frequency = int(feature_frequency)
				classes[c_name].total_words+=feature_frequency
				vocabulary.add(feature_num) # contains only unique words
				if feature_num not in class_vocabulary: # as per desc
					class_vocabulary[feature_num] = feature_frequency
				else:
					class_vocabulary[feature_num]+=feature_frequency

		VOCABULARY_SIZE = len(vocabulary)
		create_model()
		print("Vocab size:", VOCABULARY_SIZE)
		print("Total documents:", total_documents)
		print_stats(classes)	
	except:
		raise

try:
	start = timeit.default_timer()
	argLen = len(sys.argv)
	if(argLen <3 or argLen>3):
		print('ERROR: Provide valid arguments e.g python3 nblearn.py /path/to/input/file path/to/model/file')
	else:
		INPUT_FILENAME = sys.argv[1] #input file
		MODEL_FILENAME = sys.argv[2] #model file
		train()
	end = timeit.default_timer()
	print("Total time taken:",str(end-start)+"s")
except Exception as e:
	handle_exception("ERROR: Invalid input! Provide valid input to process " + str(e))

