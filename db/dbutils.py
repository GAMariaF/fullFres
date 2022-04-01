import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

def generate_db(db):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    with engine.connect() as conn:
        result = conn.execute(text("CREATE TABLE IF NOT EXISTS interpret ( \
            runid TEXT, \
            sampleid TEXT, \
            chrom TEXT, \
            pos INTEGER, \
            id TEXT, \
            ref TEXT, \
            alt TEXT, \
            qual TEXT, \
            filter TEXT, \
            GQ INTEGER, \
            AF FLOAT, \
            AO INTEGER, \
            DP INTEGER, \
            FAO	INTEGER, \
            FDP	INTEGER, \
            FDVR INTEGER, \
            FR TEXT, \
            FRO	INTEGER, \
            FSAF INTEGER, \
            FSAR INTEGER, \
            FSRF INTEGER, \
            FSRR INTEGER, \
            FWDB FLOAT, \
            FXX	FLOAT, \
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
            VCFALT TEXT, \
            VCFPOS INTEGER, \
            VCFREF TEXT, \
            HS TEXT, \
            CLSF TEXT, \
            FUNC	[{'origPos':'25398284','origRef':'C','normalizedRef':'C','gene':'KRAS','normalizedPos':'25398284','normalizedAlt':'T','polyphen':'0.517','gt':'pos','codon':'GAT','coding':'c.35G>A','sift':'0.27','grantham':'94.0','transcript':'NM_033360.4','function':'missense','protein':'p.Gly12Asp','location':'exonic','origAlt':'T','exon':'2','oncomineGeneClass':'Gain-of-Function','oncomineVariantClass':'Hotspot','CLNACC1':'12582','CLNSIG1':'Pathogenic','CLNREVSTAT1':'criteria_provided,_multiple_submitters,_no_conflicts','CLNID1':'rs121913529'}]

            PRIMARY KEY (runid, sampleid, chrom, pos, alt) \
        )"))

#sqlite also input to def?
def populate_db(db, vcf_df, run_id, sample_id):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    with engine.connect() as conn:
        vcf_df.insert(0, 'runid', len(vcf_df)*[run_id], True)
        vcf_df.insert(1, 'sampleid', len(vcf_df)*[sample_id], True)
        vcf_df.to_sql('interpret',con=conn,if_exists='append',index=False)
        conn.commit()

#sqlite syntax - rewrite ...
def count_variant(db, chrom, pos, alt):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    stmt = "SELECT COUNT(*) FROM interpret \
            WHERE \
            chrom = '"+chrom+"' AND \
            pos = '"+pos+"' AND \
            alt = '"+alt+"' \
            ;"
    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        for row in result:
            return row[0]

def count_sample(db, sampleid):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    stmt = "SELECT COUNT(*) FROM interpret \
            WHERE \
            sampleid = '"+sampleid+"' \
            ;"
    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        for row in result:
            return row[0]


##### TEST #####
#runid = 'GX_0013'
#sampleid = '22SKH03041'
#chrom = 'chr1'
#pos = '27089668'
#alt = 'G'
#db = 'variant.db'

#xx = count_variant(db, chrom, pos, alt)
#yy = count_sample(db, sampleid)
#print( xx, yy)