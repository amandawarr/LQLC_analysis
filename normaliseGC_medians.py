from __future__ import division
import numpy as np
import sys
###############################################################
#Script to adjust window [readcount||coverage] by GC content  #
###############################################################
#Args: $1=input bed file $2=output file from GC_medians.py    # 
#$3=output file 				              #
###############################################################

out=open(sys.argv[3],'w')


#Calculate the overall median [readcount||coverage] for whole genome.
cov=[]
with open(sys.argv[1], 'r')  as coverage:
	for line in coverage:
		line=line.rstrip()
		line=line.split("\t")
		cov.append(float(line[3]))
median=np.median(cov)
cov=None

#if window GC content matches GC content from sys.argv[2], divide whole genome
#median by median for GC content and multiply by original median [readcount||coverage] for window

#Make a library of medians for each possible GC content
GC_conts={}
with open(sys.argv[2], 'r') as GC:
	for line in GC:
		line=line.rstrip()
		line=line.split("\t")
		line[0]="%.3f"%float(line[0])
		GC_conts[line[0]]=line[1]

#Normalise coverage
with open(sys.argv[1], 'r') as coverage:
	for line in coverage:
		line=line.rstrip()
		row=line.split("\t") 
		if "%.3f"%float(row[4]) in GC_conts.keys():
			#check that [readcount|coverage] is not 0
			if float(row[3])!=0:				
				m=(float(median)/(float(GC_conts["%.3f"%float(row[4])])))*float(row[3])	
				out.write(line + "\t"+  str(m)+"\n")
			#if it is 0, then median is 0		
			else:
				out.write(line + "\t0\n")
		#if the window's GC % does not match any values in output from 
		#GC_medians, print error message.
		else:
			print("A window had a GC content that did not appear in "+ sys.argv[2])

#Final column of output will be normalised coverage
out.close()
