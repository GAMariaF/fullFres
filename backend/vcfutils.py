import pandas as pd
from tkinter.ttk import Separator




vcffile = '../tests/vcfs/test.vcf'


def parse_thermo_vcf(vcf):
    ''' Les inn vcf til pandas dataframe'''
    df = pd.read_csv(vcffile, sep="\t", comment='#', names=["CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT","GT"])
    return df
   
def filter_nocalls(df):
    ''' Fjern varianter som begynner med 0/0 eller ./.'''
    dfOut = df[   (~(df['GT'].str.startswith('./.')))   & (~(df['GT'].str.startswith('0/0')))   ]
    return dfOut

def expand_info_col(df):
    

def expand_GT_col(df):
    pass


df = parse_thermo_vcf(vcffile)
df = filter_nocalls(df)


#    if(match): print(match.group(1))




#result = re.sub(r"(\d.*?)\s(\d.*?)", r"\1 \2", string1)
# Gln61His;Glu62Lys

# vcf_in = pysam.VariantFile(vcffile,'r')

# records = vcf_in.fetch()



# for record in records:
# #    print(record)
#     try:
#         print(record.chrom)
#     except:
#         print("neida")