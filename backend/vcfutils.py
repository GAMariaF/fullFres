import pysam


vcf_in = pysam.VariantFile('../tests/vcfs/test.vcf','r')

records = vcf_in.fetch()
    
for record in records:
    print(record)
    print(record.chrom)