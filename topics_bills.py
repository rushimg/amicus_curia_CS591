'''
Setup for LDA model on Bill titles
python topics_bills.py | tee lda_bill_titles.txt to get topics to files with words and probabilities
'''

import logging
import sys,os,re
import fnmatch
import csv
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
IN_FILE = "govtrack.csv"
OUT_FILE = "lda_bill_titles.txt"

def read_bill_titles():
	
	bill_titles_dict = dict()
	with open(IN_FILE, 'r') as csvfile:
		reader = csv.reader(csvfile)
	     	counter = 0;

		for row in reader:
			counter+=1 
        		bill_titles_dict[str(counter)] = row[5]
		row[1] = None # remove header row
	return bill_titles_dict

def process_files():
	bill_names = read_bill_titles()
	documents= bill_names.values()
	# http://radimrehurek.com/gensim/tut1.html
	stoplist = stopwords.words("english")
	texts = [[word for word in document.lower().split() if word not in stoplist] for document in documents]
	all_tokens = sum(texts, [])
	tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
	texts = [[word for word in text if word not in tokens_once] for text in texts]
		
	dictionary = corpora.Dictionary(texts)
	
	corpus = [dictionary.doc2bow(text) for text in texts]
	#print corpus
		
	#print corpus
	#print "running lda"
	lda = models.ldamodel.LdaModel(corpus, id2word=dictionary,  num_topics=25)  # train model
	#http://radimrehurek.com/gensim/models/ldamodel.html
	lda.print_topics(25)
	
	#print(lda[doc_bow]) 
	'''
	words = get_all_words(bill_names)
	
	f_out = open(OUT_FILE,'w')
	
	for key in bill_names:
		for w in bill_names[key].split(' ' ):
			 
	'''
	
''' parse individual files '''
def parse_file(file_in,f_out,rep_names_dict_of_dict):
	f = open(file_in, 'r')
	email = f.read()

	temp_email_dict = dict()
	email = 'From:' + email # we need to add this back in bc when we split on it we removed it
	#email = email.lower()
	spaces = email.split(' ')
	temp_email_dict['rep_names'] = ''
	temp_email_dict['rep_keys'] = ''
	input_f_name = file_in.replace(DIR_NAME,'')
	temp_email_dict['file_name'] = input_f_name	
	email = email.replace(',',' , ').replace('.',' . ') # allows for better parsing
	#for space in spaces:
	#	space = space.lower()
	congress = file_in.split('/')[2].split('_')[0].replace('th','')
	''' search for rep names by congress '''
	for key in rep_names_dict_of_dict[congress]:
		if (rep_names_dict_of_dict[congress][key]  in email):
			temp_email_dict['rep_names'] += ';' + rep_names_dict_of_dict[congress][key]
			temp_email_dict['rep_keys'] += ';' + key
	
	# remove leading ';'
	temp_email_dict['rep_names'] =  temp_email_dict['rep_names'][1:]
	temp_email_dict['rep_keys'] =  temp_email_dict['rep_keys'][1:]
	 
			
	#print temp_email_dict
	write_to_file(temp_email_dict,f_out)



if __name__=='__main__':
        process_files()
