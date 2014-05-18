'''
Cluster bills based on Rep names and Intrest groups
'''

import sys,os,re
import fnmatch
import csv
import random
from collections import Counter

GOVTRACK_FILE = "govtrack.csv"
BILLS_PER_ORG = "bills_per_rep_temp"
#ORGS = "organizations.csv"
REPS = "congress_members/all_processed"
K = 5
OUT_FILE = "clust_rep_"+ str(K) +".csv"

def load_org_names():
	return_dict = dict()
        with open(REPS, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter = '\t')
                for row in reader:
                        return_dict[row[1]] = row[0]
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
	old_centroids_dict = dict()
	# initialize
	for j in range(0,K):
		rand = random.randrange(len((in_dict)))
		clusters_dict[j] = list()
		centroids_dict[j] = in_dict.values()[rand]
	#print centroids_dict		
	#print clusters_dict
	#j = 0
	#CONV = False
	for j in range(0,10):
		#j += 1	
		print "Iteration # " + str(j)		
		# assignment step
		for bill in in_dict:
			temp_dict_centroids = dict()
			for i in range(0,K):
				temp_dict_centroids[l2_dist(in_dict[bill],centroids_dict[i])] = i
			
			min_centroid = temp_dict_centroids[min(temp_dict_centroids.keys())]
			clusters_dict[min_centroid].append(bill)
		#print clusters_dict
	
		# update step
			
		for cluster in clusters_dict:
			#print cluster	
			#print clusters_dict[cluster]
			orgs_list = list()
			distances = dict()	
			for elem in clusters_dict[cluster]:
				# find mediod
				distances[elem] = 0
				for elem2 in clusters_dict[cluster]:
					#if elem2 not in distances.keys():
					#	distances[elem2] = 0
					#distances[elem2] += l2_dist(elem,elem2)
					distances[elem] += l2_dist(elem,elem2)

			inv_map = {v:k for k, v in distances.items()}
			#print "inv_map" + str(inv_map)
			#print "dist" + str(distances)
			temp = inv_map[min(distances.values())]
			centroids_dict[cluster] = temp
			inv_map = None
			#if (set(centroids_dict.values()).intersection(set(old_centroids_dict.values())/(set(centroids_dict.values()).union(set(old_centroids_dict.values())
			#)) == (len(centroids_dict) + len(old_centroids_dict)):
			#	CONV = True
			#old_centroids_dict = centroids_dict
				
	#print centroids_dict
	fout = open(OUT_FILE,'w')
	for cluster in clusters_dict:
		#print "--------cluster----------------"
		print len(clusters_dict[cluster])
		#for centroid in centroids_dict[cluster]:
		#	print orgs[centroid]	
		for org in clusters_dict[cluster]:
			fout.write(orgs[org]+ '\t' + str(org) + '\t' + str(cluster) + '\n')
			#print orgs[org]
	fout.close()
if __name__=='__main__':
        cluster()
