# read excel-file to dataframe
# send dataframe to four different
# tables in database.
import pandas as pd
from sqlalchemy import create_engine
import configparser
from dbutils import generate_db
import xxlimited
import sqlite3
import sqlalchemy
from sqlalchemy import update
import datetime
from sqlalchemy import text
import csv
import os
import time
from dbutils import populate_thermo_variantdb
from import_tolkningsskjema_utils import populate_thermo_variantdb
from import_tolkningsskjema_utils import insert_variants

#config = configparser.ConfigParser()
#config.read('backend/config.ini')
#db = config['Paths']['db_full_path']

db = '/illumina/analysis/dev/2023/mfahls/test2.db'

# Generate empty database
generate_db(db)

# Read data Tolkningskjema
excel = '/illumina/analysis/dev/2023/mfahls/Tolkningsskjema_161222.xlsx'
dfTolkning = pd.read_excel(excel, header = 0)
dfTolkning = dfTolkning.assign(Date_Signoff=dfTolkning['Date_Signoff'].astype(str))
dfTolkning = dfTolkning.assign(Date_Approval=dfTolkning['Date_Approval'].astype(str))
dfTolkning = dfTolkning.assign(POS=dfTolkning['POS'].astype(str))
dfTolkning = dfTolkning.assign(Oncogenicity=dfTolkning['Oncogenicity'].astype(str))
dfTolkning = dfTolkning.assign(Konservering=dfTolkning['Konservering'].astype(str))
dfTolkning = dfTolkning.assign(DATE_CHANGED_VARIANT_BROWSER=dfTolkning['DATE_CHANGED_VARIANT_BROWSER'].astype(str))
dfTolkning.Perc_Tumor *= 100
sampleList = dfTolkning.sampleid.drop_duplicates().reset_index(drop=True)

for sample_id in sampleList:
    print(sample_id)
    dfTolkningSample = dfTolkning.loc[dfTolkning['sampleid']==sample_id].reset_index(drop=True)
    run_id = dfTolkningSample.loc[0]['runid']
    percent_tumor = dfTolkningSample.loc[0]['Perc_Tumor']
    sample_diseasetype = dfTolkningSample.loc[0]['Genelist']
    sequencing_date = dfTolkningSample.loc[0]['Seq_date']
    status = dfTolkningSample.loc[0]['Status']
    columnListdf = ['Reply','DATE_CHANGED_VARIANT_BROWSER','User_Classification', 'Variant_ID', 'Variant_Name', 'Key_Variant',\
        'Oncomine_Reporter_Evidence', 'Type', \
        'Call', 'Oncomine_Driver_Gene', 'Copy_Number',\
         'P_Value', 'CNV_Confidence', 'Valid_CNV_Amplicons', 'Read_Counts_Per_Million',\
        'ID', 'CHROM', 'POS', 'REF', 'ALTEND', 'QUAL', 'FILTER', 'GT', 'GQ',\
        'CN', 'SVTYPE', 'READ_COUNT', 'GENE_NAME', 'EXON_NUM', 'RPM',\
        'NORM_COUNT', 'NORM_COUNT_TO_HK', 'FUSION_DRIVER_GENE', 'NOCALL_REASON',\
        'FUNC', 'AF', 'AO', 'DP', 'FAO', 'FDP', 'FDVR', 'FR', 'FRO', 'FSAF',\
        'FSAR', 'FSRF', 'FSRR', 'FWDB', 'FXX', 'GCM', 'HRUN', 'HS_ONLY', 'LEN',\
        'MLLD', 'OALT', 'OID', 'OMAPALT', 'OPOS', 'OREF', 'PB', 'PBP', 'PPD',\
        'QD', 'RBI', 'REFB', 'REVB', 'RO', 'SAF', 'SAR', 'SPD', 'SRF', 'SRR',\
        'SSEN', 'SSEP', 'SSSB', 'STB', 'STBP', 'TYPE', 'VARB', 'NID', 'VCFALT',\
        'VCFPOS', 'VCFREF', 'HS', 'PRECISE', 'END', 'NUMTILES', 'SD',\
        'CDF_MAPD', 'RAW_CN', 'REF_CN', 'PVAL', 'CI']
    columnListdfvariant = ['DATE_CHANGED_VARIANT_BROWSER','CHROM', 'POS', 'ID', 'REF', 'ALTEND', 'Type', 'gene', 'exon',\
        'oncomineGeneClass', 'oncomineVariantClass',\
        'annotation_variant', 'origPos', 'origRef', 'normalizedRef',\
        'normalizedPos', 'normalizedAlt', 'gt', 'coding', 'transcript',\
        'function', 'protein', 'location', 'origAlt', 'CLNACC1', 'CLNSIG1',\
        'CLNREVSTAT1', 'CLNID1', 'codon', 'polyphen', 'sift', 'grantham',\
        'annotation_variant2']  
    df = dfTolkningSample.loc[:,dfTolkningSample.columns.isin(columnListdf)]
    dfvariant = dfTolkningSample.loc[:,dfTolkningSample.columns.isin(columnListdfvariant)]
    dfvariant = dfvariant.assign(annotation_variant2 = dfvariant['annotation_variant'])
    time.sleep(1) # wait for one second to give unique time keys
    for ind in df.index:
        print(ind)
        df_ind = pd.DataFrame(df.loc[ind]).transpose().reset_index(drop=True)
        dfvariant_ind = pd.DataFrame(dfvariant.loc[ind]).transpose().reset_index(drop=True)
        dfTolkningSample_ind = pd.DataFrame(dfTolkningSample.loc[ind]).transpose().reset_index(drop=True)
        # INSERT DATA INTO TABLE SAMPLE, VARIANT AND INTERPRETATION
        chromPosAltEndDate = populate_thermo_variantdb(db, df_ind, dfvariant_ind, \
                                run_id, sample_id, percent_tumor, sample_diseasetype, \
                                sequencing_date, status)
        dfTolkningSample_ind['CHROM_POS_ALTEND_DATE'] = chromPosAltEndDate
        print('hepp',chromPosAltEndDate)
        insert_variants(db, dfTolkningSample_ind)

"""
colSamples              = ["runid", "sampleid", \
                                "Genelist", "Perc_Tumor", \
                                "Seq_Date", \
								"User_Signoff", "Date_Signoff", \
								"User_Approval", "Date_Approval"]
colVariantsPerSample    = ["runid", "sampleid", "CHROM_POS_ALTEND_DATE",\
								"DATE_CHANGED_VARIANT_BROWSER","Reply", \
                                "User_Classification","Variant_ID","Variant_Name", \
                                "Key_Variant","Oncomine_Reporter_Evidence","Type", \
                                "Call", "P_Value", "DP", "FDP", "FAO", \
                                "Copy_Number", "CNV_Confidence", \
                                "Valid_CNV_Amplicons","AF", \
                                "Read_Counts_Per_Million", "Oncomine_Driver_Gene"
                                ]
colClassification       = ["CHROM_POS_ALTEND_DATE",\
								"DATE_CHANGED_VARIANT_BROWSER", \
								"COSMIC", \
								"Populasjonsdata", \
								"Funksjonsstudier", \
								"Prediktive_data", \
								"Cancer_hotspots", \
								"Computational_evidens", \
								"Konservering", \
								"ClinVar", \
								"Andre_DB", \
								"Comment", \
								"Oncogenicity", \
								"Tier", \
								"class", \
                                "evidence_types", \
								"changed", \
								"visibility"]
colVariants             = [ "CHROM_POS_ALTEND_DATE", \
                                "CHROM", \
                                "POS", \
                                "ID", \
                                "REF", \
                                "ALTEND", \
                                "DATE", \
                                "Type", \
                                "gene", \
                                "exon", \
                                "oncomineGeneClass", \
                                "oncomineVariantClass", \
                                "origPos", \
                                "origRef", \
                                "normalizedRef", \
                                "normalizedPos", \
                                "normalizedAlt", \
                                "gt", \
                                "codon", \
                                "coding", \
                                "transcript", \
                                "annotation_variant", \
                                "function", \
                                "protein", \
                                "location", \
                                "origAlt", \
                                "CLNACC1", \
                                "CLNSIG1", \
                                "CLNREVSTAT1", \
                                "CLNID1", \
                                "polyphen", \
                                "sift", \
                                "grantham" ]

dfSamples           = pd.DataFrame(dfTolkning, columns = colSamples)
dfVariantsPerSample = pd.DataFrame(dfTolkning, columns = colVariantsPerSample)
dfClassification    = pd.DataFrame(dfTolkning, columns = colClassification)
dfVariants          = pd.DataFrame(dfTolkning, columns = colVariants)

dfSamples           = dfSamples.drop_duplicates()
dfVariantsPerSample = dfVariantsPerSample.drop_duplicates()
dfClassification    = dfClassification.drop_duplicates()
dfVariants          = dfVariants.drop_duplicates()

engine = create_engine("sqlite:///"+db, echo=False, future=True)
dfSamples.to_sql('Samples', engine, if_exists='append', index=False)
dfVariantsPerSample.to_sql('VariantsPerSample', engine, if_exists='append', index=False)
dfClassification.to_sql('Classification', engine, if_exists='append', index=False)
dfVariants.to_sql('Variants', engine, if_exists='append', index=False)

"""