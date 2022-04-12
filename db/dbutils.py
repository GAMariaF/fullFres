import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

#sqlite syntax...
def generate_db(db):
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		result_vcf = conn.execute(text("CREATE TABLE IF NOT EXISTS vcf ( \
		runid TEXT, \
		sampleid TEXT, \
		chrom_pos_ref_alt TEXT, \
		ID TEXT, \
		QUAL TEXT, \
		FILTER TEXT, \
		GQ INTEGER, \
		AF FLOAT, \
		AO INTEGER, \
		DP INTEGER, \
		FAO INTEGER, \
		FDP INTEGER, \
		FDVR INTEGER, \
		FR TEXT, \
		FRO INTEGER, \
		FSAF INTEGER, \
		FSAR INTEGER, \
		FSRF INTEGER, \
		FSRR INTEGER, \
		FWDB FLOAT, \
		FXX FLOAT, \
		GCM INTEGER, \
		HRUN INTEGER, \
		HS_ONLY INTEGER, \
		LEN INTEGER, \
		MLLD FLOAT, \
		OALT TEXT, \
		OID TEXT, \
		OMAPALT TEXT, \
		OPOS INTEGER, \
		OREF TEXT, \
		PB FLOAT, \
		PBP INTEGER, \
		PPD INTEGER, \
		QD FLOAT, \
		RBI FLOAT, \
		REFB FLOAT, \
		REVB FLOAT, \
		RO INTEGER, \
		SAF INTEGER, \
		SAR INTEGER, \
		SPD INTEGER, \
		SRF INTEGER, \
		SRR INTEGER, \
		SSEN INTEGER, \
		SSEP INTEGER, \
		SSSB FLOAT, \
		STB FLOAT, \
		STBP FLOAT, \
		TYPE TEXT, \
		VARB FLOAT, \
		NID TEXT, \
		MISA TEXT, \
		VCFALT TEXT, \
		VCFPOS INTEGER, \
		VCFREF TEXT, \
		MISC TEXT, \
		HS TEXT, \
		SUBSET TEXT, \
		PRIMARY KEY (runid, sampleid, chrom_pos_ref_alt) \
        )"))
		result_variant = conn.execute(text("CREATE TABLE IF NOT EXISTS variant ( \
		chrom_pos_ref_alt TEXT, \
		CHROM TEXT, \
		POS INTEGER, \
		ID TEXT, \
		REF TEXT, \
		ALT TEXT, \
		CLSF TEXT, \
		origPos INTEGER, \
		origRef TEXT, \
		normalizedRef TEXT, \
		gene TEXT, \
		normalizedPos INTEGER, \
		normalizedAlt TEXT, \
		polyphen FLOAT, \
		gt TEXT, \
		codon TEXT, \
		coding TEXT, \
		sift FLOAT, \
		grantham FLOAT, \
		transcript TEXT, \
		function TEXT, \
		protein TEXT, \
		location TEXT, \
		origAlt TEXT, \
		exon INTEGER, \
		oncomineGeneClass TEXT, \
		oncomineVariantClass TEXT, \
		CLNACC1 INTEGER, \
		CLNSIG1 TEXT, \
		CLNREVSTAT1 TEXT, \
		CLNID1 TEXT, \
		PRIMARY KEY (chrom, pos, ref, alt) \
        )"))
		result_interpret = conn.execute(text("CREATE TABLE IF NOT EXISTS interpret ( \
		runid TEXT, \
		sampleid TEXT, \
		GENLISTE TEXT, \
		chrom_pos_ref_alt TEXT, \
		SVARES_UT TEXT, \
		POPULASJONSDATA TEXT, \
		FUNKSJONSSTUDIER TEXT, \
		PREDIKTIVE_DATA TEXT, \
		CANCER_HOTSPOTS TEXT, \
		COMPUTATIONAL_EVIDENCE TEXT, \
		KONSERVERING TEXT, \
		ANDRE_DB TEXT, \
		KOMMENTAR TEXT, \
		ONCOGENICITY INTEGER, \
		TIER TEXT, \
		KOMMENTAR2 TEXT, \
		DATO TEXT, \
		BRUKER TEXT, \
		KOLONNE6 TEXT, \
		KOLONNE7 TEXT, \
		KOLONNE8 TEXT, \
		KOLONNE9 TEXT, \
		KOLONNE10 TEXT, \
		KOLONNE11 TEXT, \
		PRIMARY KEY (RUNID, SAMPLEID, chrom_pos_ref_alt) \
		)"))
		stmt = "create view all_data as select * \
			from vcf \
			left join variant \
			on vcf.chrom_pos_ref_alt = variant.chrom_pos_ref_alt \
			left join interpret \
			on vcf.chrom_pos_ref_alt = interpret.chrom_pos_ref_alt \
			and vcf.runid = interpret.runid \
			and vcf.sampleid = interpret.sampleid;"
		result_all = conn.execute(text(stmt))

def populate_vcfdb(db, df, run_id, sample_id, table):
	df = df.copy(deep=True)
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		df.insert(0, 'runid', len(df)*[run_id], True)
		df.insert(1, 'sampleid', len(df)*[sample_id], True)
		df["POS"]=df["POS"].astype(str)
		df.insert(2, 'chrom_pos_ref_alt', df[["CHROM", "POS", "REF", "ALT"]].agg("".join, axis=1))
		del df["CHROM"]
		del df["POS"]
		del df["REF"]
		del df["ALT"]
		del df["CLSF"]
		del df["FUNC"]
		df.to_sql(table ,con=conn,if_exists='append',index=False)
		conn.commit()		

def populate_variantdb(db, df, table):
	df = df.copy(deep=True)
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		df["POS"]=df["POS"].astype(str)
		df.insert(0, 'chrom_pos_ref_alt', df[["CHROM", "POS", "REF", "ALT"]].agg("".join, axis=1))
		df.to_sql(table ,con=conn,if_exists='append',index=False)
		conn.commit()		

def populate_interpretdb(db, df, table):
	df = df.copy(deep=True)
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		df["POS"]=df["POS"].astype(str)
		df.insert(2, 'chrom_pos_ref_alt', df[["CHROM", "POS", "REF", "ALT"]].agg("".join, axis=1))
		del df["CHROM"]
		del df["POS"]
		del df["REF"]
		del df["ALT"]
		df.to_sql(table,con=conn,if_exists='append',index=False)
		conn.commit()

#sqlite syntax - rewrite ...
def count_variant(db, chrom, pos, ref, alt, table):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    stmt = "SELECT COUNT(*) \
			FROM "+table+" \
            WHERE \
            	CHROM = '"+chrom+"' AND \
            	POS = '"+pos+"' AND \
				REF = '"+ref+"' AND \
            	ALT = '"+alt+"' \
            ;"
    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        for row in result:
            return row[0]

def list_runandsample_variant(db, chrom, pos, ref, alt, table):
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	pos = str(pos)
	stmt = "select \
				runid, sampleid \
			from \
				"+table+" \
			where \
				chrom_pos_ref_alt = '"+chrom+pos+ref+alt+"' \
			;"
	with engine.connect() as conn:
		result = conn.execute(text(stmt))
		for row in result:
			return row
