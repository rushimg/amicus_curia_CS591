'''
Cluster bills based on Rep names and Intrest groups
'''

import sys,os,re
import fnmatch
import csv
import random
from collections import Counter

GOVTRACK_FILE = "govtrack.csv"
BILLS_PER_ORG = "bills_per_org_temp"
ORGS = "organizations.csv"
ORDER_STATUS = {
1: 'introduced',2: 'conference_passed_house',3: 'fail_second_house',4: 'referred',5: 'pass_back_house',6: 'passed_simpleres',7: 'vetoed_override_fail_originating_senate',8: 'reported',9: 'enacted_signed',10: 'override_pass_over_house',11: 'fail_second_senate',
12: 'pass_over_senate',
13: 'vetoed_pocket',
14: 'pass_back_senate',
15: 'passed_concurrentres',
16: 'passed_constamend',
17: 'fail_originating_house',
18: 'prov_kill_pingpongfail',
19: 'pass_back_senate',
20: 'prov_kill_veto',
21: 'pass_over_house',
22: 'prov_kill_cloturefailed', 
23: 'fail_originating_senate', 
24: 'vetoed_override_fail_second_house', 
25: 'prov_kill_suspensionfailed', 
26: 'override_pass_over_senate',
27: 'passed_bill',
28: 'enacted_tendayrule',
29: 'vetoed_override_fail_second_senate',
30: 'conference_passed_senate',
31: 'enacted_veto_override',
32: 'vetoed_override_fail_originating_house'}

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

def load_bills(f_in):
	return_dict = dict()
	with open(f_in, 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = '\t')
		for row in reader:
			return_dict[row[0]] = eval(row[1])
	return return_dict

def load_bills_govtrack():
	return_dict = dict() 
	with open(GOVTRACK_FILE, 'r') as csvfile:
		reader = csv.reader(csvfile)
                for row in reader:
                        key = row[0]+'th_' + row[2] + '=' + row[1]
			return_dict[key] = row[4]
                
        return return_dict

def priors(status_per_bill):
	freqs = Counter(status_per_bill.values())
	for stat in ORDER_STATUS:
		print ORDER_STATUS[stat] + ' ' + str(freqs[ORDER_STATUS[stat]])
	#clust_status = dict()
	#clust_status[0] = list()
	#clust_status[1] = list()
	#clust_status[2] = list()
	#for status in freqs:
	#	if STATUS_CLUSTER[status] == 1:
	#		clust_status[0].append(freqs[status]) 
	#	elif STATUS_CLUSTER[status] == 2:
	#		clust_status[1].append(freqs[status])
	#	else:
	#		clust_status[2].append(freqs[status])
	#print clust_status
#def train_test(status_per_bill,orgs_per_bill):
def features(bill,orgs_per_bill):
	return {'orgs': orgs_per_bill[bill] }

#def bills_per_feature(bill, orgs_per_bill)
	#return orgs_per_bill
def classify():
	orgs_per_bill = load_bills(BILLS_PER_ORG)
	status_per_bill = load_bills_govtrack()
	#print status_per_bill
	priors(status_per_bill)
	for bill in orgs_per_bill:
		print features(bill,orgs_per_bill)
if __name__=='__main__':
        classify()
