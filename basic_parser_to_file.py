'''
Basic text parser, to parse out the To/From/Subject/Congress/Session/Context data out of the emails
We will run this on the already split emails in the emails directory so that we can accuraty keep pointers to which emails contain which data.
Same as basic parser but will write output to text

'''

import nltk
import sys,os,re
import fnmatch
import xml.etree.ElementTree as ET

MATCH = "*.txt_*"
#DIR_NAME = "../../../../Dropbox/cs 591 - dear colleagues text/Emails"
DIR_NAME = "emails/emails/"
OUT_FILE = "basic_parsing.csv"
EMAIL_SPLIT = 'From:'

def process_files():
        matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))
	
	f_out = open(OUT_FILE,'w')
        f_out.write('file_name'+','+'from' +',' + 'sent' +',' + 'to' +',' + 'subject' +',' + 'congress' +',' + 'session' + '\n')


        for match in matches:
                print match
                parse_file(match,f_out)
	f_out.close()
''' parse individual files '''
def parse_file(file_in,f_out):
	f = open(file_in, 'r')
	input_f_name = file_in.replace(DIR_NAME,'')
	email = f.read()

	temp_email_dict = dict()
	email = 'From:' + email # we need to add this back in bc when we split on it we removed it
	lines = email.split('\n')
	temp_email_dict['from'] = ''
	temp_email_dict['sent'] = ''
	temp_email_dict['to'] = ''
	temp_email_dict['subject'] = ''
	temp_email_dict['content'] = ''
	#print lines[len(lines)-1]
	spaces = input_f_name.split('_')
	temp_email_dict['file_name'] = input_f_name
	temp_email_dict['congress'] = (spaces[0].replace('th',''))
	temp_email_dict['session'] = (spaces[1].replace('nd','')).replace('st','')
	for line in lines:
		line  = clean_text(line)
		if 'From:' in line:
			temp_email_dict['from'] = (line.replace('From:','')).replace(',',' ')
		
		elif 'Sent By:' in line:
                        temp_email_dict['from'] += (';' + (line.replace('Sent By:','')).replace(',',' ').split('RE:')[0]) 

		elif 'Sent:' in line:
			temp_email_dict['sent'] = (line.replace('Sent:','')).replace(',',' ')
		elif 'Date:' in line:
			temp_email_dict['sent'] = (line.replace('Date:','')).replace(',',' ')
		

		elif 'To:' in line:
			temp_email_dict['to'] = (line.replace('To:','')).replace(',',' ')
		elif 'Cc:' in line:
                        temp_email_dict['to'] += (';' + (line.replace('Cc:','')).replace(',',' '))	
			
		elif 'Subject:' in line:
			temp_email_dict['subject'] = (line.replace('Subject:','')).replace(',',' ')
		if ('RE:' in line) and not("WHERE:" in line):
                        temp_email_dict['subject'] += (';' + (line.split('RE:')[1]))

		else:
			temp_email_dict['content'] += line+' ' 
			
		#print temp_email_dict
	write_to_file(temp_email_dict,f_out)

def write_to_file(email_dict,f_out):
	f_out.write(email_dict['file_name']+','+email_dict['from'] +',' + email_dict['sent'] +',' + email_dict['to'] +',' + email_dict['subject'] +',' + email_dict['congress'] +',' + email_dict['session'] + '\n')

def clean_text(raw_text):
	clean_text = raw_text.replace('  ',' ')
	clean_text = clean_text.replace('  ',' ')
	clean_text = clean_text.replace('\t',' ')
	clean_text = clean_text.replace('\r',' ')
	clean_text = clean_text.replace('  ',' ')
	return clean_text

if __name__=='__main__':
        process_files()
