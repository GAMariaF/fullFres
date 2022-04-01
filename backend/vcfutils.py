import pandas as pd
import re
#from tkinter.ttk import Separator

def parse_thermo_vcf(vcf):
    ''' Les inn vcf til pandas dataframe'''
    df = pd.read_csv(vcffile, sep="\t", comment='#', names=["CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT","GT"])
    return df
   
def filter_nocalls(df):
    ''' Fjern varianter som begynner med 0/0 eller ./.'''
    dfOut = df[   (~(df['GT'].str.startswith('./.')))   & (~(df['GT'].str.startswith('0/0')))   ]
    return dfOut

def explode_format_gt(df):
    ''' Eksploderer GT OG FORMAT-kolonnene til egne kolonner'''
    df.reset_index(inplace=True,drop=True)
    ny = pd.DataFrame(list(dict(zip(a,b)) for a,b in zip(df['FORMAT'].str.split(":"), df['GT'].str.split(":"))))
    dfOut = pd.concat([df, ny], axis=1)
    del dfOut["GT"]
    del dfOut["FORMAT"]
    return dfOut

def replace_semi(inputstring):
    '''  Hvor det finnes semikolon inne i curly braces i INFO-kolonnen gjoeres denne om til underscore - ellers blir det feilmelding'''
    return re.sub(r"{[^{}]+}", lambda x: x.group(0).replace(";", "_"), inputstring)

def explode_info(df):
    ''' Eksploderer INFO-kolonnen til egne kolonner'''
    df.reset_index(inplace=True,drop=True)
    # First maa vi fjerne alle semikolon som er inne i klammer:
    df["INFO"] = df["INFO"].apply(replace_semi)
    # Replace HS MED HS=NA
    df['INFO'] = df['INFO'].str.replace(';HS;',';HS=NA;')
    ny2 = pd.DataFrame([dict(w.split('=', 1) for w in x) for x in df["INFO"].str.split(";")])
    dfOut = pd.concat([df, ny2], axis=1)
    del dfOut["INFO"]
    return dfOut

def get_sample_id():
    pass

def get_run_id():
    pass

''' For aa parse en vcf -> Pandas df gjoer foelgende:  '''

#vcffile = '../tests/vcfs/test.vcf'
# vcffile = '../tests/vcfs/Oncomine_Variants_(5.16)_filtered.vcf'
# df = parse_thermo_vcf(vcffile)
# df = filter_nocalls(df)
# df = explode_format_gt(df)
# df = explode_info(df)

