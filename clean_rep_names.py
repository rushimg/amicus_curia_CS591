'''
Clean Congress member names to be used in parsing
'''

import sys,os,re
import fnmatch
import csv

MATCH = "*raw*"
DIR_NAME = "congress_members/"
OUT_FILE = "bill_parsing.csv"


def process_files():	
	matches = []
        for root, dirnames, filenames in os.walk(DIR_NAME):
                for filename in fnmatch.filter(filenames, MATCH):
                        matches.append(os.path.join(root, filename))
	
	for match in matches:
		congress = match.split('/')[1].split('_')[0]
		counter = 0
		f_out = open(match.replace('_raw','_processed'),'w')
		lines = open(match, 'r').readlines()	
		for line in lines:
			if len(line) > 2:
				paren = line.split('(')
				
				f_out.write(paren[0]+'\t' + congress+str(counter)+'\n')
                                f_out.write(paren[0].upper()+'\t' + congress+str(counter)+'\n')
				
				comma = paren[0].split(',')
				comma[1] = comma[1].replace(' Jr','')
				
				f_out.write(comma[1][1:] +comma[0])
				f_out.write('\t' + congress+str(counter))
				f_out.write('\n')
				
				f_out.write(comma[1][1:].upper() +comma[0].upper())
                                f_out.write('\t' + congress+str(counter))
                                f_out.write('\n')
				
				f_out.write(comma[0])
                                f_out.write('\t' + congress+str(counter))
                                f_out.write('\n')
		
				f_out.write(comma[0].upper())
                                f_out.write('\t' + congress+str(counter))
                                f_out.write('\n')

				# if there is a middle name
				if len(comma[1].split(' ')) > 3:
					f_out.write(comma[1].split(' ')[1]+ ' ' + comma[0])
					f_out.write('\t' + congress+str(counter))
                                	f_out.write('\n')

					f_out.write(comma[1].split(' ')[1].upper()+ ' ' + comma[0].upper())
                                        f_out.write('\t' + congress+str(counter))
                                        f_out.write('\n')
			counter += 1
		f_out.close()
if __name__=='__main__':
        process_files()
