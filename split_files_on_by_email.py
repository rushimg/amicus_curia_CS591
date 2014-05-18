'''
Python script to split the larger emails file into seprate files for each eamil, to be later used with the NER
'''


import sys,os,re
import fnmatch
import xml.etree.ElementTree as ET

MATCH = "*.txt"
DIR_NAME = "../../../../Dropbox/cs 591 - dear colleagues text/Emails"
OUT_DIR_NAME = "emails/emails/"
EMAIL_SPLIT = 'From:'

def split_files():
        matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))

        for match in matches:
                print match
                split_file(match)

def split_file(file_in):
	f = open(file_in, 'r')
	input_f_name = file_in.replace(DIR_NAME+'/','')
	input_f_name = input_f_name.replace(' ','_') 
	text = (f.read()).decode("ascii", "ignore")
	emails = text.split(EMAIL_SPLIT)
	email_counter = 0
	for email in emails:
		temp_f = open(OUT_DIR_NAME+input_f_name+'_'+str(email_counter), 'w')
		email = email.replace('>','')
		temp_f.write(email)
		temp_f.close()
		email_counter += 1

if __name__=='__main__':
        split_files()
