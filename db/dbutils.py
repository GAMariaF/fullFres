import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

def generate_db(db):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    with engine.connect() as conn:
        result_vcf = conn.execute(text("CREATE TABLE IF NOT EXISTS vcf ( \
		runid TEXT, \
		sampleid TEXT, \
		chrom TEXT, \
		POS INTEGER, \
		ID TEXT, \
		REF TEXT, \
		ALT TEXT, \
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
		PRIMARY KEY (runid, sampleid, chrom, pos, ref, alt) \
        )"))
        result_interpret = conn.execute(text("CREATE TABLE IF NOT EXISTS interpret ( \
		runid TEXT, \
		sampleid TEXT, \
		GENLISTE TEXT, \
		chrom TEXT, \
		POS TEXT, \
		REF TEXT, \
		ALT TEXT, \
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
		KOLONNE6 TEXT, \
		KOLONNE7 TEXT, \
		KOLONNE8 TEXT, \
		KOLONNE9 TEXT, \
		KOLONNE10 TEXT, \
		KOLONNE11 TEXT, \
		PRIMARY KEY (RUNID, SAMPLEID, CHROM, POS, REF, ALT) \
		)"))

def populate_vcfdb(db, vcf_df, run_id, sample_id):
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		vcf_df.insert(0, 'runid', len(vcf_df)*[run_id], True)
		vcf_df.insert(1, 'sampleid', len(vcf_df)*[sample_id], True)
		vcf_df.to_sql('vcf',con=conn,if_exists='append',index=False)
		conn.commit()

def populate_db(db, vcf_df, table):
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	with engine.connect() as conn:
		vcf_df.to_sql(table,con=conn,if_exists='append',index=False)
		conn.commit()

#sqlite syntax - rewrite ...
def count_variant(db, chrom, pos, alt, table):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    stmt = "SELECT COUNT(*) \
			FROM "+table+" \
            WHERE \
            	chrom = '"+chrom+"' AND \
            	pos = '"+pos+"' AND \
            	alt = '"+alt+"' \
            ;"
    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        for row in result:
            return row[0]

def list_runandsample_variant(db, chrom, pos, ref, alt, table):
	engine = create_engine("sqlite:///"+db, echo=True, future=True)
	stmt = "select \
				runid, sampleid \
			from \
				"+table+" \
			where \
				chrom = '"+chrom+"' \
				and POS = '"+pos+"' \
				and REF = '"+ref+"' \
				and ALT = '"+alt+"' \
			;"
	with engine.connect() as conn:
		result = conn.execute(text(stmt))
		for row in result:
			return row
