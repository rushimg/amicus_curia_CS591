'''
Basic text parser, to parse out the To/From/Subject/Congress/Session/Context data out of the emails
'''

import nltk
import sys,os,re
import fnmatch
import xml.etree.ElementTree as ET
import nltk.data
from nltk import FreqDist
from senti_classifier import senti_classifier

MATCH = "*session*"
DIR_NAME = "emails/emails/"
OUT_DIR_NAME = "emails/sentiment_emails/"

def process_files():
        matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))

	out_f = open(OUT_DIR_NAME+'nltk_sentiments','r')
        # stop from processing same files if rerun
	for line in out_f.readlines():
		matches.remove(line.split(',')[0])
	out_f.close()
	
	out_f = open(OUT_DIR_NAME+'nltk_sentiments','a')
	for match in matches:
		print match

		f = open(match, 'r')
		text = f.readlines()
		pos_score, neg_score = senti_classifier.polarity_scores(text)
    		netScore = pos_score - neg_score
    		print netScore
		out_f.write(match +',' + str(netScore) +'\n')
 
if __name__=='__main__':
        process_files()
