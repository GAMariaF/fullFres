import pandas as pd
import sqlite3
import sqlalchemy
import datetime
from sqlalchemy import create_engine
from sqlalchemy import text

#sqlite syntax...
def generate_db(db):
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	with engine.connect() as conn:
		result_variantspersample = conn.execute(text("CREATE TABLE IF NOT EXISTS VariantsPerSample ( \
		runid TEXT, \
		sampleid TEXT, \
		CHROM_POS_ALTEND_DATE TEXT, \
		DATE_CHANGED_VARIANT_BROWSER TEXT, \
		Reply, \
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
		changed TEXT, \
		visibility TEXT, \
		PRIMARY KEY (CHROM_POS_ALTEND_DATE, DATE_CHANGED_VARIANT_BROWSER) \
		)"))
	
def populate_thermo_variantdb(db, dfvcf, dfvariant, run_id, sample_id, percent_tumor, sample_diseasetype):
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
					# if in db: use key in Variants table (chrom_pos_ref_alt_date) as key to vcf table
					# do not add variant to table Variants
					# if sample, run and variant already in VariantsPerSample database don't add
					dfvariant_copy = dfvariant_copy.drop(row)
					dfvcf_copy.loc[row,'CHROM_POS_ALTEND_DATE'] = dfdb_variant_latest.CHROM_POS_ALTEND_DATE.iloc[0]
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
		dfSamples = pd.DataFrame({'runid': [run_id], 'sampleid': [sample_id],'Perc_Tumor': [percent_tumor], 'Genelist': [sample_diseasetype]})
		print(run_id,sample_id,percent_tumor,sample_diseasetype)
		# Transfer data to database
		dfvcf_copy.to_sql('VariantsPerSample', engine, if_exists='append', index=False)
		if not dfvariant_copy.empty:
			dfvariant_copy["POS"]=dfvariant_copy["POS"].astype(str)
			dfvariant_copy.to_sql('Variants', engine, if_exists='append', index=False)
		try:			
			dfSamples.to_sql('Samples', engine, if_exists='append', index=False)
		except:
			print('There is an error trying to add '+run_id+','+sample_id+' to table Samples. Is it already in database?')

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
				WHERE Date_Signoff IS NULL;"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_all_samples(db):
	#list all samples
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT s.runid, s.sampleid, \
			s.Date_Signoff, \
			s.Date_Approval \
			FROM Samples s;"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_signoff_samples(db):
	#list all signed off samples ready for approval
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT DISTINCT sampleid, runid, Date_Signoff \
				FROM Samples \
				WHERE Date_Signoff IS NOT NULL \
				AND Date_Approval IS NULL;"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_approved_samples(db):
	#list all approved samples
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT sampleid, runid \
				FROM Samples \
				WHERE Date_Approval IS NOT NULL;"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_all_variants(db):
	#list all variants including frequency
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT COUNT(*) as Frequency\
		, v.gene, v.Type, v.oncomineGeneClass, \
		v.oncomineVariantClass, v.CHROM, v.POS, v.REF, v.ALTEND, \
		group_concat(s.sampleid,', ') VariantsPerSample \
		FROM VariantsPerSample s, Variants v \
		WHERE s.chrom_pos_altend_date = v.chrom_pos_altend_date \
		AND s.chrom_pos_altend_date = v.chrom_pos_altend_date \
		GROUP BY s.chrom_pos_altend_date;"
	with engine.connect() as conn:
		samplelist = pd.read_sql_query(text(stmt), con = conn)
	samplelist_json = samplelist.to_dict('records')
	return samplelist_json

def list_sample_variants(db,sampleid):
	#list all variants for specific sample
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "SELECT VariantsPerSample.sampleid, \
					VariantsPerSample.runid, \
					Variants.gene, Variants.Type, \
					Variants.oncomineGeneClass, \
					Variants.oncomineVariantClass, \
					Variants.CHROM, Variants.POS, Variants.REF, \
					Variants.ALTEND, Classification.class, \
					VariantsPerSample.FILTER \
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

def list_interpretation(db,sampleid):
	#list "tolkningsskjema"
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "select VariantsPerSample.runid, VariantsPerSample.sampleid, Samples.Genelist, \
		Samples.Perc_Tumor, Variants.gene, Variants.transcript, \
		Variants.annotation_variant, VariantsPerSample.FAO || ' / ' || VariantsPerSample.FDP as Reads, \
		VariantsPerSample.Copy_Number, VariantsPerSample.AF, Classification.COSMIC, \
		VariantsPerSample.Reply, VariantsPerSample.User_Classification, VariantsPerSample.Variant_ID, \
		VariantsPerSample.Variant_Name, VariantsPerSample.Key_Variant, VariantsPerSample.Oncomine_Reporter_Evidence, \
		VariantsPerSample.Type, Variants.oncomineGeneClass, Variants.oncomineVariantClass, \
		VariantsPerSample.FILTER, Variants.gene, \
		Variants.chrom || ':' || Variants.pos as Locus, Variants.protein, Variants.ref, \
		Variants.altend, VariantsPerSample.Call, VariantsPerSample.DP, \
		VariantsPerSample.FDP, VariantsPerSample.FAO, \
		Variants.coding, VariantsPerSample.AF, \
		VariantsPerSample.P_Value, VariantsPerSample.Read_Counts_Per_Million, \
		VariantsPerSample.Oncomine_Driver_Gene, VariantsPerSample.Copy_Number, \
		VariantsPerSample.CNV_Confidence, \
		VariantsPerSample.Valid_CNV_Amplicons, Classification.Populasjonsdata, \
		Classification.Funksjonsstudier, Classification.Prediktive_data, \
		Classification.Cancer_hotspots, Classification.Computational_evidens, \
		Classification.Konservering, Classification.ClinVar, VariantsPerSample.CLSF, \
		Classification.class, \
		Classification.Andre_DB, Classification.Comment, \
		Classification.Oncogenicity, Classification.Tier, Classification.Comment \
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
