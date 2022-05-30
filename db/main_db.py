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
from vcfutils import get_percent_tumor
from vcfutils import get_sample_diseasetype
from dbutils import generate_db
from dbutils import populate_thermo_variantdb
from dbutils import list_samples
from dbutils import list_signoff_samples
from dbutils import list_approved_samples
from dbutils import list_all_variants
from dbutils import list_sample_variants

vcffile = './tests/vcfs/22skh06417_Oncomine_Extended_516_filtered.vcf'
excelfile = './tests/vcfs/22skh06417_variants.xlsx'
db = '/illumina/analysis/dev/2022/mfahls/fullFres/fullFres/db/variantdb.db'
run_id = get_run_id(vcffile)
sample_id = get_sample_id(vcffile)
percent_tumor = get_percent_tumor(vcffile)
sample_diseasetype = get_sample_diseasetype(vcffile)

# GENERATE DATABASE
generate_db(db)

# TRANSFER VCF TO DATAFRAME
df = parse_thermo_vcf(vcffile,excelfile)
# df = filter_nocalls(df)
df = explode_format_gt(df)
df = explode_info(df)
dfvariant = df[["CHROM","POS","ID","REF","ALTEND","Type","FUNC"]]
dfvariant = explode_func(dfvariant)

# INSERT DATA INTO TABLE SAMPLE, VARIANT AND INTERPRETATION
populate_thermo_variantdb(db, df, dfvariant, \
    run_id, sample_id, percent_tumor, sample_diseasetype)

list_samples(db)
list_signoff_samples(db)
list_approved_samples(db)
list_all_variants(db)
list_sample_variants(db,run_id,sample_id)


# INSERT DATA INTO TABLE INTERPRET
df_interpret = pd.read_excel("Tolkningsskjema.xlsx")
df_interpret = df_interpret.iloc[0:1]
chrom_pos_ref_alt_date = 'chr1225398284CT220504131039'
populate_interpretdb(db, df_interpret, chrom_pos_ref_alt_date)
