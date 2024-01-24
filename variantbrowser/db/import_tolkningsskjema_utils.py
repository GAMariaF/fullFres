##########################################################################################
##
### IMPORTANT!!
### Only working for import from Tolkningsskjema!!
##
##########################################################################################
import pandas as pd
from sqlalchemy import create_engine
import configparser
import xxlimited
import sqlite3
import sqlalchemy
from sqlalchemy import update
import datetime
from sqlalchemy import text
import csv
import os

def populate_thermo_variantdb(db, dfvcf, dfvariant, \
					run_id, sample_id, percent_tumor, sample_diseasetype, \
					sequencing_date, status):
	# add variants to table sample and add variants if new to table Variants
	print('populate_thermodb')
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	if dfvcf.empty:
		print("Missing data to import to tables Variants, VariantsPerSample and Samples")
		return
	dfvcf_copy = dfvcf.copy(deep=True)
	dfvariant_copy = dfvariant.copy(deep=True)
	# add chrom_pos_altend_date column
	dfvcf_copy.insert(0, 'runid', run_id, True)
	dfvcf_copy.insert(1, 'sampleid', sample_id, True)
	dfvcf_copy.insert(2, 'CHROM_POS_ALTEND_DATE', "" )
	#dfvcf_copy.insert(3, 'DATE_CHANGED_VARIANT_BROWSER', "" )
	dfvariant_copy.insert( 0, 'CHROM_POS_ALTEND_DATE', "" )
	# add date column
	date=datetime.datetime.now().strftime("%y%m%d%H%M%S")
	dfvariant_copy.insert(6, 'DATE', date)
	dfvariant_copy["POS"]=dfvariant_copy["POS"].astype(str)
	dfvariant_copy.CHROM_POS_ALTEND_DATE = \
		dfvariant_copy[["CHROM", "POS", "ALTEND", "DATE"]] \
			.agg("".join, axis=1)
	# Connecting to sqlite database
	with engine.connect() as conn:
		#BRUK kombinasjon chrom,pos,alt (/end for CNV) og sjekk om denne er med i Variants-tabell 
		for row in range(len(dfvcf_copy)):
			stmt = "select * from Variants \
				where CHROM = '"+dfvariant_copy.CHROM[row]+"' \
					AND POS = '"+dfvariant_copy.POS[row]+"' \
					AND ALTEND = '"+dfvariant_copy.ALTEND[row]+"';"
			dfdb_variant = pd.read_sql_query(text(stmt), con = conn)
			#hvis med: sjekk hvis den er lik den som skal legges in
			if not dfdb_variant.empty:
				print(dfdb_variant)
				dfdb_variant_latest = dfdb_variant[ dfdb_variant.CHROM_POS_ALTEND_DATE == \
					dfdb_variant.CHROM_POS_ALTEND_DATE.max() ]
				cols = dfvariant_copy.columns.tolist()
				cols.remove('DATE')
				cols.remove('CHROM_POS_ALTEND_DATE')
				cols.remove('DATE_CHANGED_VARIANT_BROWSER')
				dfvariant_copy = dfvariant_copy.astype(str)
				dfdb_variant_latest = dfdb_variant_latest.astype(str)
				# check if variant in database except key chrom_pos_altend_date
				variantindb = dfdb_variant_latest.reset_index(drop=True)[cols].equals( \
					dfvariant_copy.loc[[row]].reset_index(drop=True)[cols])
				if variantindb:
					# if in db: use key in Variants table
					# (chrom_pos_ref_alt_date) as key to 
					# variantspersample (dfvcf_copy) table
					# do not add variant to table Variants
					dfvariant_copy = dfvariant_copy.drop(row)
					dfvcf_copy.loc[row,'CHROM_POS_ALTEND_DATE'] = dfdb_variant_latest.CHROM_POS_ALTEND_DATE.iloc[0]
					# # Find if in Classification table with CHROM_POS_ALTEND_DATE
					# # If present get max DATE_CHANGED_VARIANT_BROWSER and set in
					# # VariantsPerSample table
					# stmtClassification = "select * from Classification \
					# 	where CHROM_POS_ALTEND_DATE = '"\
					# 					+dfdb_variant_latest.CHROM_POS_ALTEND_DATE.iloc[0]+"';"
					# dfdbClassification = \
					# 	pd.read_sql_query(text(stmtClassification), con = conn)
					# if not dfdbClassification.empty:
					# 	dfvcf_copy.loc[row, 'DATE_CHANGED_VARIANT_BROWSER'] = \
					# 		dfdbClassification.DATE_CHANGED_VARIANT_BROWSER.max()	
					# if sample, run and variant already in VariantsPerSample database don't add
					stmtvcf = "select * from VariantsPerSample \
						where runid = '"+dfvcf_copy.runid.loc[row]+"' \
							AND sampleid = '"+dfvcf_copy.sampleid.loc[row]+"' \
							AND CHROM_POS_ALTEND_DATE = '"+dfvcf_copy.CHROM_POS_ALTEND_DATE.loc[row]+"';"
					dfdb_vcf = pd.read_sql_query(text(stmtvcf), con = conn)
					if not dfdb_vcf.empty:
						print(dfvcf_copy.runid.loc[row], \
							dfvcf_copy.sampleid.loc[row], \
								dfvcf_copy.CHROM_POS_ALTEND_DATE.loc[row], " is already in database")
						dfvcf_copy = dfvcf_copy.drop(row)
				else:
					# if FUNC not in db, i.e existing variant but with new FUNC
					dfvcf_copy.loc[row,'CHROM_POS_ALTEND_DATE'] = dfvariant_copy.CHROM_POS_ALTEND_DATE.loc[row]
			else:
				# if variant not previously in database, add new variant
				dfvcf_copy.loc[row,'CHROM_POS_ALTEND_DATE'] = dfvariant_copy.CHROM_POS_ALTEND_DATE.loc[row]
		dfvcf_copy = dfvcf_copy.drop(columns=['CHROM','POS', \
						'REF', 'ALTEND', 'FUNC', 'TYPE','SVTYPE', \
						'Oncomine Gene Class','Oncomine Variant Class'], \
						errors='ignore')
		dfvcf_copy = dfvcf_copy.rename(columns={ \
				'User Classification': 'User_Classification', \
				'Variant ID': 'Variant_ID', \
				'Variant Name': 'Variant_Name', \
				'Key Variant': 'Key_Variant', \
				'Oncomine Reporter Evidence': 'Oncomine_Reporter_Evidence', \
				'Call Details': 'Call_Details', \
				'Phred QUAL Score': 'Phred_QUAL_Score', \
				'P-Value': 'P_Value', \
				'P-Value.1': 'P_Value_1', \
				'Read Counts Per Million': 'Read_Counts_Per_Million', \
				'Oncomine Driver Gene': 'Oncomine_Driver_Gene', \
				'Gene Isoform': 'Gene_Isoform', \
				'Imbalance Score': 'Imbalance_Score', \
				'Copy Number': 'Copy_Number', \
				'CNV Confidence': 'CNV_Confidence', \
				'Valid CNV Amplicons': 'Valid_CNV_Amplicons', \
				'Non-Targeted': 'Non_Targeted' \
				})
		# Data to table Samples
		dfSamples = pd.DataFrame({'runid': [run_id], 'sampleid': [sample_id],\
					'Perc_Tumor': [percent_tumor], 'Genelist': [sample_diseasetype],\
					'Seq_Date': [sequencing_date], 'Status': [status]})
		print(run_id,sample_id,percent_tumor,sample_diseasetype,sequencing_date, status)
		# Transfer data to database
		##dfvcf_copy.AF = dfvcf_copy.AF.astype(float)
		##dfvcf_copy.AF *= 100
		##dfvcf_copy.AF = dfvcf_copy.AF.astype(str)
		dfvcf_copy.to_sql('VariantsPerSample', engine, if_exists='append', index=False)
		if not dfvariant_copy.empty:
			dfvariant_copy = dfvariant_copy.drop(columns=['DATE_CHANGED_VARIANT_BROWSER'])
			dfvariant_copy["POS"]=dfvariant_copy["POS"].astype(str)
			dfvariant_copy.to_sql('Variants', engine, if_exists='append', index=False)
		try:
			dfSamples.to_sql('Samples', engine, if_exists='append', index=False)
		except:
			print('There is an error trying to add '+run_id+','+sample_id+' \
				to table Samples. Is it already in database?')
			return dfvcf_copy.CHROM_POS_ALTEND_DATE.loc[row]
	return dfvcf_copy.CHROM_POS_ALTEND_DATE.loc[row]


def insert_variants(db, dfVariant):
	# update DATE_CHANGED_VARIANT_BROWSER !!!
	# Check if classification has a copy in database 
	# if true: pick that DATE_CHANGED_VARIANT_BROWSER and
	# set it into Classification and VariantsPerSample
	# if false: set new DATE_CHANGED_VARIANT_BROWSER and
	# set it into Classification and VariantsPerSample
	colClassification = ["CHROM_POS_ALTEND_DATE",\
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
	colVariantsPerSample = ["runid", "sampleid", "CHROM_POS_ALTEND_DATE",\
								"DATE_CHANGED_VARIANT_BROWSER","Reply"]
	colSamples = ["runid", "sampleid", \
								"User_Signoff", "Date_Signoff", \
								"User_Approval", "Date_Approval"]
	colVariants = ["CHROM_POS_ALTEND_DATE", "CHROM", "POS", "ALTEND", "DATE", "annotation_variant2"]
	# Dataframe to table Classification
	dfVarClassification = pd.DataFrame(dfVariant, columns = colClassification)
	dfVarClassification = dfVarClassification.fillna('')
	# Dataframe to table VariantsPerSample
	dfVarVariantsPerSample = pd.DataFrame(dfVariant, columns = colVariantsPerSample)
	dfVarVariantsPerSample = dfVarVariantsPerSample.fillna('')
	# Dataframe to table Samples
	dfVarSamples = pd.DataFrame(dfVariant, columns = colSamples)
	dfVarSamples = dfVarSamples.fillna('')
	# Dataframe to table Variants
	dfVariants = pd.DataFrame(dfVariant, columns = colVariants)
	dfVariants = dfVariants.fillna('')
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	# stmt = "select * from Classification \
	# 			where CHROM_POS_ALTEND_DATE = '"+	dfVarClassification['CHROM_POS_ALTEND_DATE'][0]			+"' \
	# 			AND COSMIC='"+						dfVarClassification['COSMIC'][0]						+"' \
	# 			AND Populasjonsdata='"+				dfVarClassification['Populasjonsdata'][0]				+"' \
	# 			AND Funksjonsstudier='"+			dfVarClassification['Funksjonsstudier'][0]				+"' \
	# 			AND Prediktive_data='"+				dfVarClassification['Prediktive_data'][0]				+"' \
	# 			AND Cancer_hotspots='"+			dfVarClassification['Cancer_hotspots'][0]				+"' \
	# 			AND Computational_evidens='"+		dfVarClassification['Computational_evidens'][0]			+"' \
	# 			AND Konservering='"+				dfVarClassification['Konservering'][0]					+"' \
	# 			AND ClinVar='"+						dfVarClassification['ClinVar'][0]						+"' \
	# 			AND Andre_DB='"+					dfVarClassification['Andre_DB'][0]						+"' \
	# 			AND Comment='"+						dfVarClassification['Comment'][0]						+"' \
	# 			AND Oncogenicity='"+				dfVarClassification['Oncogenicity'][0]					+"' \
	# 			AND evidence_types='"+				dfVarClassification['evidence_types'][0]				+"' \
	# 			AND Tier='"+						dfVarClassification['Tier'][0]							+"' \
	# 			AND class='"+						dfVarClassification['class'][0]							+"';"
	# with engine.connect() as conn:
	# 	dfInDB = pd.read_sql_query(text(stmt), con=conn)
	# if dfInDB.empty:
		# If not in DB set DATE_CHANGED_VARIANT_BROWSER to present date
	print('new classifiction')
		# dateChangedVariantBrowser = datetime.datetime.now().strftime("%y%m%d%H%M%S")
		# dfVarClassification.loc[0, 'DATE_CHANGED_VARIANT_BROWSER'] = \
		#dateChangedVariantBrowser
		# Since Classification not in table it has to be added
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	with engine.connect() as conn:
		dfVarClassification.to_sql('Classification', engine, \
			if_exists='append', index=False)
		conn.commit()
	# else:
	# 	print('not new in classification')
	# 	# If already in DB choose most recent entry DATE_CHANGED_VARIANT_BROWSER
	# 	dateChangedVariantBrowser = \
	# 		dfInDB['DATE_CHANGED_VARIANT_BROWSER'].astype(float).max().astype(int).astype(str)	
	#print(dateChangedVariantBrowser)
	# Update table VariantsPerSample with DATE_CHANGED_VARIANT_BROWSER
	# engine = create_engine("sqlite:///"+db, echo=False, future=True)
	# with engine.connect() as conn:
	# 	stmtVPS = "UPDATE VariantsPerSample set \
	# 				DATE_CHANGED_VARIANT_BROWSER = \
	# 					'"+dateChangedVariantBrowser+"',\
	# 				Reply = \
	# 					'"+dfVarVariantsPerSample['Reply'][0]+"'\
	# 			WHERE \
	# 				runid = \
	# 					'"+dfVarVariantsPerSample.runid[0]+"'\
	# 				AND sampleid = \
	# 					'"+dfVarVariantsPerSample.sampleid[0]+"'\
	# 				AND CHROM_POS_ALTEND_DATE = \
	# 					'"+dfVarVariantsPerSample.CHROM_POS_ALTEND_DATE[0]+"';"
	# 	result = conn.execute(text(stmtVPS))
	# 	conn.commit()
	# Update table Samples with data for User and Date (Sign_off)
	# and User and Date (Approval)
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	print(dfVarSamples)
	with engine.connect() as conn:
		stmtS = "UPDATE Samples set \
					User_Signoff = \
						'"+dfVarSamples.User_Signoff[0]+"',\
					Date_Signoff = \
						'"+dfVarSamples.Date_Signoff[0]+"',\
					User_Approval = \
						'"+dfVarSamples.User_Approval[0]+"',\
					Date_Approval = \
						'"+dfVarSamples.Date_Approval[0]+"'\
				WHERE \
					runid = \
						'"+dfVarSamples.runid[0]+"'\
					AND sampleid = \
						'"+dfVarSamples.sampleid[0]+"';"
		result = conn.execute(text(stmtS))
		conn.commit()
	# Update table Variants with annotation_variant2
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	with engine.connect() as conn:
		stmtV = "UPDATE Variants set \
					annotation_variant2 = \
						'"+dfVariants.annotation_variant2[0]+"'\
				WHERE \
					CHROM = \
						'"+dfVariants.CHROM[0]+"'\
					POS = \
						'"+dfVariants.POS[0]+"'\
					ALTEND = \
						'"+dfVariants.ALTEND[0]+"'\
					DATE = \
						'"+dfVariants.DATE[0]+"';"
		result = conn.execute(text(stmtS))
		conn.commit()
