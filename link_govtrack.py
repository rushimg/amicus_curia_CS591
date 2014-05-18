'''
Grab data from govtrack api by Bill name
sample api call https://www.govtrack.us/api/v2/bill?number=4569&congress=105&format=csv&fields=congress,number,bill_type_label,is_alive,current_status,title_without_number
'''

import sys,os,re
import fnmatch
import csv
import urllib2

BILL_FILE = "bill_parsing_billtype.csv"
GOVTRACK = 'govtrack_additional.csv'

def link_bill_parsing():
        with open(BILL_FILE, 'r') as csvfile:
                reader = csv.reader(csvfile)
                f_out = open('bill_parsing_link.csv','w')
		for row in reader:
			f_out.write(row[0]+',')
                        # get only numerical part of bill name
                        if len(row[1]) > 0:
				congress = row[0].split('_')[0][0:3]
                        	semi =  row[1].split(';')
			
				if len(semi) > 0:
					for bill in semi:
						f_out.write(congress+'#'+bill+';')
                                
			f_out.write('\n')
		f_out.close()
def link_govtrack():
	 with open(GOVTRACK, 'r') as csvfile:
                reader = csv.reader(csvfile)
                f_out = open('govtrack_add_link.csv','w')
                for row in reader:
			print len(row)
                       	#f_out.write(row[0]+',')
                        f_out.write(row[0]+'#'+row[2]+'='+row[1])
			f_out.write(','+row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+','+row[6]+','+row[7]+','+row[8]+','+row[9]+','+row[10]+','+row[11]+','+row[12])
			# get only numerical part of bill name
                        #if len(row[1]) > 0:
                        #        congress = row[0].split('_')[0][0:3]
                        #        semi =  row[1].split(';')

                        #        if len(semi) > 0:
                        #                for bill in semi:
                        #                        f_out.write(congress+'#'+bill+';')

                        f_out.write('\n')
                f_out.close()
if __name__=='__main__':
        link_govtrack()
