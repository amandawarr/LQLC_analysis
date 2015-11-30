from __future__ import division
import sys

###############################################################
#Script to calculate % of reads in a window that are abnormal #
#Input file should be output of bedtools coverage for abnormal#
#reads with extra column of bedtools coverage read counts     #
#for all reads						      #
###############################################################
#Args: $1=input bed file $2=output file		              #
###############################################################

#open output file
out=open(sys.argv[2],'w')


with open(sys.argv[1], 'r') as data:
	for line in data:
		line=line.rstrip()
		row=line.split("\t")
		#check read count for abnormal reads is not 0
		if float(row[3])!=0:
			#check read counts for all reads is not lower than read counts of abnormal reads and calculate percentage
			if not float(row[7])>row[3]:
				p=(float(row[3])/float(row[7]))*100
				out.write(line+"\t"+str(p)+"\n")
			else:
				print ("Error: Higher read count in abnormal reads than all reads")
		else:
			out.write(line+"\t0\n")
	
#close out
out.close
