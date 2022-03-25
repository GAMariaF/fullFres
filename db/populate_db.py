import pandas as pd
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text

def populate_db(db, vcf_df, run_id, sample_id):
    engine = create_engine("sqlite:///"+db, echo=True, future=True)
    with engine.connect() as conn:
        vcf_df.insert(0, 'runid', len(vcf_df)*[run_id], True)
        vcf_df.insert(1, 'sampleid', len(vcf_df)*[sample_id], True)
        vcf_df.to_sql('interpret',con=conn,if_exists='append',index=False)
        conn.commit()

db = 'variant.db'
vcf_df = pd.read_csv('vcf_dataframe2.csv')
run_id = 'GX_0013'
sample_id = '22SKH03044'

#if no database
#engine = create_engine("sqlite:///"+db, echo=True, future=True)
#with engine.connect() as conn:
#    result = conn.execute(text("CREATE TABLE IF NOT EXISTS interpret ( \
#        runid TEXT, \
#        sampleid TEXT, \
#        chrom TEXT, \
#        pos INTEGER, \
#        id TEXT, \
#        ref TEXT, \
#        alt TEXT, \
#        qual TEXT, \
#        filter TEXT, \
#        AF FLOAT, \
#        PRIMARY KEY (runid, sampleid, chrom, pos, alt) \
#    )"))

populate_db(db, vcf_df, run_id, sample_id)