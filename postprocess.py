#!/usr/bin/python3
import sys

INPUT_FILENAME = ""

def handle_exception(message):
	print(message)
	sys.exit(1)

def label_sentiment_svm():
	try:
		final_result = []
		for line in open(INPUT_FILENAME, 'r'):
			result = line.rstrip()
			if float(result)>0:
				final_result.append("POSITIVE")
			else: #<0
				final_result.append("NEGATIVE")
		WRITE_HANDLER = open(INPUT_FILENAME, 'w')
		WRITE_HANDLER.write("\n".join(final_result))
		WRITE_HANDLER.close()
	except:
		raise

def label_email_svm():
	try:
		final_result = []
		for line in open(INPUT_FILENAME, 'r'):
			result = line.rstrip()
			if float(result)>0:
				final_result.append("SPAM")
			else: #<0
				final_result.append("HAM")
		WRITE_HANDLER = open(INPUT_FILENAME, 'w')
		WRITE_HANDLER.write("\n".join(final_result))
		WRITE_HANDLER.close()
	except:
		raise

def label_email_megam():
	try:
		final_result = []
		for line in open(INPUT_FILENAME, 'r'):
			result = line.rstrip().split()[0]
			if result.isdigit() and int(result) == 1:
				final_result.append("SPAM")
			else: #0
				final_result.append("HAM")
		WRITE_HANDLER = open(INPUT_FILENAME, 'w')
		WRITE_HANDLER.write("\n".join(final_result))
		WRITE_HANDLER.close()
	except:
		raise

def label_sentiment_megam():
	try:
		final_result = []
		for line in open(INPUT_FILENAME, 'r'):
			result = line.rstrip().split()[0]
			if result.isdigit() and int(result) == 1:
				final_result.append("POSITIVE")
			else: #0
				final_result.append("NEGATIVE")
		WRITE_HANDLER = open(INPUT_FILENAME, 'w')
		WRITE_HANDLER.write("\n".join(final_result))
		WRITE_HANDLER.close()
	except:
		raise

try:
	COMMAND = sys.argv[1] # list of commands {-label_sentiment_svm, -label_sentiment_megam, -label_email_megam, -label_email_svm}
	INPUT_FILENAME = sys.argv[2]
	if COMMAND == "-label_sentiment_svm":
		label_sentiment_svm()
	elif COMMAND == "-label_sentiment_megam":
		label_sentiment_megam()
	elif COMMAND == "-label_email_megam":
		label_email_megam()
	elif COMMAND == "-label_email_svm":
		label_email_svm()
	else:
		print("ERROR:Provide valid command options [-label_sentiment_svm, -label_sentiment_megam,-label_email_megam, -label_email_svm]")
except Exception as e:
	handle_exception("ERROR: Invalid input! Provide valid input to process " + str(e))
