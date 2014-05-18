'''
Grab data from govtrack api by Bill name
sample api call https://www.govtrack.us/api/v2/bill?number=4569&congress=105&format=csv&fields=congress,number,bill_type_label,is_alive,current_status,title_without_number
'''

import sys,os,re
import fnmatch
import csv
import urllib2

BILL_FILE = "bill_parsing_billtype.csv"
GOVTRACK_URI = 'https://www.govtrack.us/api/v2/bill/'
OUTPUT = 'govtrack_additional.csv'

def get_unique_bills():
        bill_names = set()
	with open(BILL_FILE, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
			# get only numerical part of bill name
			congress = get_num(row[0].split('_')[0])
			for bill in row[1].split(';'):
				bill_names.add(congress+'?'+bill)

        return bill_names

def get_data():	
	bill_names = get_unique_bills()
	f_out = open(OUTPUT,'w')
	f_out.write('congress,number,bill_type,is_alive,current_status,committees, cosponsors, current_status_date, current_status_description, introduced_date, sponsor, sponsor_role,title_without_number')
	f_out.write('\n')
	length = str(len(bill_names))
	counter = 0	
	for bill in bill_names:
		print str(counter) + ' of ' + length + ' processed'
		counter += 1
		#print bill
		try:
			f_out.write(get_govtrack(bill))
			f_out.write('\n')
		except:
			pass

	f_out.close()

def get_govtrack(bill):
	print bill
	q = bill.split('?')
	congress = q[0]
	equal = q[1].split('=')
	number= equal[1]
	bill_type = equal[0]
	#if bill_type != '':
	url = 'https://www.govtrack.us/api/v2/bill?number='+number+'&congress='+congress+'&bill_type='+bill_type+'&format=csv&fields=congress,number,bill_type,is_alive,current_status,committees,cosponsors,current_status_date,current_status_description,introduced_date,sponsor,sponsor_role,title_without_number'
	#print url
	data = urllib2.urlopen(url).read()	
	return data.split('\n')[1]
	#else:
	#	return ''

def get_num(x):	
	return ''.join(ele for ele in x if ele.isdigit())

if __name__=='__main__':
        get_data()
