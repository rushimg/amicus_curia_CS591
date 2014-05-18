'''
Fuzzy matching for representative  names
Reads rep names in from CSV file 
uses fuzzy matching techniquese to match orgnames present in the emails to ones provided in DB

'''

import sys,os,re
import fnmatch
import csv

MATCH = "*.txt_*"
DIR_NAME = "emails/emails"
OUT_FILE = "reps_parsing.csv"


def read_org_names(in_file):
	rep_names_dict = dict()
	with open(in_file, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
	     	counter = 0;
		for row in reader:
			counter+=1 
			if row[1] not in rep_names_dict.keys():
				rep_names_dict[row[1]] = set()
        		rep_names_dict[row[1]].add(row[0])
	#print rep_names_dict
	return rep_names_dict

def process_files():
	''' dictionaries of dictionaries of rep names'''
	rep_names_dict_of_dict = dict()
	
        rep_names_dict_of_dict['105'] = read_org_names('congress_members/all_processed')
	rep_names_dict_of_dict['106'] = read_org_names('congress_members/all_processed')
	rep_names_dict_of_dict['107'] = read_org_names('congress_members/all_processed')
	rep_names_dict_of_dict['108'] = read_org_names('congress_members/all_processed')
	rep_names_dict_of_dict['109'] = read_org_names('congress_members/all_processed')
 	rep_names_dict_of_dict['110']= read_org_names('congress_members/all_processed')
	rep_names_dict_of_dict['111'] = read_org_names('congress_members/all_processed')
	rep_names_dict_of_dict['112'] = read_org_names('congress_members/all_processed')
	
	matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))
	
	f_out = open(OUT_FILE,'w')
        f_out.write('file_name'+','+'rep_names'+','+'rep_ids'+'\n')
	
        for match in matches:
                print match
                parse_file(match,f_out,rep_names_dict_of_dict)
	f_out.close()
	
''' parse individual files '''
def parse_file(file_in,f_out,rep_names_dict_of_dict):
	f = open(file_in, 'r')
	email = f.read()

	temp_email_dict = dict()
	email = 'From:' + email # we need to add this back in bc when we split on it we removed it
	#email = email.lower()
	spaces = email.split(' ')
	temp_email_dict['rep_names'] = set()
	temp_email_dict['rep_keys'] = set()
	input_f_name = file_in.replace(DIR_NAME,'')
	temp_email_dict['file_name'] = input_f_name	
	email = email.replace(',',' , ').replace('.',' . ') # allows for better parsing
	#for space in spaces:
	#	space = space.lower()
	congress = file_in.split('/')[2].split('_')[0].replace('th','')
	''' search for rep names by congress '''
	for key in rep_names_dict_of_dict[congress]:
		for alias in (rep_names_dict_of_dict[congress][key]):
			if alias in email:
				temp_email_dict['rep_names'].add(alias) #+= ';' + alias
				temp_email_dict['rep_keys'].add(key)  #+= ';' + key
	
	# remove leading ';'
	#temp_email_dict['rep_names'] =  temp_email_dict['rep_names'][1:]
	#temp_email_dict['rep_keys'] =  temp_email_dict['rep_keys'][1:]
	 
			
	#print temp_email_dict
	write_to_file(temp_email_dict,f_out)

def write_to_file(email_dict,f_out):
	rep_names_str = ''
	#if len(email_dict['rep_names']) > 0:
	for rep in email_dict['rep_names']:
		rep_names_str += ';' + rep
	rep_names_str = rep_names_str[1:]
	rep_keys_str = ''
	#if len(email_dict['rep_keys']) > 0:
       	for rep in email_dict['rep_keys']:
               	rep_keys_str += ';' + rep
	rep_keys_str = rep_keys_str[1:]
	
	f_out.write(email_dict['file_name']+','+rep_names_str +',' + rep_keys_str +'\n') 

def clean_text(raw_text):
	clean_text = raw_text.replace('  ',' ')
	clean_text = clean_text.replace('  ',' ')
	clean_text = clean_text.replace('\t',' ')
	clean_text = clean_text.replace('\r',' ')
	clean_text = clean_text.replace('  ',' ')
	return clean_text

if __name__=='__main__':
        process_files()
