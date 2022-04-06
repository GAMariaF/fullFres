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
#generate_db(db)
populate_db(db, df, run_id, sample_id)

#populate_db(db, df, run_id, sample_id)
