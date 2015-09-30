#!/usr/bin/python3
import sys
import os
import collections
import timeit

INPUT_FILENAME = ""
FEATURE_VECTOR_FILENAME = ""
FEATURE_VECTOR_HANDLER = None
VOCAB_FILENAME = None
vocab = dict()

def handle_exception(message):
	print(message)
	sys.exit(1)

def remove_label():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME + "_label_removed"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			features = line.split()
			WRITE_HANDLER.write(" ".join(features[1:])+"\n")
		WRITE_HANDLER.close()
		print("Resultant file location :", OUTPUT_FILENAME)	
	except:
		raise
		#print("ERROR: Invalid input to remove label! Provide valid input to process")

"""
Splits the data for training and testing
e.g for Sentiment Data, it shuffles the data randomly and splits 18500/25000 of them as train and remaining 6500 as test data
"""
def split_data():
	try:
		shuffled_datafile = INPUT_FILENAME + "_shuffled"
		shuffle_cmd = "cat " + INPUT_FILENAME + " | shuf > " + shuffled_datafile
		os.system(shuffle_cmd)
		num_lines = sum(1 for line in open(shuffled_datafile))
		t_count = int(.75*num_lines)
		file1 = shuffled_datafile + ".75";
		data_split = "head -"+ str(t_count) + " " + shuffled_datafile + " > " + file1
		os.system(data_split)
		t_count = int(.25*num_lines)
		file2 = shuffled_datafile + ".25"
		data_split = "tail -"+ str(t_count) + " " + shuffled_datafile + " > " + file2
		os.system(data_split)
		print("INFO: Shuffled data and splited, results are stored in following files\n ",file1,"\n",file2)
	except:
		raise
		#print("ERROR: Invalid input to split data! Provide valid input to process")
	
def convert_to_feature_vector(c_name, file_path):
	try:
		feature_vector = dict()
		for line in open(file_path, 'r', encoding='latin1'):
			tokens = line.split()
			for token in tokens:
				if token in vocab:
					if vocab[token] in feature_vector: #feature_num in feature_vector				
						feature_vector[vocab[token]]+=1
					else:
						feature_vector[vocab[token]] = 1
		feature_vector = collections.OrderedDict(sorted(feature_vector.items()))
		if c_name is not None: FEATURE_VECTOR_HANDLER.write(c_name + " ")
		firstFeature = 1
		for feature,frequency in feature_vector.items():
			if firstFeature == 1:
				FEATURE_VECTOR_HANDLER.write(str(feature)+":"+str(frequency))
				firstFeature = 0
			else:
				FEATURE_VECTOR_HANDLER.write(" " +str(feature)+":"+str(frequency))
		FEATURE_VECTOR_HANDLER.write("\n")
	except:
		raise

def load_vocabulary():
	try:
		global VOCAB_FILENAME
		feature_num = 0
		for line in open(VOCAB_FILENAME, 'r', encoding="latin1"):
			vocab[line.strip()] = feature_num
			feature_num+=1
	except:
		raise

def create_feature_vector_test_data():
	try:
		load_vocabulary()
		global FEATURE_VECTOR_HANDLER
		ROOT_DIR = INPUT_FILENAME #directory containing all the files to be pre-processed
		FEATURE_VECTOR_HANDLER = open(FEATURE_VECTOR_FILENAME, 'w')
		for root, dirs, files in os.walk(ROOT_DIR): # gets all the files from subfolders recrsively
			for name in files:
				absolute_path = os.path.join(root, name)
				if os.path.isfile(absolute_path) and name != ".DS_Store":
					convert_to_feature_vector(None, absolute_path)
		FEATURE_VECTOR_HANDLER.close()
	except:
		raise

def create_feature_vector():
	try:
		load_vocabulary()
		global FEATURE_VECTOR_HANDLER
		ROOT_DIR = INPUT_FILENAME #directory containing all the files to be pre-processed
		FEATURE_VECTOR_HANDLER = open(FEATURE_VECTOR_FILENAME, 'w')
		for root, dirs, files in os.walk(ROOT_DIR): # gets all the files from subfolders recrsively
			for name in files:
				absolute_path = os.path.join(root, name)
				if os.path.isfile(absolute_path) and "Summary.txt" != name:
					class_name = os.path.basename(root)
					convert_to_feature_vector(class_name.upper(), absolute_path)
		FEATURE_VECTOR_HANDLER.close()
	except:
		raise

def add_target_megam():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME +"_megam_target.in"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			result = []
			features = line.split()
			f_w = " ".join(features)
			f_w = f_w.replace(":", " ")
			WRITE_HANDLER.write("1 " + f_w + "\n")
		WRITE_HANDLER.close()
		print("Labeled file location :", OUTPUT_FILENAME)
	except:
		raise

def add_target_svm():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME +"_svm_target.in"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			result = []
			features = line.split() 
			for feature in features: # change feeatures to start from 1
				f,w = feature.split(":")	
				result.append(str(int(f)+1) + ":" + w) # add +1 to features
			WRITE_HANDLER.write("+1 "+" ".join(result)+"\n")
		WRITE_HANDLER.close()
		print("Labeled file location :", OUTPUT_FILENAME)
	except:
		raise

def label_email_megam():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME +"_megam.in"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			result = []
			features = line.split()
			f_w = " ".join(features[1:])
			f_w = f_w.replace(":", " ")
			if(features[0] == "SPAM"):
				WRITE_HANDLER.write("1 " + f_w + "\n")
			else:
				WRITE_HANDLER.write("0 " + f_w + "\n")
		WRITE_HANDLER.close()
		print("Labeled file location :", OUTPUT_FILENAME)
	except:
		raise

def label_email_svm():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME +"_svm.in"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			result = []
			features = line.split() 
			for feature in features[1:]: # change feeatures to start from 1
				f,w = feature.split(":")	
				result.append(str(int(f)+1) + ":" + w) # add +1 to features
			if(features[0] == "SPAM"):
				WRITE_HANDLER.write("+1 "+" ".join(result)+"\n")
			elif(features[0] == "HAM"):
				WRITE_HANDLER.write("-1 "+" ".join(result)+"\n")
		WRITE_HANDLER.close()
		print("Labeled file location :", OUTPUT_FILENAME)
	except:
		raise

def label_sentiment_megam():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME +"_megam.in"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			result = []
			features = line.split()
			f_w = " ".join(features[1:])
			f_w = f_w.replace(":", " ")
			if((features[0].isdigit() and int(features[0])>=7) or features[0] == "POSITIVE"):
				WRITE_HANDLER.write("1 " + f_w + "\n")
			elif((features[0].isdigit() and int(features[0])<=4) or features[0] == "NEGATIVE"):
				WRITE_HANDLER.write("0 " + f_w + "\n")
		WRITE_HANDLER.close()
		print("Labeled file location :", OUTPUT_FILENAME)
	except:
		raise
	
def label_sentiment_svm():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME +"_svm.in"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			result = []
			features = line.split() 
			for feature in features[1:]: # change feeatures to start from 1
				f,w = feature.split(":")	
				result.append(str(int(f)+1) + ":" + w) # add +1 to features
			if((features[0].isdigit() and int(features[0])>=7) or features[0] == "POSITIVE"):
				WRITE_HANDLER.write("+1 "+" ".join(result)+"\n")
			elif((features[0].isdigit() and int(features[0])<=4) or features[0] == "NEGATIVE"):
				WRITE_HANDLER.write("-1 "+" ".join(result)+"\n")
		WRITE_HANDLER.close()
		print("Labeled file location :", OUTPUT_FILENAME)
	except:
		raise


def label_sentiment_nb():
	try:
		OUTPUT_FILENAME = INPUT_FILENAME + "_nb.in"
		WRITE_HANDLER = open(OUTPUT_FILENAME, 'w')
		for line in open(INPUT_FILENAME, 'r'):
			features = line.split() 
			if(int(features[0])>=7):
				WRITE_HANDLER.write("POSITIVE "+" ".join(features[1:])+"\n")
			elif(int(features[0])<=4):
				WRITE_HANDLER.write("NEGATIVE "+" ".join(features[1:])+"\n")
			else:
				WRITE_HANDLER.write(features+"\n")
		WRITE_HANDLER.close()
		print("Labeled file location :", OUTPUT_FILENAME)
	except:
		raise

def get_first_col():
	try:
		for line in open(INPUT_FILENAME, 'r'):
			features = line.split() 
			print(features[0])
	except:
		raise

try:
	start = timeit.default_timer()
	COMMAND = sys.argv[1] # list of commands {-label_sentiment_nb, -create_feature_vector, -split_data}
	INPUT_FILENAME = sys.argv[2]
	if COMMAND == "-split_data":
		split_data()
	elif COMMAND == "-label_sentiment_nb":
		label_sentiment_nb()
	elif COMMAND == "-label_sentiment_svm":
		label_sentiment_svm()
	elif COMMAND == "-label_sentiment_megam":
		label_sentiment_megam()
	elif COMMAND == "-label_email_svm":
		label_email_svm()
	elif COMMAND == "-label_email_megam":
		label_email_megam()
	elif COMMAND == "-add_target_svm":
		add_target_svm()
	elif COMMAND == "-add_target_megam":
		add_target_megam()
	elif COMMAND == "-create_feature_vector":	
		FEATURE_VECTOR_FILENAME = sys.argv[3]
		VOCAB_FILENAME = sys.argv[4]
		create_feature_vector()
	elif COMMAND == "-create_feature_vector_test":
		FEATURE_VECTOR_FILENAME = sys.argv[3]
		VOCAB_FILENAME = sys.argv[4]
		create_feature_vector_test_data()
	elif COMMAND == "-remove_label":
		remove_label()
	elif COMMAND == "-get_first_col":
		get_first_col()
	else:
		print("ERROR:Provide valid command options [-label_sentiment_nb, -create_feature_vector, -split_data, -remove_label, -label_sentiment_svm, -label_sentiment_megam, -create_feature_vector_test]")
	end = timeit.default_timer()
	#print("Total time taken:",str(end-start)+"s")
except Exception as e:
	handle_exception("ERROR: Invalid input! Provide valid input to process " + str(e))

