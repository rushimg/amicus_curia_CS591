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

def link_emails():
	emails_to_bills = dict()
	with open('bill_parsing_billtype.csv', 'r') as csvfile:
		reader = csv.reader(csvfile) 
		for row in reader:
			bills = set()
			semi =  row[1].split(';')
			for s in semi:
				#if s in emails_to_bills.keys():
				#	print "ERROR"	
				#emails_to_bills[s] = row[0]
				if (s != '') and (len(s.split('=')[0])>1):
					bills.add(s)
			#if len(bills) > 1:
			#	print row[0] 
			emails_to_bills[row[0]] = bills

        gov_track_dict = dict()
	with open(GOVTRACK, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
			#print row[0]
			#print row[2]+'='+row[1]
			gov_track_dict[row[2]+'='+row[1]] = row	
			#print row

	f_out = open('govtrack_add_links_2.csv','w')
	for key in emails_to_bills:
		for elem in emails_to_bills[key]:
			#print elem
			#print key
			
			try:
				f_out.write(key+',')
				row = gov_track_dict[elem] 
				f_out.write(row[0]+'#'+row[2]+'='+row[1])
				f_out.write(','+row[0]+','+row[1]+','+row[2]+','+row[3]+','+row[4]+','+row[5]+','+row[6]+','+row[7]+','+row[8]+','+row[9]+','+row[10]+','+row[11]+','+row[12]) 
				f_out.write('\n')
			except:
				#print elem 
				pass
			#gov_track_dict[elem]
		
	f_out.close()
'''
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
'''
if __name__=='__main__':
        link_emails()
