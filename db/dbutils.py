import xxlimited
import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import update
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
	
def populate_thermo_variantdb(db, dfvcf, dfvariant, \
					run_id, sample_id, percent_tumor, sample_diseasetype):
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
						dfvcf_copy.DATE_CHANGED_VARIANT_BROWSER.loc[row] = \
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
					'Perc_Tumor': [percent_tumor], 'Genelist': [sample_diseasetype]})
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
	return samplelist_json

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

def list_interpretation(db,sampleid):
	#list "tolkningsskjema"
	engine = create_engine("sqlite:///"+db, echo=False, future=True)
	stmt = "select VariantsPerSample.runid, VariantsPerSample.sampleid, Samples.Genelist, \
		Samples.Perc_Tumor, Variants.gene, Variants.exon, Variants.transcript, \
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
								"changed", \
								"visibility"]
	colVariantsPerSample = ["runid", "sampleid", "CHROM_POS_ALTEND_DATE",\
								"DATE_CHANGED_VARIANT_BROWSER","Reply"]
	colSamples = ["runid", "sampleid", \
								"User_Signoff", "Date_Signoff", \
								"User_Approval", "Date_Approval"]
	# Dataframe to table Classification
	dfVarClassification = pd.DataFrame(dfVariant, columns = colClassification)
	dfVarClassification = dfVarClassification.fillna('')
	# Dataframe to table VariantsPerSample
	dfVarVariantsPerSample = pd.DataFrame(dfVariant, columns = colVariantsPerSample)
	dfVarVariantsPerSample = dfVarVariantsPerSample.fillna('')
	# Dataframe to table Samples
	dfVarSamples = pd.DataFrame(dfVariant, columns = colSamples)
	dfVarSamples = dfVarSamples.fillna('')
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
				AND Tier='"+						dfVarClassification['Tier'][0]							+"' \
				AND class='"+						dfVarClassification['class'][0]							+"';"
	with engine.connect() as conn:
		dfInDB = pd.read_sql_query(text(stmt), con=conn)
	if dfInDB.empty:
		# If not in DB set DATE_CHANGED_VARIANT_BROWSER to present date
		print('new classifiction')
		dateChangedVariantBrowser = datetime.datetime.now().strftime("%y%m%d%H%M%S")
		dfVarClassification['DATE_CHANGED_VARIANT_BROWSER'][0] = \
		dateChangedVariantBrowser
		# Since Classification not in table it has to be added
		engine = create_engine("sqlite:///"+db, echo=False, future=True)
		with engine.connect() as conn:
			dfVarClassification.to_sql('Classification', engine, \
				if_exists='append', index=False)
			conn.commit()
	else:
		print('not new in classification')
		# If already in DB chose most recent entry DATE_CHANGED_VARIANT_BROWSER
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
		
def db_to_vcf(db,outvcf='exported.vcf'):
	''' 
	import configparser, sys
	config = configparser.ConfigParser()
	config.read('backend/config.ini')

	sys.path.insert(0, config['Paths']['backend_path'])
	sys.path.insert(0, config['Paths']['db_path'])
	from dbutils import db_to_vcf
	db_to_vcf('/illumina/analysis/dev/2022/fullFres/db/variantdb.db')

	db 		-> the variantDB that is being exported
	outvcf 	-> name of the output vcf
	'''
	vcf_header = '''
	##fileformat=VCFv4.1
	##fileDate=20090805
	##source=myImputationProgramV3.1
	##reference=file:///seq/references/1000GenomesPilot-NCBI36.fasta
	##contig=<ID=20,length=62435964,assembly=B36,md5=f126cdf8a6e0c7f379d618ff66beb2da,species="Homo sapiens",taxonomy=x>
	##phasing=partial
	##INFO=<ID=NS,Number=1,Type=Integer,Description="Number of Samples With Data">
	##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">
	##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
	##INFO=<ID=AA,Number=1,Type=String,Description="Ancestral Allele">
	##INFO=<ID=DB,Number=0,Type=Flag,Description="dbSNP membership, build 129">
	##INFO=<ID=H2,Number=0,Type=Flag,Description="HapMap2 membership">
	##FILTER=<ID=q10,Description="Quality below 10">
	##FILTER=<ID=s50,Description="Less than 50% of samples have data">
	##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
	##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
	##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
	##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
	#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT NA00001 NA00002 NA00003
	'''
	# Write header to file
	
	with open(outvcf, 'w') as f:
		f.write(vcf_header)