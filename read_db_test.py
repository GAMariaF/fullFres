import xxlimited
import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import update
import datetime
from sqlalchemy import create_engine
from sqlalchemy import text
import csv
import os
import configparser
import sys

config = configparser.ConfigParser()
config.read('backend/config.ini')

sys.path.insert(0, config['Paths']['backend_path'])
sys.path.insert(0, config['Paths']['db_path'])

db_path = config['Paths']['db_full_path']

def list_approved_samples(db, sampleid):

    
	#list "tolkningsskjema"
    engine = create_engine("sqlite:///"+db, echo=False, future=True)
    stmt = "select VariantsPerSample.runid, VariantsPerSample.sampleid, Samples.Genelist, \
		Samples.Perc_Tumor, Samples.Seq_date, Variants.gene, Variants.exon, Variants.transcript, \
		Variants.annotation_variant, VariantsPerSample.FAO || ' / ' || VariantsPerSample.FDP as Reads, \
		VariantsPerSample.Copy_Number, round(VariantsPerSample.AF,1) as AF, Classification.COSMIC, \
		VariantsPerSample.Reply, VariantsPerSample.User_Classification, VariantsPerSample.Variant_ID, \
		VariantsPerSample.Variant_Name, VariantsPerSample.Key_Variant, \
		VariantsPerSample.Oncomine_Reporter_Evidence, \
		VariantsPerSample.Type, Variants.oncomineGeneClass, Variants.oncomineVariantClass, \
		VariantsPerSample.FILTER, \
		Variants.chrom || ':' || Variants.pos as Locus, Variants.protein, Variants.ref, \
		Variants.altend, VariantsPerSample.Call, VariantsPerSample.DP, \
		VariantsPerSample.FDP, VariantsPerSample.FAO, \
		Variants.coding, \
		VariantsPerSample.P_Value, VariantsPerSample.Read_Counts_Per_Million, \
		VariantsPerSample.Oncomine_Driver_Gene, \
		VariantsPerSample.CNV_Confidence, \
		VariantsPerSample.Valid_CNV_Amplicons, Classification.Populasjonsdata, \
		Classification.Funksjonsstudier, Classification.Prediktive_data, \
		Classification.Cancer_hotspots, Classification.Computational_evidens, \
		Classification.Konservering, Classification.ClinVar, VariantsPerSample.CLSF, \
		Classification.class, \
		Classification.evidence_types, \
		Classification.Andre_DB, Classification.Oncogenicity, \
		Classification.Tier, Classification.Comment, \
		VariantsPerSample.chrom_pos_altend_date, \
		VariantsPerSample.DATE_CHANGED_VARIANT_BROWSER, \
		Classification.changed, \
		Classification.visibility \
			from VariantsPerSample \
			left join Variants \
			on VariantsPerSample.chrom_pos_altend_date = Variants.chrom_pos_altend_date \
			left join Classification \
			on VariantsPerSample.chrom_pos_altend_date = Classification.chrom_pos_altend_date \
			AND VariantsPerSample.DATE_CHANGED_VARIANT_BROWSER = \
											Classification.DATE_CHANGED_VARIANT_BROWSER \
			LEFT JOIN Samples \
			on VariantsPerSample.runid = Samples.runid \
			and VariantsPerSample.sampleid = Samples.sampleid \
			WHERE VariantsPerSample.sampleid='"+sampleid+"';"
    with engine.connect() as conn:
        interpretationlist = pd.read_sql_query(text(stmt), con = conn)
    list_json = interpretationlist.to_dict('records')
    for item in list_json:
        #print(item)
        print("----------------NEW VAR-----------------------")
        for k, v in item.items():
            print(str(k)+": "+str(v))
            

if __name__ == '__main__':
    list_approved_samples(db_path, '22SHK10172')
