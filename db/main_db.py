import pandas as pd
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
from dbutils import populate_vcfdb
from dbutils import populate_variantdb
from dbutils import populate_interpretdb
from dbutils import count_variant
from dbutils import list_runandsample_variant

vcffile = './Oncomine_Variants_(5.16)_filtered.vcf'
db = '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/db/variantdb.db'
run_id = get_run_id(vcffile)
sample_id = get_sample_id(vcffile)

# GENERATE DATABASE
generate_db(db)

# TRANSFER VCF TO DATAFRAME
df = parse_thermo_vcf(vcffile)
df = filter_nocalls(df)
df = explode_format_gt(df)
df = explode_info(df)

# INSERT DATA INTO TABLE VCF
populate_vcfdb(db, df, run_id, sample_id, 'vcf')

# EXPLODE COLUMN FUNC
dfvariant = df[["CHROM","POS","ID","REF","ALT","CLSF","FUNC"]]
dfvariant = explode_func(dfvariant)

# INSERT DATA INTO TABLE VARIANT
populate_variantdb(db, dfvariant, 'variant')

# INSERT DATA INTO TABLE INTERPRET
df_interpret = pd.read_excel("Tolkningsskjema.xlsx")
populate_interpretdb(db, df_interpret, 'interpret')

chrom = "chr12"
pos = "25398284"
ref = "C"
alt = "T"
db = 'variantdb.db'

count_variant(db, chrom, pos, ref, alt, 'variant')

list_runandsample_variant(db, chrom, pos, ref, alt, 'interpret')
