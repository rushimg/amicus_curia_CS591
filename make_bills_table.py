'''
Cluster bills based on Rep names and Intrest groups
'''

import sys,os,re
import fnmatch
import csv

GOVTRACK_FILE = "govtrack.csv"
BILLS_PER_EMAIL = "bill_parsing_billtype.csv"
ORGS_PER_EMAIL = "org_parsing.csv"
REPS_PER_EMAIL = "reps_parsing.csv"
OUT_FILE = "bills.csv"

def make_bill_table():
	''' bills per email '''
	bills_per_email = dict()
	bills_per_reps = dict()
	bills_per_org = dict()

	with open(BILLS_PER_EMAIL, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		next(reader)
		for row in reader:
			congress = row[0].split('_')[0]
			semi_colon = row[1].split(';')				
			bills_per_email[row[0]]  = set()
			for s in semi_colon:
				if not( s == "" or s == ' '):
					s = congress +'_'+s
					#print s
					bills_per_email[row[0]].add(s)
	#print bills_per_email
		
	reps_per_email = dict()
        with open(REPS_PER_EMAIL, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
			semi_colon = row[2].split(';')                          
                        reps_per_email[row[0]]  = set()
                        for s in semi_colon:
				if not( s == "" or s == ' '):
                                	reps_per_email[row[0]].add(s)
	'''
	#print reps_per_email	
	orgs_per_email = dict()
        with open(ORGS_PER_EMAIL, 'rb') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)
                for row in reader:
			if not (row[0] == ''):
				semi_colon = row[2].split(';')
                        	orgs_per_email[row[0]]  = set()
                        	for s in semi_colon:
                                	if not((s == '') or (s == ' ')):
						orgs_per_email[row[0]].add(s)
        #print orgs_per_email
	'''
		
	for email in reps_per_email:
		#print email
		email_wo_slash = email[1:]
		bills = bills_per_email[email_wo_slash]
		orgs = reps_per_email[email]
		for org in orgs:
                       if not(org in bills_per_org.keys()):   
                               bills_per_org[org] = set()
                       bills_per_org[org] =  bills_per_org[org].union(bills)

		#for bill in bills:
		#	if not(bill in bills_per_org.keys()):	
		#		bills_per_org[bill] = set()
		#	bills_per_org[bill] =  bills_per_org[bill].union(orgs)
	print bills_per_org
	'''
	f = open('bills_per_org_temp','w')
	for bill in bills_per_org:
		if len(bills_per_org[bill]) > 0 :
			f.write(str(bill) +'\t' +str(bills_per_org[bill])+'\n')
	f.close()
		
	length = str(len(reps_per_email))
	counter = 0
	for email in reps_per_email:
		counter += 1
		print str(counter) + ' of ' + length
		email_wo_slash = email[1:]
		if (email in reps_per_email.keys()) and (email_wo_slash in bills_per_email.keys()):
			bills = bills_per_email[email_wo_slash]
			#print bills
			reps = reps_per_email[email]
               		#print reps
			for bill in bills:
                       		if len(reps) > 0:
					if not(bill in bills_per_reps.keys()):
                               			bills_per_reps[bill] = set()
                       			#print reps
					bills_per_reps[bill] =  bills_per_reps[bill].union(reps)
	print bills_per_reps
	'''
	f = open('bills_per_rep_temp','w')
        for bill in bills_per_org:
                if len(bills_per_org[bill]) > 0 :
			f.write(str(bill) +'\t' +str(bills_per_org[bill])+'\n')
        f.close()		
		
if __name__=='__main__':
        make_bill_table()
