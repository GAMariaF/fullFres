import sqlite3
import sqlalchemy
from sqlalchemy import update
from sqlalchemy import create_engine
from sqlalchemy import text
import argparse
import sys
import configparser
config = configparser.ConfigParser()
config.read('../backend/config.ini')

try:
    from sys.stdin import buffer as std_in
    from sys.stdout import buffer as std_out
except ImportError:
    from sys import stdin as std_in
    from sys import stdout as std_out



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-S", metavar="sampleid", default=std_in, help="The ID of the sample which should be unapproved and unsigned.")
    args = parser.parse_args()

    db = config['Paths']['db_full_path']

    engine = create_engine("sqlite:///"+db, echo=False, future=True)

    stmt = f"DELETE FROM Samples WHERE sampleid = '{args.S}';"
    stmt2 = f"DELETE FROM VariantsPerSample WHERE sampleid = '{args.S}';"

    with engine.connect() as conn:
        result = conn.execute(text(stmt))
        result2 = conn.execute(text(stmt2))
        conn.commit()

if __name__ == "__main__":
    main()