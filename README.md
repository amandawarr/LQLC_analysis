Detailed instructions for carrying out analysis described in http://dx.doi.org/10.3389/fgene.2015.00338

This analysis was designed for mapping Illumina reads from the Duroc sow whose DNA was used to construct Sscrofa10.2 to Sscrofa10.2 to find regions that may be low-confidence. If you have used different sequencing methods, parts of this may need to be altered (e.g. if you are using a sequencing method that is not influenced by GC content you may want to skip the GC normalisation).Anywhere in this method where mean and std is used it is necessary to check the distribution of your data, it is extremely likely that a draft genome will have extreme outliers that will inflate these.



Map reads from the individual used to construct the genome to the genome assembly (or repeat the analysis for multiple individuals and accept regions occuring in all individuals as abnormal). We used BWA aln and sampe, bam files should be merged into a single bam file.



Use bedtools makewindows (http://bedtools.readthedocs.org/en/latest/) to create windows covering the genome. We used 1000 base windows (-w 1000) with 200 overlap (-s 800) for the majority of the analysis and 1000 base windows with no overlap for the coverage. The scripts have since been improved and the use of none overlapping windows for coverage is no longer necessary, but faster.

Run bedtools coverage (http://bedtools.readthedocs.org/en/latest/content/tools/coverage.html) on the bam file using the overlapping windows to obtain read counts per window for all reads. Sort the output using: sort -k1,1 -k2,2n in.bed > in.sorted.bed



Use Picard InsertSizeMetrics (https://broadinstitute.github.io/picard/picard-metric-definitions.html) on the bam file to find the mean and std for insert sizes and filter your bam file for insert sizes above or below 2 std from the mean. We used samtools view (http://www.htslib.org/doc/samtools.html) and awk for this and kept high insert sizes and low insert sizes in separate files, the insert sizes are in column 9 of the sam format. Sam files need to be converted back to bam for use with bedtools.

Run bedtools coverage to find the number of reads in each windows that have high or low insert sizes. Sort as before. Use paste to add column 4 (the read counts) from the coverage done previously on all reads to the output files. Use perc.py on these to calculate the percentage of reads in each window with high or low insert sizes, again we kept these separate. You can then find the mean and std of the percentages and accept any windows more than 2 std above the mean for each file as abnormal assuming a normal distribution.




Filter the original bam file to keep properly paired reads using samtools view and the flag -f 0×2 then do as was done for insert sizes. Bedtools coverage, sort, paste raw read counts and perc.py. Again, windows more than 2 std below the mean are abnormal.




For the coverage analysis take the bam file that is filtered for properly paired reads and sort it by name using samtools sort and the -n flag. We also filtered out multimapped reads at this point. Use bedtools bamtobed with the -bedpe flag. Column 1, 2 and 6 of the output file will contain the chromosome, start and end of the whole fragment. These need to be extracted into a bed file (tab delimited, with columns chrom, start, end) When extracting these columns from the file, check that the chromosomes of both ends match (column 1 and column 4) and that neither are set to "." which indicates an unmapped end, disregard any that do not meet these critiria.

We used bedtools genomecov with the -d flag to get per base coverage for the whole genome, however I would now recommend bedtools coverage with the -d flag as it is easier to sort into windows later on. The scripts I have provided for normalisation of GC content assume you have used bedtools coverage and are more efficient than the scripts used previously, though produce the same result. You may use overlapping or non overlapping windows for this.

Use cov2windows.py on the output of bedtools coverage -d. Sort the output as other files were sorted and paste the GC content in as before. Next run GC_medians.py - this will find the median coverage for each possible % of GC. The output of this file can be used to visualise the relationship between GC content and coverage if desired. Use normaliseGC_medians.py with the output of cov2windows.py (with added GC content column) and the output of GC_medians.py. The final column in the output of this file will be the normalised coverage. Find the mean and std of the normalised coverage and check the distribution of the coverage agrees with this as extreme outliers will likely have inflated the mean and std. Find windows above or below 2 std from the mean.




If you find you have a large number of low coverage regions you may want to identify regions enriched for multimappers. This can be done using the same method as identifying regions with improperly paired reads with a bam filtered for only multimappers. The distribution of these is unlikely to be normal, we arbritrarily took any region with >50% multimappers as an explanation for low coverage.




We used samtools to call variants on the bam file as follows:

samtools mpileup -uf ref.fa reads.bam | bcftools view -bvcg - > var.raw.bcf
bcftools view var.raw.bcf | vcfutils.pl varFilter -D100 > var.flt.vcf

We filtered the vcf for homozygous variants and took 100 bases either side of the variant as abnormal. Make sure the ends of these regions aren't below 0 or above the full length of the chromosome!




We then merged the windows as follows using samtools merge:
LQ=High coverage, large insert sizes, small insert sizes, low % properly paired, homozygous variants
LC-Low coverage
LQLC=All of the above

There is expected to be some noise in these data, you may wish to filter these for regions where there are X consecutive windows flagged as abnormal, however we chose to remain strict for the sake of reducing the false-positive rate from variant calling as much as possible.




Bedtools genomecov can be used to find how much of the genome and of each individual chromosome the regions cover. We also used the gEVAL browser to check how BAC ends and fosmids mapped to some of the regions identified. There are a limited number of other species available in this browser, but if you have reads from another method such as BAC ends these can be useful for increasing confidence in the regions the analysis has identified.
