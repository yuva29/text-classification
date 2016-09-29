# Binary Text Classification 

Classify a cluster of documents into different classes using Naive Bayes Classifier

The goal is to perform binary classification: SPAM or HAM (not spam), and POSITIVE or NEGATIVE using naive bayes classification techinique and comapre the results with maximum entropy modeling, and support vector machines(MegaM and SVM-Light). 

Dataset : IMDB movie reviews

The following data representation is used for training the model:

For training and development data, the first item will be a label for the example. For spam detection, it will be either SPAM or HAM where HAM refers to not spam. For sentiment detection, it will be either POSITIVE or NEGATIVE. Following the label will be a list of features and values for that example. The features correspond to the tokens present in the example which will be represented by their unique identifiers and listed in increasing order. The value of a feature will be the count of how many times that token appears in the example. The feature and value should be separated by ":".

So for a movie review, each feature would correspond to a token followed by ":" followed by the count of that token in the movie review. If "1" corresponded to "the", then "1:38" means that "the" appeared 38 times. If "2" corresponded to "a", then "2:10" means that "a" appeared 10 times.

The next line in the data file will correspond to a different example. It may have a different number of features since it may contain different tokens. For test data, the format will be the same except that there will be no LABEL.

LABEL FEATURE_NAME1:FEATURE_VALUE1 FEATURE_NAME2:FEATURE_VALUE_2 ... FEATURE_NAME_Q:FEATURE_VALUE_Q

