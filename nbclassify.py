#!/usr/bin/python3
import sys
import timeit
import math
from math import log

MODEL_FILENAME = ""
TEST_FILENAME = ""
OUTPUT_FILENAME = "naive.out"
class_details = dict()
feature_prob = dict()
c1_name = ""
c2_name = ""

predicted_result = dict()
actual_result = dict()
belongs = dict()
total_documents = 0
vocabulary_size = 0

def handle_exception(message):
	print(message)
	sys.exit(1)

def load_model():
	try:
		global total_documents
		global vocabulary_size
		MODELFILE_HANDLER = open(MODEL_FILENAME, 'r')
		total_documents = int(MODELFILE_HANDLER.readline().split()[0])
		vocabulary_size = int(MODELFILE_HANDLER.readline().split()[0])

		c1_name, details = MODELFILE_HANDLER.readline().split(None, 1)
		class_details[c1_name] = details #roc, total_words, prob

		c2_name, details = MODELFILE_HANDLER.readline().split(None, 1)
		class_details[c2_name] = details

		for line in MODELFILE_HANDLER:
			feature_num, c1_prob, c2_prob = line.split()
			feature_prob[feature_num] = {c1_name:float(c1_prob), c2_name:float(c2_prob)}
	except:
		raise

def predict():
	try:
		for line in open(TEST_FILENAME, 'r'):
			features = line.rstrip().split()
			max_class_prob = None
			predicted_class = ""
			for c_name in class_details.keys():
				prob_msg = 0
				for feature in features:
					token,frequency = feature.split(":")
					frequency = int(frequency) # always its > 0
					if token in feature_prob:
						prob_msg+= (feature_prob[token][c_name]*frequency)
				class_prob = float(class_details[c_name].split()[2]) #class_prob
				prob_class_given_msg = class_prob+prob_msg
				if max_class_prob is None or prob_msg>max_class_prob:
					max_class_prob = prob_msg
					predicted_class = c_name
			print(predicted_class)
	except:
		raise

try:	
	start = timeit.default_timer()	
	argLen = len(sys.argv)
	if(argLen <3 or argLen>3):
		print('ERROR: Provide valid arguments e.g python3 nbclassify.py /path/to/model/file path/to/test/file')
	else:
		MODEL_FILENAME = sys.argv[1] #input file
		TEST_FILENAME = sys.argv[2] #model file
		load_model()
		predict()
	end = timeit.default_timer()
	#print("Total time taken:",str(end-start)+"s") #seconds
except Exception as e:
	handle_exception("ERROR: Invalid input! Provide valid input to process " + str(e))

