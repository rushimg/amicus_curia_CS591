'''
Grab bill names present in each email
'''

import sys,os,re
import fnmatch
import csv

MATCH = "*.txt_*"
DIR_NAME = "emails/emails/"
OUT_FILE = "bill_parsing_billtype.csv"

#PREFIXES = ['HR','H.R.','S.','S','S.Res.','SRes', 'H.Res.', 'HRes', 'S.J.Res.','H.J.Res.''SJRes','HJRes','S.Con.Res.','SConRes','H.Con.Res.','HConRes','P.L.','PL','Amdt','Amdt.', 'H.Amdt.','HAmdt','S.Amdt.','SAmdt']

PREFIXES = {
'HR':'house_bill',
'H.R.':'house_bill',
'S.':'senate_bill',
'S':'senate_bill',
'S.Res.':'senate_joint_resolution',
'SRes':'senate_joint_resolution', 
'H.Res.':'house_resolution', 
'HRes':'house_resolution', 
'S.J.Res.':'senate_joint_resolution',
'H.J.Res.':'house_joint_resolution',
'SJRes':'senate_joint_resolution',
'HJRes':'house_joint_resolution',
'S.Con.Res.':'senate_concurrent_resolution',
'SConRes':'senate_concurrent_resolution',
'H.Con.Res.':'house_concurrent_resolution',
'HConRes':'house_concurrent_resolution',
'P.L.':'','PL':'','Amdt':'','Amdt.':'', 'H.Amdt.':'','HAmdt':'','S.Amdt.':'','SAmdt':''}

def process_files():	
	matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))
	
	f_out = open(OUT_FILE,'w')
        f_out.write('file_name'+','+'bills'+'\n')
	length = str(len(matches))	
        counter = 0
	for match in matches:
                print str(counter) + ' of ' + length
		counter += 1
                parse_file(match,f_out)
	f_out.close()
	
''' parse individual files '''
def parse_file(file_in,f_out):
	f = open(file_in, 'r')
	email = f.read()

	temp_email_dict = dict()
	email = 'From:' + email # we need to add this back in bc when we split on it we removed it
	#email = email.lower()
	spaces = email.split(' ')
	temp_email_dict['bills'] = ''
	input_f_name = file_in.replace(DIR_NAME,'')
	temp_email_dict['file_name'] = input_f_name	
	#email = email.replace(',',' , ').replace('.',' . ') # allows for better parsing
	#for space in spaces:
	#	space = space.lower(u)
	email = email.replace('(',' ( ')
	email = email.replace(')',' ) ')

	spaces = email.split(' ')
	space_counter = 0
	for space in spaces:
		if space in PREFIXES.keys():
			bill_num = re.findall(r'\d+',spaces[space_counter + 1])
			if bill_num:
				temp_email_dict['bills'] += (';' + (PREFIXES[space] +'='+ bill_num[0]))
			#temp_email_dict['bills'] += (';' + (space))
		space_counter+=1
	
	# remove leading ';'
	temp_email_dict['bills'] =  temp_email_dict['bills'][1:]
	 
			
	#print temp_email_dict
	write_to_file(temp_email_dict,f_out)

def write_to_file(email_dict,f_out):
	f_out.write(email_dict['file_name']+','+email_dict['bills'] +'\n') 

def clean_text(raw_text):
	clean_text = raw_text.replace('  ',' ')
	clean_text = clean_text.replace('  ',' ')
	clean_text = clean_text.replace('\t',' ')
	clean_text = clean_text.replace('\r',' ')
	clean_text = clean_text.replace('  ',' ')
	return clean_text

if __name__=='__main__':
        process_files()
