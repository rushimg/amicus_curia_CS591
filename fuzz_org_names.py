'''
Fuzzy matching for organization names
Reads organization names in from CSV file 
uses fuzzy matching techniquese to match orgnames present in the emails to ones provided in DB

'''

import sys,os,re
import fnmatch
import csv

MATCH = "*.txt_*"
DIR_NAME = "emails/emails/"
OUT_FILE = "org_parsing.csv"
ORG_NAMES_FILE = 'organizations.csv'


def read_org_names():
	org_names_dict = dict()
	with open(ORG_NAMES_FILE, 'r') as csvfile:
		reader = csv.reader(csvfile)
	     	for row in reader:
        		org_names_dict[row[0]] = row[1].lower()
	return org_names_dict

def process_files():
        org_names = read_org_names()
	
	matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))
	
	f_out = open(OUT_FILE,'w')
        f_out.write('file_name'+','+'org_names'+','+'org_ids'+'\n')
	
        for match in matches:
                print match
                parse_file(match,f_out,org_names)
	f_out.close()
	
''' parse individual files '''
def parse_file(file_in,f_out,org_names):
	f = open(file_in, 'r')
	email = f.read()

	temp_email_dict = dict()
	email = 'From:' + email # we need to add this back in bc when we split on it we removed it
	#email = email.lower()
	spaces = email.split(' ')
	temp_email_dict['org_names'] = ''
	temp_email_dict['org_keys'] = ''
	input_f_name = file_in.replace(DIR_NAME,'')
	temp_email_dict['file_name'] = input_f_name	
	email = email.replace(',',' , ').replace('.',' . ') # allows for better parsing
	#for space in spaces:
	#	space = space.lower()
	
	for org_key in org_names:
		if (' ' + org_names[org_key].title() + ' '  in email):
			temp_email_dict['org_names'] += ';' + org_names[org_key]
			temp_email_dict['org_keys'] += ';' + org_key
	
	# remove leading ';'
	temp_email_dict['org_names'] =  temp_email_dict['org_names'][1:]
	temp_email_dict['org_keys'] =  temp_email_dict['org_keys'][1:]
	 
			
	#print temp_email_dict
	write_to_file(temp_email_dict,f_out)

def write_to_file(email_dict,f_out):
	f_out.write(email_dict['file_name']+','+email_dict['org_names'] +',' + email_dict['org_keys'] +'\n') 

def clean_text(raw_text):
	clean_text = raw_text.replace('  ',' ')
	clean_text = clean_text.replace('  ',' ')
	clean_text = clean_text.replace('\t',' ')
	clean_text = clean_text.replace('\r',' ')
	clean_text = clean_text.replace('  ',' ')
	return clean_text

if __name__=='__main__':
        process_files()
