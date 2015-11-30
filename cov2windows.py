import numpy as np
import sys

###############################################################
#Script to find median coverage for each window		      #
#the input file is the output of bedtools coverage with -d    #
#flag							      #
###############################################################
#Args: $1=input bed file $2=output file                       #
###############################################################


medians=open(sys.argv[2], 'w')
#list[0] will store the chromosome, startpos and endpos of the window
#list[1] will be a list of the coverage for each base in the window
list=[[],[]]

with open (sys.argv[1],'r') as frags:
	for line in frags:
		line=line.rstrip()
		line=line.split("\t")

		#check current line matches the window of the current list
		if list[0]!=[line[0],line[1],line[2]]:

			#if not, output the median of all bases in the window
			if len(list[1])>0:
				medians.write("\t".join(list[0])+"\t"+str(np.median(list[1]))+"\n")

			#set the window to the current window and clear list of last window
			list[0]=[line[0],line[1],line[2]]
			list[1]=[]

		#append coverage of current base to list of coverage for current window
		list[1].append(int(line[4]))

	#output median coverage of final window
	medians.write("\t".join(list[0])+"\t"+str(np.median(list[1]))+"\n")

medians.close()


