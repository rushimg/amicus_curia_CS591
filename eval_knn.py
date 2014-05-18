'''
EVALUATE KNN
'''

import sys,os,re
import fnmatch
import csv
def evaluate(file_in):
        with open(file_in, 'r') as csvfile:
                reader = csv.reader(csvfile,delimiter= '\t')
                correct = 0
		total = 0
		baseline = 0
		for row in reader:
                        total += 1 
			if row[2] == 'RIGHT':
				correct += 1
			if row[1] == '1' and row[1] == '1':
				baseline += 1
        print "Accuracy : " + str(float(correct)/float(total))
	print "Baseline : " + str(float(baseline)/float(total))
	
if __name__=='__main__':
        evaluate(sys.argv[1])
