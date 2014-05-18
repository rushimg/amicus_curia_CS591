'''
Basic text parser, to parse out the To/From/Subject/Congress/Session/Context data out of the emails
'''

import nltk
import sys,os,re
import fnmatch
import xml.etree.ElementTree as ET

MATCH = "*.txt"
DIR_NAME = "../../../../Dropbox/cs 591 - dear colleagues text/Emails"
OUT_FILE = "basic_parsing.csv"
EMAIL_SPLIT = 'From:'

def process_files():
        matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))

        for match in matches:
                print match
                parse_file(match)

''' parse individual files '''
def parse_file(file_in):
	f = open(file_in, 'r')
	input_f_name = file_in.replace(DIR_NAME+'/','')
	text = f.read()
	emails = text.split(EMAIL_SPLIT)
	parse_email(emails,input_f_name)
	#print emails[20]	

''' parse individual emails '''
def parse_email(email_list,file_name):
	
	for email in email_list:
		temp_email_dict = dict()
		email = 'From:' + email # we need to add this back in bc when we split on it we removed it
		lines = email.split('\n')
		temp_email_dict['content'] = ''
		#print lines[len(lines)-1]
               	spaces = file_name.split(' ')
                temp_email_dict['congress'] = spaces[0].replace('th','')
                temp_email_dict['session'] = (spaces[1].replace('nd','')).replace('st','')
		for line in lines:
			line  = clean_text(line)
			if 'From:' in line:
				temp_email_dict['from'] = line.replace('From:','')
			elif 'Sent:' in line:
				temp_email_dict['sent'] = line.replace('Sent:','')
			
			elif 'To:' in line:
				temp_email_dict['to'] = line.replace('To:','')
			
			elif 'Subject:' in line:
				temp_email_dict['subject'] = line.replace('Subject:','')
			else:
				temp_email_dict['content'] += line+' ' 
			
		#print temp_email_dict
		write_to_file(temp_email_dict)

def write_to_file(email_dict):
	f_out = open(OUT_FILE,'w')
	f_out.write(email_dict['from'] +',' + email_dict['sent'] +',' + email_dict['to'] +',' + email_dict['subject'] +',' + email_dict['congress'] +',' + email_dict['from'] + '\n')
	f_out.close()

def clean_text(raw_text):
	clean_text = raw_text.replace('  ',' ')
	clean_text = clean_text.replace('  ',' ')
	clean_text = clean_text.replace('\t',' ')
	clean_text = clean_text.replace('\r',' ')
	clean_text = clean_text.replace('  ',' ')
	return clean_text

if __name__=='__main__':
        process_files()
