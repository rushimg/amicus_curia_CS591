'''
k-Nearest Neighbors Classsifier
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
K = 2
OUTPUT_FILE = "knn_reps_"+ str(K) +".csv"
STATUS_CLUSTER = {
'introduced':1,
'conference_passed_house':1,
'fail_second_house':1,
'referred':1,
'pass_back_house':2,
'passed_simpleres':2,
'vetoed_override_fail_originating_senate':2,
'reported':2,
'enacted_signed':2,
'override_pass_over_house':2,
'fail_second_senate':2,
'pass_over_senate':2,
'vetoed_pocket':2,
'pass_back_senate':2,
'passed_concurrentres':2,
'passed_constamend':2,
'fail_originating_house':2,
'prov_kill_pingpongfail':2,
'pass_back_senate':2,
'prov_kill_veto':2,
'pass_over_house':3,
'prov_kill_cloturefailed':3,
'fail_originating_senate':3,
'vetoed_override_fail_second_house':3,
'prov_kill_suspensionfailed':3,
'override_pass_over_senate':3,
'passed_bill':3,
'enacted_tendayrule':3,
'vetoed_override_fail_second_senate':3,
'conference_passed_senate':3,
'enacted_veto_override':3,
'vetoed_override_fail_originating_house':3}


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
                        return_dict[row[1]] = 'rep_'+row[0]
        return return_dict

def load_bills(f_in):
	return_dict = dict()
	with open(f_in, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = '\t')
		for row in reader:
			for elem in eval(row[1]):
				if elem not in return_dict.keys():
					return_dict[elem] = set()
				return_dict[elem].add(row[0])

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

def jdist(a,b):
	union = a.union(b)
	inter = a.intersection(b)
	len_union = float(len(union))
	len_inter = float(len(inter))
	jsim = len_inter/len_union
	jdist = 1-jsim
	return jdist

def l2_dist(a,b):
	# treat the set of bills as binary feature vectors
	dist = 0
	for elem in a:
		if not(elem in b):
			dist = dist+1
	for elem in b:
		 if not(elem in a):
                        dist = dist+1
	return dist

def knn():
	#bills_per_org = load_bills(BILLS_PER_ORG)
	#bills_per_rep = load_bills(BILLS_PER_REP)
	#print bills_per_rep
	#fout = open('knn_cache_rep','w')
	#fout.write(str(bills_per_rep))
	#fout.close()
	#bills = dict(bills_per_org.items() + bills_per_rep.items())
	
	bills_per_rep = eval(open('knn_cache_rep','r').read())
	bills_per_org = eval(open('knn_cache_org','r').read())
	orgs = load_org_names()
        reps = load_rep_names()
	print bills_per_rep
	bills_govtrack = load_bills_govtrack()
	bills_train = dict()
	bills_test = dict()
	for bill in bills_govtrack:
		if bill.startswith('112'):
			bills_test[bill] = STATUS_CLUSTER[bills_govtrack[bill]]
		else:
			bills_train[bill] = STATUS_CLUSTER[bills_govtrack[bill]]
	#print bills_train
	#print len(bills_test)
	#print len(bills_train)
	fout= open(OUTPUT_FILE,'w')
	length = str(len(bills_test))
	counter = 0
	for test_bill in bills_test:
		print str(counter) + ' of ' + length
 		counter += 1 
		distances_dict = dict()
		for train_bill in bills_train:
			#print train_bill
			#print bills_per_rep.keys	
			if (train_bill in bills_per_rep.keys() and test_bill in bills_per_rep.keys()):
				distances_dict[train_bill] = jdist(bills_per_rep[test_bill],bills_per_rep[train_bill])
				#print "F"
			#else:
				#print "NF"
		sorted_x = sorted(distances_dict.iteritems(), key=operator.itemgetter(1))	
		neighbors = sorted_x[0:K]
		list_output = list()
		# find most frequent output
		for ne in neighbors:
			list_output.append(bills_train[ne[0]])
		#print Counter(list_output).most_common(1)	
		
		experimental = Counter(list_output).most_common(1)[0][0]
		theoretical =  bills_test[test_bill]
		
		#print experimental
		#print theoretical
		corr = 'WRONG'
		if int(theoretical) == int(experimental):
			corr = "RIGHT"
		#print corr	
		fout.write(str(experimental)+'\t'+str(theoretical)+'\t'+corr+'\n')
	fout.close()  
if __name__=='__main__':

        knn()
