# def generate_db(db): 
# creates new database db

# def populate_thermo_variantdb(db, dfvcf, dfvariant, \
#		run_id, sample_id, percent_tumor, sample_diseasetype):
# adds data to database db from dataframes dfvcf, dfvariant

# def list_samples(db):
# list all samples ready for interpretation

# def list_all_samples(db):
# list all samples

# def list_signoff_samples(db):
# list all signed off samples ready for approval

# def list_approved_samples(db):
# list all approved samples

# def list_all_variants(db):
# list all variants including frequency

# def list_interpretation(db,sampleid):
# list "tolkningsskjema"

# def insert_signoffdate(db, user, date, sampleid):
#	When hitting the signoff-button in the browser - set signoff date and signoff user

#def insert_approvedate(db, user, date, sampleid):
#	When hitting the approve-button in the browser - set approved date and approved user

# def insert_variants(db, variant_dict):
# insert variant into database

# def db_to_vcf(db,outvcf='exported.vcf'):
# create vcf from db data to upload to Genexus software

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

#sqlite syntax...
def generate_db(db):
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	with engine.connect() as conn:
		result_variantspersample = conn.execute(text("CREATE TABLE IF NOT EXISTS VariantsPerSample ( \
		runid TEXT, \
		sampleid TEXT, \
		CHROM_POS_ALTEND_DATE TEXT, \
		DATE_CHANGED_VARIANT_BROWSER TEXT, \
		Reply TEXT, \
		User_Classification TEXT, \
		Variant_ID TEXT, \
		Variant_Name TEXT, \
		Key_Variant TEXT, \
		Oncomine_Reporter_Evidence TEXT, \
		Type TEXT, \
		Call TEXT, \
		Call_Details TEXT, \
		Phred_QUAL_Score TEXT, \
		Zygosity TEXT, \
		P_Value TEXT, \
		PPA TEXT, \
		Read_Counts_Per_Million TEXT, \
		Oncomine_Driver_Gene TEXT, \
		Gene_Isoform TEXT, \
		NormalizedReadCount TEXT, \
		Imbalance_Score TEXT, \
		Copy_Number TEXT, \
		P_Value_1 TEXT, \
		CNV_Confidence TEXT, \
		Valid_CNV_Amplicons TEXT, \
		ID TEXT, \
		QUAL TEXT, \
		FILTER TEXT, \
		GT TEXT, \
		GQ TEXT, \
		CN TEXT, \
		READ_COUNT TEXT, \
		GENE_NAME TEXT, \
		EXON_NUM TEXT, \
		RPM TEXT, \
		NORM_COUNT TEXT, \
		NORM_COUNT_TO_HK TEXT, \
		FUSION_DRIVER_GENE TEXT, \
		ANNOTATION TEXT, \
		PASS_REASON TEXT, \
		Non_Targeted TEXT, \
		PRECISE TEXT, \
		END TEXT, \
		NUMTILES TEXT, \
		SD TEXT, \
		CDF_MAPD TEXT, \
		RAW_CN TEXT, \
		REF_CN TEXT, \
		PVAL TEXT, \
		CI TEXT, \
		AF TEXT, \
		AO TEXT, \
		DP TEXT, \
		FAO TEXT, \
		FDP TEXT, \
		FDVR TEXT, \
		FR TEXT, \
		FRO TEXT, \
		FSAF TEXT, \
		FSAR TEXT, \
		FSRF TEXT, \
		FSRR TEXT, \
		FWDB TEXT, \
		FXX TEXT, \
		GCM TEXT, \
		HRUN TEXT, \
		HS_ONLY TEXT, \
		LEN TEXT, \
		MLLD TEXT, \
		OALT TEXT, \
		OID TEXT, \
		OMAPALT TEXT, \
		OPOS TEXT, \
		OREF TEXT, \
		PB TEXT, \
		PBP TEXT, \
		PPD TEXT, \
		QD TEXT, \
		RBI TEXT, \
		REFB TEXT, \
		REVB TEXT, \
		RO TEXT, \
		SAF TEXT, \
		SAR TEXT, \
		SPD TEXT, \
		SRF TEXT, \
		SRR TEXT, \
		SSEN TEXT, \
		SSEP TEXT, \
		SSSB TEXT, \
		STB TEXT, \
		STBP TEXT, \
		VARB TEXT, \
		NID TEXT, \
		MISA TEXT, \
		CLSF TEXT, \
		VCFALT TEXT, \
		VCFPOS TEXT, \
		VCFREF TEXT, \
		HS TEXT, \
		SUBSET TEXT, \
		MISC TEXT, \
		PRIMARY KEY (runid, sampleid, CHROM_POS_ALTEND_DATE) \
        )"))
		result_variants = conn.execute(text("CREATE TABLE IF NOT EXISTS Variants ( \
		CHROM_POS_ALTEND_DATE TEXT, \
		CHROM TEXT, \
		POS TEXT, \
		ID TEXT, \
		REF TEXT, \
		ALTEND TEXT, \
		DATE TEXT, \
		Type TEXT, \
		gene TEXT, \
		exon TEXT, \
		oncomineGeneClass TEXT, \
		oncomineVariantClass TEXT, \
		origPos TEXT, \
		origRef TEXT, \
		normalizedRef TEXT, \
		normalizedPos TEXT, \
		normalizedAlt TEXT, \
		gt TEXT, \
		codon TEXT, \
		coding TEXT, \
		transcript TEXT, \
		annotation_variant TEXT, \
		annotation_variant2 TEXT, \
		function TEXT, \
		protein TEXT, \
		location TEXT, \
		origAlt TEXT, \
		CLNACC1 TEXT, \
		CLNSIG1 TEXT, \
		CLNREVSTAT1 TEXT, \
		CLNID1 TEXT, \
		polyphen TEXT, \
		sift TEXT, \
		grantham TEXT, \
		PRIMARY KEY (CHROM, POS, ALTEND, DATE) \
        )"))
		result_samples = conn.execute(text("CREATE TABLE IF NOT EXISTS Samples ( \
		runid TEXT, \
		sampleid TEXT, \
		Genelist TEXT, \
		Perc_Tumor TEXT, \
		Seq_Date TEXT, \
		Status TEXT, \
		User_Signoff TEXT, \
		Date_Signoff TEXT, \
		User_Approval TEXT, \
		Date_Approval TEXT, \
		PRIMARY KEY (runid, sampleid) \
		)"))
		result_classification = conn.execute(text("CREATE TABLE IF NOT EXISTS Classification ( \
		CHROM_POS_ALTEND_DATE TEXT, \
		DATE_CHANGED_VARIANT_BROWSER TEXT, \
		COSMIC TEXT, \
		Populasjonsdata TEXT, \
		Funksjonsstudier TEXT, \
		Prediktive_data TEXT, \
		Cancer_hotspots TEXT, \
		Computational_evidens TEXT, \
		Konservering TEXT, \
		ClinVar TEXT, \
		Andre_DB TEXT, \
		Comment TEXT, \
		Oncogenicity TEXT, \
		Tier TEXT, \
		class TEXT, \
		evidence_types TEXT, \
		changed TEXT, \
		visibility TEXT, \
		PRIMARY KEY (CHROM_POS_ALTEND_DATE, DATE_CHANGED_VARIANT_BROWSER) \
		)"))
	
def populate_thermo_variantdb(db, dfvcf, dfvariant, \
					run_id, sample_id, percent_tumor, sample_diseasetype, sequencing_date):
	# add variants to table sample and add variants if new to table Variants
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
	dfvcf_copy.insert(3, 'DATE_CHANGED_VARIANT_BROWSER', "" )
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
				dfdb_variant_latest = dfdb_variant[ dfdb_variant.CHROM_POS_ALTEND_DATE == \
					dfdb_variant.CHROM_POS_ALTEND_DATE.max() ]
				cols = dfvariant_copy.columns.tolist()
				cols.remove('DATE')
				cols.remove('CHROM_POS_ALTEND_DATE')
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
					# Find if in Classification table with CHROM_POS_ALTEND_DATE
					# If present get max DATE_CHANGED_VARIANT_BROWSER and set in
					# VariantsPerSample table
					stmtClassification = "select * from Classification \
						where CHROM_POS_ALTEND_DATE = '"\
										+dfdb_variant_latest.CHROM_POS_ALTEND_DATE.iloc[0]+"';"
					dfdbClassification = \
						pd.read_sql_query(text(stmtClassification), con = conn)
					if not dfdbClassification.empty:
						dfvcf_copy.loc[row, 'DATE_CHANGED_VARIANT_BROWSER'] = \
							dfdbClassification.DATE_CHANGED_VARIANT_BROWSER.max()	
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
					'Seq_Date': [sequencing_date]})
		print(run_id,sample_id,percent_tumor,sample_diseasetype,sequencing_date)
		# Transfer data to database
		dfvcf_copy.AF = dfvcf_copy.AF.astype(float)
		dfvcf_copy.AF *= 100
		dfvcf_copy.AF = dfvcf_copy.AF.astype(str)
		dfvcf_copy.to_sql('VariantsPerSample', engine, if_exists='append', index=False)
		if not dfvariant_copy.empty:
			dfvariant_copy["POS"]=dfvariant_copy["POS"].astype(str)
			dfvariant_copy.to_sql('Variants', engine, if_exists='append', index=False)
		try:			
			dfSamples.to_sql('Samples', engine, if_exists='append', index=False)
		except:
			print('There is an error trying to add '+run_id+','+sample_id+' \
				to table Samples. Is it already in database?')

#BRUK kombinasjon chrom,pos,ref,alt og sjekk om denne er med i Variants-tabell 
#	hvis med 
#		sjekk hvis den er lik den som skal legges in
#			hvis lik
#				bruk key (chrom_pos_ref_alt_date) som nokkel i VariantsPerSample-tabell
#			hvis forskjellig
#				lag chrom_pos_ref_alt_date
#				legg inn ny post i Variants-tabell med key (chrom_pos_ref_alt_date)
#				bruk key (chrom_pos_ref_alt_date) som nokkel i VariantsPerSample-tabell

def list_samples(db):
	#list all samples ready for interpretation
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT DISTINCT sampleid, runid \
				FROM Samples \
				WHERE (Date_Signoff IS NULL \
				OR Date_Signoff IS '') \
				AND (Date_Approval IS Null \
				OR Date_Approval is '');"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_all_samples(db):
	#list all samples
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT * FROM Samples s;"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_signoff_samples(db):
	#list all signed off samples ready for approval
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT DISTINCT sampleid, runid, Date_Signoff, User_Signoff \
				FROM Samples \
				WHERE (Date_Signoff IS NOT NULL \
				AND Date_Signoff IS NOT '') \
				AND (Date_Approval IS NULL \
				OR Date_Approval IS '');"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_approved_samples(db):
	#list all approved samples
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT sampleid, runid, Date_Approval \
				FROM Samples \
				WHERE Samples.Date_Approval IS NOT NULL \
				AND Samples.Date_Approval != '';"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_all_variants(db):
	#list all variants including frequency
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT COUNT(*) as Frequency \
		, *,  max(s.DATE_CHANGED_VARIANT_BROWSER),\
		group_concat(s.sampleid,', ') SamplesPerVariant \
		FROM VariantsPerSample s \
		LEFT JOIN Variants v \
		ON s.CHROM_POS_ALTEND_DATE = \
			v.CHROM_POS_ALTEND_DATE \
		LEFT JOIN Classification c \
		ON s.CHROM_POS_ALTEND_DATE = \
			c.CHROM_POS_ALTEND_DATE \
		AND s.DATE_CHANGED_VARIANT_BROWSER = \
			c.DATE_CHANGED_VARIANT_BROWSER \
		GROUP BY s.chrom_pos_altend_date;"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	"""
	To print (some) duplicates to check the data.
	temp = samplelist[['CHROM_POS_ALTEND_DATE', 'DATE_CHANGED_VARIANT_BROWSER)', 'DATE_CHANGED_VARIANT_BROWSER', 'ID', 'Type', ]].reset_index()
	for i in range(temp.shape[0]-100, temp.shape[0]):
		print(i)
		temp2 = temp.loc[i, :]
		temp2.sort_index(inplace=True)
		for c in temp2.items():
			print(c)
		print("----------new var-------------")
		"""
	return samplelist_json

'''
def list_sample_variants(db,sampleid):
	#list all variants for specific sample
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT VariantsPerSample.sampleid, \
					VariantsPerSample.runid, \
					Variants.gene, \
					Variants.exon, Variants.Type, \
					Variants.oncomineGeneClass, \
					Variants.oncomineVariantClass, \
					Variants.CHROM, Variants.POS, Variants.REF, \
					Variants.ALTEND, Classification.class, \
					Classification.evidence_types, \
					VariantsPerSample.FILTER, \
					VariantsPerSample.chrom_pos_altend_date, \
					VariantsPerSample.DATE_CHANGED_VARIANT_BROWSER \
			FROM VariantsPerSample \
			LEFT JOIN Variants \
			ON VariantsPerSample.CHROM_POS_ALTEND_DATE = \
						Variants.CHROM_POS_ALTEND_DATE \
			LEFT JOIN Classification \
			ON VariantsPerSample.chrom_pos_altend_date = \
						Classification.chrom_pos_altend_date \
			AND VariantsPerSample.DATE_CHANGED_VARIANT_BROWSER = \
						Classification.DATE_CHANGED_VARIANT_BROWSER \
			WHERE VariantsPerSample.sampleid='"+sampleid+"';"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json
'''

def list_interpretation(db,sampleid):
	#list "tolkningsskjema"
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "select VariantsPerSample.runid, VariantsPerSample.sampleid, Samples.Genelist, \
		Samples.Perc_Tumor, Samples.Seq_Date, Samples.Status, Variants.gene, Variants.exon, Variants.transcript, \
		Variants.annotation_variant, Variants.annotation_variant2, \
		VariantsPerSample.FAO || ' / ' || VariantsPerSample.FDP as Reads, \
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
	return list_json

def list_search(db, runid: list, sampleid: list, diag: list, variants: list):
	
	engine = create_engine("sqlite:///"+db, echo=False, future=True)

	cond_dict = {"VariantsPerSample.runid": runid, "VariantsPerSample.sampleid": sampleid, "Samples.Genelist": diag, "Variants.annotation_variant": variants}
	conds = ""
	
	for k, v in cond_dict.items():
		if v:
			conds += k + " IN (" + str(v)[1:-1] +") AND " 

	if cond_dict["Samples.Genelist"]:
		add_cond = ("").join([f" AND GenelistsPerVariant LIKE '%{gl}%'" for gl in cond_dict["Samples.Genelist"]])
	else:
		add_cond = ""
	stmt = f"""
	SELECT v.Type, v.CHROM, v.POS, v.REF, v.ALTEND, v.gene, v.oncomineGeneClass, v.oncomineVariantClass, v.annotation_variant, 

	group_concat(vs.sampleid,', ') SamplesPerVariant,
	group_concat(s.Genelist, ', ') GenelistsPerVariant,

	COUNT(DISTINCT s.Genelist) as FreqGenLis, 
	COUNT(s.sampleid) as FreqSamples,

	group_concat(v.CHROM_POS_ALTEND_DATE,', ') CPADListPerVariant

	FROM Variants v
	LEFT JOIN VariantsPerSample vs
	ON v.CHROM_POS_ALTEND_DATE = 
		vs.CHROM_POS_ALTEND_DATE 
	LEFT JOIN Samples s 
	ON vs.sampleid =  
		s.sampleid 
 
	WHERE v.annotation_variant in 
		(SELECT Variants.annotation_variant
		FROM Variants
		LEFT JOIN VariantsPerSample
		ON Variants.CHROM_POS_ALTEND_DATE = 
			VariantsPerSample.CHROM_POS_ALTEND_DATE
		LEFT JOIN Samples
		ON VariantsPerSample.sampleid = 
			Samples.sampleid 
		WHERE {conds[:-4]} 
		) 

	GROUP BY v.CHROM, v.POS, v.annotation_variant 
	HAVING FreqGenLis >= {len(diag)}{add_cond}
	ORDER BY FreqGenLis DESC;"""
	print(stmt)
	with engine.connect() as conn:
		interpretationlist = pd.read_sql_query(text(stmt), con = conn)
	list_json = interpretationlist.to_dict('records')
	return list_json

def insert_signoffdate(db, user, date, sampleid):
	'''
	When hitting the signoff-button in the browser - set signoff date and signoff user
	'''
	
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	print(sampleid)
	stmt = "UPDATE Samples set User_Signoff = '"+user+"' ,Date_Signoff = '"+date+"' WHERE sampleid = '"+sampleid+"';"
	with engine.connect() as conn:
		result = conn.execute(text(stmt))
		conn.commit()

def insert_approvedate(db, user, date, sampleid):
	''' 
	When hitting the approve-button in the browser - set approved date and approved user
	'''
	print("running approve-date")
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "UPDATE Samples set User_Approval = '"+user+"', Date_Approval = '"+date+"' WHERE sampleid = '"+sampleid+"';"
	with engine.connect() as conn:
		result = conn.execute(text(stmt))
		conn.commit()

def insert_variants(db, variant_dict):
	# update DATE_CHANGED_VARIANT_BROWSER !!!
    # Check if classification has a copy in database 
    # if true: pick that DATE_CHANGED_VARIANT_BROWSER and
    # set it into Classification and VariantsPerSample
    # if false: set new DATE_CHANGED_VARIANT_BROWSER and
    # set it into Classification and VariantsPerSample
	dfVariant = pd.DataFrame(variant_dict,index=[0])
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
	stmt = "select * from Classification \
				where CHROM_POS_ALTEND_DATE = '"+	dfVarClassification['CHROM_POS_ALTEND_DATE'][0]			+"' \
				AND COSMIC='"+          			dfVarClassification['COSMIC'][0]						+"' \
				AND Populasjonsdata='"+ 			dfVarClassification['Populasjonsdata'][0]				+"' \
				AND Funksjonsstudier='"+			dfVarClassification['Funksjonsstudier'][0]				+"' \
				AND Prediktive_data='"+ 			dfVarClassification['Prediktive_data'][0]				+"' \
				AND Cancer_hotspots='"+ 			dfVarClassification['Cancer_hotspots'][0]				+"' \
				AND Computational_evidens='"+		dfVarClassification['Computational_evidens'][0]			+"' \
				AND Konservering='"+				dfVarClassification['Konservering'][0]					+"' \
				AND ClinVar='"+						dfVarClassification['ClinVar'][0]						+"' \
				AND Andre_DB='"+					dfVarClassification['Andre_DB'][0]						+"' \
				AND Comment='"+						dfVarClassification['Comment'][0]						+"' \
				AND Oncogenicity='"+				dfVarClassification['Oncogenicity'][0]					+"' \
				AND evidence_types='"+				dfVarClassification['evidence_types'][0]				+"' \
				AND Tier='"+						dfVarClassification['Tier'][0]							+"' \
				AND class='"+						dfVarClassification['class'][0]							+"';"
	with engine.connect() as conn:
		dfInDB = pd.read_sql_query(text(stmt), con=conn)
	if dfInDB.empty:
		# If not in DB set DATE_CHANGED_VARIANT_BROWSER to present date
		print('new classifiction')
		dateChangedVariantBrowser = datetime.datetime.now().strftime("%y%m%d%H%M%S")
		dfVarClassification.loc[0, 'DATE_CHANGED_VARIANT_BROWSER'] = \
		dateChangedVariantBrowser
		# Since Classification not in table it has to be added
		engine = create_engine("sqlite:///"+db, echo=False, future=True)
		with engine.connect() as conn:
			dfVarClassification.to_sql('Classification', engine, \
				if_exists='append', index=False)
			conn.commit()
	else:
		print('not new in classification')
		# If already in DB choose most recent entry DATE_CHANGED_VARIANT_BROWSER
		dateChangedVariantBrowser = \
			dfInDB['DATE_CHANGED_VARIANT_BROWSER'].astype(float).max().astype(int).astype(str)	
	print(dateChangedVariantBrowser)
	# Update table VariantsPerSample with DATE_CHANGED_VARIANT_BROWSER
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	with engine.connect() as conn:
		stmtVPS = "UPDATE VariantsPerSample set \
					DATE_CHANGED_VARIANT_BROWSER = \
						'"+dateChangedVariantBrowser+"',\
					Reply = \
						'"+dfVarVariantsPerSample['Reply'][0]+"'\
				WHERE \
					runid = \
						'"+dfVarVariantsPerSample.runid[0]+"'\
					AND sampleid = \
						'"+dfVarVariantsPerSample.sampleid[0]+"'\
					AND CHROM_POS_ALTEND_DATE = \
						'"+dfVarVariantsPerSample.CHROM_POS_ALTEND_DATE[0]+"';"
		result = conn.execute(text(stmtVPS))
		conn.commit()
	# Update table Samples with data for User and Date (Sign_off)
	# and User and Date (Approval)
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
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

def db_to_vcf(db,outvcf='exported.vcf'):
	''' 
	
	'''
	print("test")
	writer = csv.writer(open(outvcf,'w'), delimiter="\t", quoting=csv.QUOTE_NONE, quotechar="", escapechar=' ')
	vcf_header = ['##fileformat=VCFv4.1',
		'##fileDate=20170821',
		'##source=CentoMD',
		'##reference=GRChr37',
		'##INFO=<ID=IHSAMPLES,Number=1,Type=String,Description="Sample names from inhouse db that contains this variant and het state in parentheses">',
		'##INFO=<ID=IHHET,Number=1,Type=String,Description="Number of inhouse hets for this variant">',
		'##INFO=<ID=IHHOM,Number=1,Type=String,Description="Number of inhouse homozygotes for this variant">'
		]
	lasthead = ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO']
		# Write header to file
	for i in vcf_header:
		writer.writerow([i])
	writer.writerow(lasthead)

	# Hente data fra DB: (spørring)

	''' 
	SELECT CHROM,POS,REF,ALTEND,group_concat(VPS.User_Classification, '|') AS User_Classification, group_concat(VPS.sampleid, '|') AS sampleid FROM Variants AS V
	LEFT JOIN VariantsPerSample AS VPS ON V.CHROM_POS_ALTEND_DATE = VPS.CHROM_POS_ALTEND_DATE
	GROUP BY V.CHROM_POS_ALTEND_DATE
	
	'''
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	with engine.connect() as conn:
		vcf_data = conn.execute(text("SELECT CHROM,POS,REF,ALTEND,group_concat(VPS.User_Classification, '|') AS User_Classification, group_concat(VPS.sampleid, '|') AS sampleid, VPS.ID AS ID, VPS.QUAL AS QUAL FROM Variants AS V LEFT JOIN VariantsPerSample AS VPS ON V.CHROM_POS_ALTEND_DATE = VPS.CHROM_POS_ALTEND_DATE GROUP BY V.CHROM_POS_ALTEND_DATE")).fetchall()
		
	df_vcf_data = pd.DataFrame(vcf_data)
	
	df_vcf_data[['REF', 'ALTEND']] = df_vcf_data[['REF','ALTEND']].fillna(value=".")
	df_vcf_data[['QUAL']] = df_vcf_data[['QUAL']].fillna(value=".")
	# Fjerne Chr
	df_vcf_data.CHROM = df_vcf_data.CHROM.str.replace('chr','')
	# Slå sammen User_classification og sampleid tin INFO-format
	df_vcf_data["INFO"] = "SAMPLEID="+df_vcf_data.sampleid
	# Fjern de som ikke har verdi i CHR
	df_vcf_data = df_vcf_data[df_vcf_data["CHROM"] != ""]
	# Legg til classification kun hvis den er tilstede
	df_vcf_data.loc[~df_vcf_data['User_Classification'].isnull(), 'INFO'] = df_vcf_data.INFO + ";USR_CLASSIFICATION=" + df_vcf_data.User_Classification
	# ADD filter
	df_vcf_data[['FILTER']] = "."
	
	df_vcf_data[['CHROM','POS','REF','ALTEND','QUAL','FILTER','INFO']].to_csv('exported.vcf', sep="\t", header=False, index=False, mode='a',quoting=csv.QUOTE_NONE, quotechar="", escapechar=' ')










def statistics(db):
	'''
	input: database
	outputs a json with different statistics from the database
	
	
	'''
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = ""
	with engine.connect() as conn:
		# Number of runs
		n_runs = conn.execute(text("SELECT COUNT(DISTINCT(runid)) \
			FROM Samples")).fetchone()[0]

		# Number of users
		n_users = conn.execute(text("SELECT COUNT(DISTINCT(User_Signoff)) \
			FROM Samples")).fetchone()[0]

		# Number of samples
		n_samples = conn.execute(text("SELECT COUNT(DISTINCT(sampleid)) \
			FROM Samples")).fetchone()[0]
	
		# Number of variants
		n_variants = conn.execute(text("SELECT COUNT(*) \
			FROM (SELECT DISTINCT chrom, pos, altend from Variants)")).fetchone()[0]

		# Number of samples waiting for interpretation
		n_samples_waiting = conn.execute(text("SELECT COUNT(*) FROM(SELECT DISTINCT sampleid, runid \
												FROM Samples \
												WHERE (Date_Signoff IS NULL \
												OR Date_Signoff IS '') \
												AND (Date_Approval IS Null \
												OR Date_Approval is ''))")).fetchone()[0]

		# Number of samples waiting for control
		n_samples_signedoff = conn.execute(text("SELECT COUNT(*) FROM(SELECT DISTINCT \
													sampleid, runid, Date_Signoff \
													FROM Samples \
													WHERE (Date_Signoff IS NOT NULL \
													AND Date_Signoff IS NOT '') \
													AND (Date_Approval IS NULL \
													OR Date_Approval IS ''))")).fetchone()[0]

		# Number of samples per genelist
		n_samples_genelist = conn.execute(text("SELECT Genelist, COUNT(*) as Freq \
													FROM Samples GROUP BY Genelist")).fetchall()
		n_samples_genepd = pd.DataFrame(n_samples_genelist)
		n_samples_genedict = n_samples_genepd.to_dict('list')

		# Number of variants per genelist
		n_variants_genelist = conn.execute(text("SELECT Genelist,COUNT(*) AS Freq FROM ( \
													SELECT DISTINCT chrom, pos, altend, Genelist FROM Samples s \
													LEFT JOIN VariantsPerSample vps \
													ON s.runid = vps.runid \
													AND s.sampleid = vps.sampleid \
													LEFT JOIN Variants v \
													ON vps.CHROM_POS_ALTEND_DATE = \
														v.CHROM_POS_ALTEND_DATE) \
													GROUP BY Genelist")).fetchall()
		n_variants_genepd = pd.DataFrame(n_variants_genelist)
		n_variants_genedict = n_variants_genepd.to_dict('list')

#### query to get no of variants grouped by class, Genelist
		## class 1
		n_variants_class1list = conn.execute(text("SELECT class, Genelist, COUNT(*) AS Freq \
										FROM ( \
										SELECT DISTINCT chrom, pos, altend, \
										Genelist, class FROM Samples s \
										LEFT JOIN VariantsPerSample vps \
										ON s.runid = vps.runid \
										AND s.sampleid = vps.sampleid \
										LEFT JOIN Variants v \
										ON vps.CHROM_POS_ALTEND_DATE = \
											v.CHROM_POS_ALTEND_DATE \
										LEFT JOIN Classification c \
										ON vps.CHROM_POS_ALTEND_DATE = \
											c.CHROM_POS_ALTEND_DATE \
										AND vps.DATE_CHANGED_VARIANT_BROWSER = \
											c.DATE_CHANGED_VARIANT_BROWSER \
										WHERE c.class='1 - Benign') \
										GROUP BY Genelist")).fetchall()
		n_variants_class1pd = pd.DataFrame(n_variants_class1list)
		n_variants_class1 = n_variants_class1pd.to_dict('list')

#### query to get no of variants grouped by class, Genelist
		## class 2
		n_variants_class2list = conn.execute(text("SELECT class, Genelist, COUNT(*) AS Freq \
										FROM ( \
										SELECT DISTINCT chrom, pos, altend, \
										Genelist, class FROM Samples s \
										LEFT JOIN VariantsPerSample vps \
										ON s.runid = vps.runid \
										AND s.sampleid = vps.sampleid \
										LEFT JOIN Variants v \
										ON vps.CHROM_POS_ALTEND_DATE = \
											v.CHROM_POS_ALTEND_DATE \
										LEFT JOIN Classification c \
										ON vps.CHROM_POS_ALTEND_DATE = \
											c.CHROM_POS_ALTEND_DATE \
										AND vps.DATE_CHANGED_VARIANT_BROWSER = \
											c.DATE_CHANGED_VARIANT_BROWSER \
										WHERE c.class='2 - Likely Benign') \
										GROUP BY Genelist")).fetchall()
		n_variants_class2pd = pd.DataFrame(n_variants_class2list)
		n_variants_class2 = n_variants_class2pd.to_dict('list')

#### query to get no of variants grouped by class, Genelist
		## class 3
		n_variants_class3list = conn.execute(text("SELECT class, Genelist, COUNT(*) AS Freq \
										FROM ( \
										SELECT DISTINCT chrom, pos, altend, \
										Genelist, class FROM Samples s \
										LEFT JOIN VariantsPerSample vps \
										ON s.runid = vps.runid \
										AND s.sampleid = vps.sampleid \
										LEFT JOIN Variants v \
										ON vps.CHROM_POS_ALTEND_DATE = \
											v.CHROM_POS_ALTEND_DATE \
										LEFT JOIN Classification c \
										ON vps.CHROM_POS_ALTEND_DATE = \
											c.CHROM_POS_ALTEND_DATE \
										AND vps.DATE_CHANGED_VARIANT_BROWSER = \
											c.DATE_CHANGED_VARIANT_BROWSER \
										WHERE c.class='3 - VUS') \
										GROUP BY Genelist")).fetchall()
		n_variants_class3pd = pd.DataFrame(n_variants_class3list)
		n_variants_class3 = n_variants_class3pd.to_dict('list')

#### query to get no of variants grouped by class, Genelist
		## class 4
		n_variants_class4list = conn.execute(text("SELECT class, Genelist, COUNT(*) AS Freq \
										FROM ( \
										SELECT DISTINCT chrom, pos, altend, \
										Genelist, class FROM Samples s \
										LEFT JOIN VariantsPerSample vps \
										ON s.runid = vps.runid \
										AND s.sampleid = vps.sampleid \
										LEFT JOIN Variants v \
										ON vps.CHROM_POS_ALTEND_DATE = \
											v.CHROM_POS_ALTEND_DATE \
										LEFT JOIN Classification c \
										ON vps.CHROM_POS_ALTEND_DATE = \
											c.CHROM_POS_ALTEND_DATE \
										AND vps.DATE_CHANGED_VARIANT_BROWSER = \
											c.DATE_CHANGED_VARIANT_BROWSER \
										WHERE c.class='4 - Likely Oncogenic') \
										GROUP BY Genelist")).fetchall()
		n_variants_class4pd = pd.DataFrame(n_variants_class4list)
		n_variants_class4 = n_variants_class4pd.to_dict('list')

#### query to get no of variants grouped by class, Genelist
		## class 5
		n_variants_class5list = conn.execute(text("SELECT class, Genelist, COUNT(*) AS Freq \
										FROM ( \
										SELECT DISTINCT chrom, pos, altend, \
										Genelist, class FROM Samples s \
										LEFT JOIN VariantsPerSample vps \
										ON s.runid = vps.runid \
										AND s.sampleid = vps.sampleid \
										LEFT JOIN Variants v \
										ON vps.CHROM_POS_ALTEND_DATE = \
											v.CHROM_POS_ALTEND_DATE \
										LEFT JOIN Classification c \
										ON vps.CHROM_POS_ALTEND_DATE = \
											c.CHROM_POS_ALTEND_DATE \
										AND vps.DATE_CHANGED_VARIANT_BROWSER = \
											c.DATE_CHANGED_VARIANT_BROWSER \
										WHERE c.class='5 - Oncogenic') \
										GROUP BY Genelist")).fetchall()
		n_variants_class5pd = pd.DataFrame(n_variants_class5list)
		n_variants_class5 = n_variants_class5pd.to_dict('list')

		# Number of users
		n_users = conn.execute(text("SELECT COUNT(DISTINCT(User_Signoff)) \
			FROM Samples")).fetchone()[0]

		n_users_samples = conn.execute(text("SELECT User_Signoff, COUNT(*) AS Freq \
												FROM Samples \
												GROUP BY User_Signoff")).fetchall()
		n_users_samplespd = pd.DataFrame(n_users_samples)
		n_users_samplesdict = n_users_samplespd.to_dict('list')

	results = {"runs": n_runs, "samples": n_samples, "variants": n_variants, \
				"samples_waiting": n_samples_waiting, \
				"samples_signedoff": n_samples_signedoff, \
				"samples_genelist": n_samples_genedict, \
				"variants_genelist": n_variants_genedict, \
				"users": n_users, \
				"users_samples": n_users_samplesdict, \
				"variants_class1": n_variants_class1,
				"variants_class2": n_variants_class2,
				"variants_class3": n_variants_class3,
				"variants_class4": n_variants_class4,
				"variants_class5": n_variants_class5 }
	return results

def data_report(db):
	#list variant data for report
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "select VariantsPerSample.runid, \
		VariantsPerSample.sampleid, Samples.Genelist, \
		Samples.Perc_Tumor, Samples.Seq_Date, Samples.Status, Variants.gene, Variants.exon,\
		Variants.annotation_variant, \
		Samples.Date_Approval, \
		VariantsPerSample.FAO || ' / ' || VariantsPerSample.FDP as Reads, \
		VariantsPerSample.Copy_Number, VariantsPerSample.AF, \
		VariantsPerSample.DP, \
		VariantsPerSample.CNV_Confidence, \
		VariantsPerSample.Valid_CNV_Amplicons, \
		VariantsPerSample.chrom_pos_altend_date, \
		VariantsPerSample.DATE_CHANGED_VARIANT_BROWSER \
			from VariantsPerSample \
			left join Variants \
			on VariantsPerSample.chrom_pos_altend_date = \
							Variants.chrom_pos_altend_date \
			LEFT JOIN Samples \
			on VariantsPerSample.runid = Samples.runid \
			and VariantsPerSample.sampleid = Samples.sampleid \
			WHERE Samples.Date_Approval IS NOT NULL \
			AND Samples.Date_Approval != '' \
			AND VariantsPerSample.Reply='Yes';"
	with engine.connect() as conn:
		interpretationlist = pd.read_sql_query(text(stmt), con = conn)
	list_json = interpretationlist.to_dict('records')
	return list_json
