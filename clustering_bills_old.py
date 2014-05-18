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
K = 500
OUT_FILE = "CLUSTERS_"+ str(K) +".txt"

def load_org_names():
	return_dict = dict()
        with open(ORGS, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                        return_dict[row[0]] = row[1]
        return return_dict

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
			return_dict[key] = row[5]
                
        return return_dict

def jdist(a,b):
	union = a.union(b)
	inter = a.intersection(b)
	len_union = float(len(union))
	len_inter = float(len(inter))
	jsim = len_inter/len_union
	jdist = 1-jsim
	return jdist

def cluster():
	bills_per_org = load_bills(BILLS_PER_ORG)
	bills_govtrack = load_bills_govtrack()
	#print bills_govtrack
	orgs = load_org_names()
	#print bills_per_org
	k_means(bills_per_org,bills_govtrack,orgs)

def k_means(in_dict,bills_govtrack,orgs):
	centroids_dict = dict()
	clusters_dict = dict()
	# initialize
	for j in range(0,K):
		rand = random.randrange(len((in_dict)))
		clusters_dict[j] = list()
		centroids_dict[j] = in_dict.values()[rand]
	#print centroids_dict		
	for j in range(0,25):
		
		# assignment step
		for bill in in_dict:
			temp_dict_centroids = dict()
			for i in range(0,K):
				# assignment step
				temp_dict_centroids[jdist(in_dict[bill],centroids_dict[i])] = i
			
			min_centroid = temp_dict_centroids[min(temp_dict_centroids.keys())]
			clusters_dict[min_centroid].append(bill)

		# update step
		
		for cluster in clusters_dict:
			#print cluster	
			#print clusters_dict[cluster]
			orgs_list = list()
			average_len = 0
			for elem in clusters_dict[cluster]:
				
				orgs_list+=(list(in_dict[elem]))
				average_len += len(in_dict[elem])
			#print len(clusters_dict[cluster])	
			try:
				average_length = average_len/len(clusters_dict[cluster])
				c = Counter(orgs_list)
				common = c.most_common(average_length)
                        	temp_set = set()
				for e in common:
					temp_set.add(e[0]) 
				centroids_dict[cluster] = temp_set
				#print centroids_dict[cluster]
			except ZeroDivisionError:
				centroids_dict[cluster] = in_dict.values()[rand]
		
				
					
			#centroids_dict[cluster] = max(set(clusters_dict[cluster]), key=clusters_dict[cluster].count)

	#print clusters_dict
	#print centroids_dict
	for cluster in clusters_dict:
		print "--------cluster----------------"
		print len(clusters_dict[cluster])
		#for centroid in centroids_dict[cluster]:
		#	print orgs[centroid]	
		
		for bill in clusters_dict[cluster]:
			try:
				print bills_govtrack[bill]
			except:
				pass
if __name__=='__main__':

        cluster()
