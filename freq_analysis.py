'''
Analyze most common attriubtes
'''
import operator
import sys,os,re
import fnmatch
import csv
import random
from collections import Counter

GOVTRACK_FILE = "govtrack.csv"
BILLS_PER_ORG = "bills_per_org_temp"
BILLS_PER_REP = "bills_per_rep_temp"
ORGS = "organizations.csv"
REPS = "congress_members/all_processed"
K = 10

def load_org_names():
	return_dict = dict()
        with open(ORGS, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                        return_dict[row[0]] = row[1]
        return return_dict

def load_rep_names():
        return_dict = dict()
        with open(REPS, 'r') as csvfile:
                reader = csv.reader(csvfile,delimiter= '\t')
                for row in reader:
			if not row[1] in return_dict.keys():
                        	return_dict[row[1]] = row[0]
        return return_dict

def load_bills(f_in):
	return_dict = dict()
	with open(f_in, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = '\t')
		for row in reader:
			for elem in eval(row[1]):
				return_dict[row[0]] = len(eval(row[1]))
				#if elem not in return_dict.keys():
				#	return_dict[elem] = set()
				#return_dict[elem].add(row[0])

	return return_dict

def load_bills_govtrack():
	return_dict = dict() 
	with open(GOVTRACK_FILE, 'r') as csvfile:
		reader = csv.reader(csvfile)
                reader.next()
		for row in reader:
                        key = row[0]+'th_' + row[2] + '=' + row[1]
			return_dict[key] = row[4]
                
        return return_dict

def freq_analysis():
	org_names = load_rep_names()	
	#rep_names = load_rep_names()
	
	bills_per_org = load_bills(BILLS_PER_REP)
	#bills_per_rep = load_bills(BILLS_PER_REP)
	#print bills_per_org
	sorted_bills = sorted(bills_per_org, key=bills_per_org.get)
	for org in sorted_bills[-100:]:
		print org_names[org] + ' ' + str(bills_per_org[org])

	#for org in bills_per_org:
		
	#experimental = Counter(list_output).most_common(1)[0][0]
	#theoretical =  bills_test[test_bill]
		
		#print experimental
		#print theoretical
		#corr = 'WRONG'
		#if int(theoretical) == int(experimental):
		#	corr = "RIGHT"
		#print corr	
		#fout.write(str(experimental)+'\t'+str(theoretical)+'\t'+corr+'\n')
	#fout.close()  
if __name__=='__main__':
        freq_analysis()
