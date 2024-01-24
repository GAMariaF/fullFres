import pandas as pd
import sys
import configparser
config = configparser.ConfigParser()
config.read('backend/config.ini')
sys.path.insert(0, config['Paths']['backend_path'])
sys.path.insert(0, config['Paths']['db_path'])
from vcfutils import parse_thermo_vcf
from vcfutils import explode_format_gt
from vcfutils import explode_info
from vcfutils import explode_func
from vcfutils import get_sample_id
from vcfutils import get_run_id
from vcfutils import get_percent_tumor
from vcfutils import get_sample_diseasetype
from vcfutils import get_sequencing_date
from dbutils import generate_db
from dbutils import populate_thermo_variantdb
from dbutils import list_samples
from dbutils import list_all_samples
from dbutils import list_signoff_samples
from dbutils import list_approved_samples
from dbutils import list_all_variants
#from dbutils import list_sample_variants
from dbutils import list_interpretation

vcffile     = config['Testfiles']['vcffile']      # './tests/vcfs/22shk04823_Oncomine_Extended_516_filtered.vcf'
excelfile   = config['Testfiles']['excelfile']  # './tests/vcfs/22shk04823_variants.xlsx'
db          = config['Paths']['db_full_path']
run_id = get_run_id(vcffile)
sample_id = get_sample_id(vcffile)
percent_tumor = get_percent_tumor(vcffile)
sample_diseasetype = get_sample_diseasetype(vcffile)
sequencing_date = get_sequencing_date(vcffile)

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
list_all_samples(db)
list_signoff_samples(db)
list_approved_samples(db)
list_all_variants(db)
#list_sample_variants(db,sample_id)
list_interpretation(db,sample_id)
