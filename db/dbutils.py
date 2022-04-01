import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

def generate_db()
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
            AF FLOAT, \


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