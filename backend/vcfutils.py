import pandas as pd
import numpy as np
import re
import json
#from tkinter.ttk import Separator

class CustomFileError(Exception):
    """Raised when some thing went wrong with the input files."""
    def __init__(self, message="Something went wrong with the files."):
        self.message = message
        super().__init__(self.message)

def parse_thermo_vcf(vcf,excel):
    ''' Les inn vcf og excel, slå de sammen til en pandas dataframe'''
    df_vcf = pd.read_csv(vcf, sep="\t", comment='#', names=["CHROM","POS","ID","REF","ALT","QUAL","FILTER","INFO","FORMAT","GT"])
    df_excel = pd.read_excel(excel)
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    # With fusion 
    df_excel_w = df_excel.loc[df_excel['Type'] == 'Fusion']
    if not df_excel_w.empty:
        #df_excel_w.loc[:,'ID'] = df_excel_w.loc[:,'Variant ID'] + "_1"
        df_excel_w = df_excel_w.assign(ID = df_excel_w.loc[:,'Variant ID'] + "_1")
        df1 = pd.merge(df_excel_w,df_vcf,on='ID',how='left')
        df1.loc[:,'ID']=df1.loc[:,'Variant ID']
    # With RNAExonVariant
    df_excel_wRNA = df_excel.loc[df_excel['Type'] == 'RNAExonVariant']
    if not df_excel_wRNA.empty:
        df_excel_wRNA = df_excel_wRNA.assign(ID = df_excel_wRNA.loc[:,'Variant ID'] + "_1")
        df3 = pd.merge(df_excel_wRNA,df_vcf,on='ID',how='left')
        df3.loc[:,'ID']=df3.loc[:,'Variant ID']
        
    # Without fusion and without RNAExonVariant
    df_excel_wo = df_excel.loc[df_excel['Type'] != 'Fusion']
    df_excel_wo = df_excel_wo.loc[df_excel_wo['Type'] != 'RNAExonVariant']
    if not df_excel_wo.empty:
        df_excel_wo = df_excel_wo.reset_index(drop='True')
        df_vcf["Locus_vcf"] = df_vcf.CHROM.astype(str)+":" \
                    +df_vcf.POS.astype(str)
        #df_vcf.Locus = df_vcf.Locus.astype(str)
        #df_excel_wo.Locus.astype(str)
        df2 = pd.merge(df_excel_wo,df_vcf,\
                    left_on=['Locus','Variant ID'],right_on=['Locus_vcf','ID'],how='left')
        df2 = df2.drop(columns=['Locus_vcf'])

    df = pd.concat([df1,df2,df3])
    df = df.reset_index(drop='True')
    df = df.rename(columns={'ALT':'ALTEND'})
    # Removing columns TYPE and SVTYPE (already specifiec in column Type)
    df = df.drop(columns=['TYPE','SVTYPE', 'Gene', 'Locus', \
                        'AA Change', 'Ref','Alt','Raw Read Depth', \
                        'Effective Read Depth', 'Alt Allele Read Counts',\
                        'Allele Ratio', 'Nuc Change', 'Allele Frequency', \
                        'Allele Frequency (%)', 'Filtered Read Coverage', \
                        'Allele read Count', 'NOCALL_REASON'], errors='ignore')
    return df
   
def filter_nocalls(df):
    ''' Fjern varianter som begynner med 0/0 eller ./.'''
    dfOut = df[   (~(df['GT'].str.startswith('./.')))   & (~(df['GT'].str.startswith('0/0')))   ]
    return dfOut

def explode_format_gt(df):
    ''' 
    
    Eksploderer GT OG FORMAT-kolonnene til egne kolonner
    #1: Følgende kolonner finnes to steder, så de fjernes fra format: AF,AO,DP,FAO,FDP,FRO,FSAF,FSAR,FSRF,FSRR,RO,SAF,SAR,SRF,SRR
    
    '''
    df.reset_index(inplace=True,drop=True)
    df.rename(columns = {'GT':'GTFORMAT'}, inplace = True)
    
    ny = pd.DataFrame(list(dict(zip(a,b)) for a,b in zip(df['FORMAT'].str.split(":"), df['GTFORMAT'].str.split(":"))))
    for i in ["AF","AO","DP","FAO","FDP","FRO","FSAF","FSAR","FSRF","FSRR","RO","SAF","SAR","SRF","SRR"]: #1
        try:
            ny = ny.drop(i, axis=1)
        except:
            pass
    dfOut = pd.concat([df, ny], axis=1)
    del dfOut["GTFORMAT"]
    del dfOut["FORMAT"]
    
    return dfOut

def replace_semi(inputstring):
    '''  Hvor det finnes semikolon inne i curly braces i INFO-kolonnen gjoeres denne om til underscore - ellers blir det feilmelding'''
    return re.sub(r"{[^{}]+}", lambda x: x.group(0).replace(";", "_"), inputstring)

def fix_info(input_string):
    '''Catches any other cases of missing info'''
    info = input_string.split('=', 1)
    if len(info) == 1:
        return info + ['NA']
    else:
        return info

def explode_info(df):
    ''' Eksploderer INFO-kolonnen til egne kolonner'''
    df.reset_index(inplace=True,drop=True)
    # First maa vi fjerne alle semikolon som er inne i klammer:
    df["INFO"] = df["INFO"].apply(replace_semi)
    # Replace HS MED HS=NA
    # ok???? ';HS;',';HS=NA;' --> 'HS;','HS=NA;' /mfahls
    df['INFO'] = df['INFO'].str.replace('HS;','HS=NA;')
    df['INFO'] = df['INFO'].str.replace('Non-Targeted;','Non-Targeted=1;')
    ny2 = pd.DataFrame([dict(fix_info(w) for w in x) for x in df["INFO"].str.split(";")])
    dfOut = pd.concat([df, ny2], axis=1)
    del dfOut["INFO"]

    if 'END' in dfOut.columns:
            dfOut['ALTEND'] = dfOut['ALTEND'].replace('<CNV>',np.nan)
            temp1 = dfOut.ALTEND
            temp2 = dfOut.END

            dfOut.ALTEND = temp1.combine_first(temp2)
    dfOut = dfOut.drop(columns=['NOCALL_REASON'], errors='ignore')
    return dfOut

def explode_func(df):
    ''' Eksploderer FUNC-kolonnen til egne kolonner 
        Hvis flere transcripter/gener per variant blir disse numerert'''
    row_count = len(df.index)
    dfOut = pd.DataFrame()
    for row in range(row_count):
        dftemp2 = pd.DataFrame()
        if not pd.isnull(df.FUNC[row]):
            temp0 = eval(df.FUNC[row])
            lentemp0 = len(temp0)
            if lentemp0>1:
                dftemp1 = pd.DataFrame(temp0)
                dftemp1['annotation_variant'] = ''
                # Add '(1)', '(2)' etc to different transcripts/genes of same variant
                for i in range(lentemp0):
                    try:
                        dftemp1['annotation_variant'].iloc[i] = \
                            str(dftemp1['transcript'].iloc[i]) + ':' + \
                            str(dftemp1['coding'].iloc[i]) + ' ' + \
                            str(dftemp1['protein'].iloc[i][:2]) + '(' + \
                            str(dftemp1['protein'].iloc[i][2:]) + ')'
                    except:
                        pass
                    dftemp1.iloc[i] = dftemp1.iloc[i].add("("+str(i+1)+")")
                dftemp1 = dftemp1.fillna("")
                for column in dftemp1:
                    for rowtemp1 in range(1,lentemp0):
                        dftemp1[column].iloc[0] += " " +dftemp1[column].iloc[rowtemp1]
                dftemp2 = pd.DataFrame(dftemp1.iloc[[0]])
                dftemp2.rename(index={0:row},inplace=True)
            else:
                dftemp2 = pd.DataFrame(temp0)
                dftemp2['annotation_variant'] = ''
                try:
                    dftemp2['annotation_variant'].iloc[0] = \
                        str(dftemp2['transcript'].iloc[0]) + ':' + \
                        str(dftemp2['coding'].iloc[0]) + ' ' + \
                        str(dftemp2['protein'].iloc[0][:2]) + '(' + \
                        str(dftemp2['protein'].iloc[0][2:]) + ')'
                except:
                    pass
                dftemp2.rename(index={0:row},inplace=True)
                dftemp2 = dftemp2.fillna("")
        dfrow = df.iloc[[row]]
        dfOutrow = pd.concat([dfrow,dftemp2], axis = 1)
        dfOut = pd.concat([dfOut,dfOutrow])
    del dfOut["FUNC"]
    dfOut = dfOut.fillna("")
    return dfOut       

def get_sample_id(vcf):
    sample_list=[re.findall(r'IonReporterAnalysisName=.+_Lib',line) 
            for line in open(vcf)]
    sample_string=[string for string in sample_list if len(string) > 0][0][0]
    sample_string=sample_string[24:-4]
    return sample_string
#IonReporterAnalysisName=22SKH02673_LibPrep87

def get_run_id(vcf):
    run_list=[re.findall(r'GNXS-0\d{3}-\d{1,}-GX_\d{4}.*_\d{2}/Auto',line) 
            for line in open(vcf)]
    run_string=[string for string in run_list if len(string) > 0][0][0]
    # A bit weird maybe, but 'GX' has been hardcoded in above anyway.
    run_string='GX' + run_string[:-8].split('GX')[1]
    print(run_string)
    return run_string
#GNXS-0297-18-GX_0016_22/Auto

def get_percent_tumor(vcf):
    sample_list=[re.findall(r'##manually_input_percent_tumor_cellularity=\d{2}',line) 
            for line in open(vcf)]
    sample_string=[string for string in sample_list if len(string) > 0][0][0]
    sample_string=sample_string[-2:]
    return sample_string
# ##manually_input_percent_tumor_cellularity=85

def get_sample_diseasetype(vcf):
    sample_list=[re.findall(r'##sampleDiseaseType=.*',line) 
            for line in open(vcf)]
    sample_string=[string for string in sample_list if len(string) > 0][0][0]
    sample_string=sample_string[20:]
    return sample_string
# ##sampleDiseaseType=Prostate Cancer

def get_sequencing_date(vcf):
    sample_list=[re.findall(r'##fileDate=.*',line) 
            for line in open(vcf)]
    sample_string=[string for string in sample_list if len(string) > 0][0][0]
    sample_string=sample_string[11:]
    return sample_string
# ##sampleDiseaseType=Prostate Cancer

''' For aa parse en vcf -> Pandas df gjoer foelgende:  '''

# vcffile = '../tests/vcfs/test.vcf'
# vcffile = '../tests/vcfs/Oncomine_Variants_(5.16)_filtered.vcf'
#vcffile = '../db/Oncomine_LibPrep88_ff8081817e2f1544017f7c2a5b340019.vcf'

#df = parse_thermo_vcf(vcffile)
#df = filter_nocalls(df)
#df = explode_format_gt(df)
#df = explode_info(df)
#df = explode_func(df)
