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

def test():
	try:
		OUTPUT_FILENAME = TEST_FILENAME + ".eval.out"
		OUTPUT_HANDLER = open(OUTPUT_FILENAME, "w")
		doc_num = 0
		for c_name in class_details.keys():
			belongs[c_name] = 0

		for line in open(TEST_FILENAME, 'r'):
			doc_num+=1
			actual_class, features = line.rstrip().split(None, 1)
			actual_result[doc_num] = actual_class
			belongs[actual_class]+=1

			max_class_prob = None
			predicted_class = ""
			for c_name in class_details.keys():
				#prob_msg = float(class_details[c_name].split()[2]) #class_prob
				prob_msg = 0
				for feature in features.split():
					token,frequency = feature.split(":")
					frequency = int(frequency) # always its > 0
					if token in feature_prob:
						prob_msg+= (feature_prob[token][c_name]*frequency) # * as its log
				class_prob = float(class_details[c_name].split()[2]) #class_prob
				prob_class_given_msg = class_prob+prob_msg
				if max_class_prob is None or prob_msg>max_class_prob:
					max_class_prob = prob_msg
					predicted_class = c_name
			predicted_result[doc_num] = predicted_class
			OUTPUT_HANDLER.write(predicted_class+"\n")
		evaluate_result()
	except:
		raise

def evaluate_result():
	try:
		correctly_classified_documents = 0
		correctly_classified = dict()
		classified = dict()
		for c_name in class_details.keys():
			classified[c_name] = 0
			correctly_classified[c_name] = 0

		for doc_num in actual_result.keys():
			c_name = actual_result[doc_num]
			classified[predicted_result[doc_num]]+=1
			if c_name == predicted_result[doc_num]:
				correctly_classified[c_name]+=1
				correctly_classified_documents+=1

		accuracy = correctly_classified_documents/total_documents

		for c_name in class_details.keys():
			c_name_belongs = belongs[c_name]
			precision = correctly_classified[c_name]/classified[c_name]
			recall = correctly_classified[c_name]/c_name_belongs
			f_score = (2*precision*recall)/(precision+recall)
			print(c_name, ":", "Precision:", precision, "Recall:", recall, "F-Score:", f_score, "Accuracy:", accuracy, "Correctly classified :", correctly_classified[c_name] , " Classified as this class :", classified[c_name] , "Total correctly classified docs :", correctly_classified_documents)
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
		test()
	end = timeit.default_timer()
	print("Total time taken:",str(end-start)+"s") #seconds
except Exception as e:
	handle_exception("ERROR: Invalid input! Provide valid input to process " + str(e))

