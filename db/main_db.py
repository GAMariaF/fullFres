import sys
sys.path.insert(0, '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/backend')
sys.path.insert(0, '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/db')
from vcfutils import parse_thermo_vcf
from vcfutils import filter_nocalls
from vcfutils import explode_format_gt
from vcfutils import explode_info
from vcfutils import explode_func
from vcfutils import get_sample_id
from vcfutils import get_run_id
from dbutils import generate_db
from dbutils import populate_db
from dbutils import populate_vcfdb
from dbutils import count_variant
from dbutils import list_runandsample_variant

vcffile = './Oncomine_Variants_(5.16)_filtered.vcf'

df = parse_thermo_vcf(vcffile)
df = filter_nocalls(df)
df = explode_format_gt(df)
df = explode_info(df)
df = explode_func(df)

#df.to_csv('test.csv')
db = '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/db/variant.db'
run_id = get_run_id(vcffile)
sample_id = get_sample_id(vcffile)
print(run_id, sample_id)
generate_db(db)
populate_vcfdb(db, df, run_id, sample_id)

import pandas as pd
df_interpret = pd.read_excel("Tolkningsskjema.xlsx")

populate_db(db, df_interpret, 'interpret')

# Create view statement for all_data
#CREATE VIEW all_data as select * from vcf inner jo0in interpret on vcf.runid = interpret.runid and vcf.sampleid = interpret.sampleid and vcf.chrom = interpret.chrom and vcf.POS = interpret.POS and vcf.REF = interpret.REF and vcf.ALT = interpret.ALT;

chrom = "chr12"
pos = "25398284"
ref = "C"
alt = "T"
db = 'variant.db'

count_variant(db, chrom, pos, alt, 'vcf')
#yy = count_sample(db, sampleid)

list_runandsample_variant(db, chrom, pos, ref, alt, 'interpret')
