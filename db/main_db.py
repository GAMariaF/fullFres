import sys
sys.path.insert(0, '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/backend')
sys.path.insert(0, '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/db')
from vcfutils import parse_thermo_vcf
from vcfutils import filter_nocalls
from vcfutils import explode_format_gt
from vcfutils import explode_info
from vcfutils import get_sample_id
from dbutils import populate_db

vcffile = './Oncomine_Variants_(5.16)_filtered.vcf'

df = parse_thermo_vcf(vcffile)
df = filter_nocalls(df)
df = explode_format_gt(df)
df = explode_info(df)

#df.to_csv('test.csv')

sample_id = get_sample_id(vcffile)
print(sample_id)

#populate_db(db, df, run_id, sample_id)