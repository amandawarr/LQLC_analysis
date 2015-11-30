import numpy as np
import sys
#################################################################################
#Script to find median [readcount||coverage] of windows for each possible GC %	#
#Input file should be output from cov2windows.py with a column added for GC	#
#content which can be obtained using column 5 of the output from bedtools nuc	#
#################################################################################
#Args: $1=Input bed file $2=Output file       				        #
#################################################################################

out=open(sys.argv[2],'w')

#loop through values 0-1, to 3dp
for f in [float(j) / 1000 for j in range(0, 1001, 1)]:
			
#For each possible % GC content (f) find matching values in column 5 
#for matching values, append the read count||depth from column 4 to r

	r=[]
	#Open bed file with 5 columns (chr, st, end, [readcount|coverage], GC content)
	with open(sys.argv[1], 'r') as data:
		for line in data:
			line=line.rstrip()
			line=line.split("\t")
	
			if "%.3f"%float(line[4])=="%.3f"%float(f):
				r.append(float(line[3]))			
	#If there are values in the array, calculate the median and write, else write median as 0
	if len(r)!=0:
		out.write(str(f)+ "\t" + str(np.median(r)) + "\n")
	else:
		out.write(str(f)+ "\t0\n")

out.close()
