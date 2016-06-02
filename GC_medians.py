from __future__ import division
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
perc_dict={}
#Open bed file with 5 columns (chr, st, end, [readcount|coverage], GC content)
with open(sys.argv[1], 'r') as data:
	for line in data:
		line=line.rstrip()
		line=line.split("\t")
		#For each line add coverage to dict entry for GC content
		if str("%.3f"%float(line[4])) in perc_dict.keys():
			perc_dict[str("%.3f"%float(line[4]))].append(float(line[3]))
		else:
			perc_dict[str("%.3f"%float(line[4]))]=(float(line[3]))			


#For each possible GC percentage, calculate the median and write, if there are no entries write median as 0
for %.3f"%item in [float(j) / 1000 for j in range(0, 1001, 1)]:
	if str(item) in perc_dict.keys():
		out.write(str(item)+ "\t" + str(np.median(perc_dict[str(item)])) + "\n")
	else:
		out.write(str(item)+ "\t0\n")

out.close()
