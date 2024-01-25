#!/bin/bash

date=$(date '+%Y%m%d')

sqlite3 /illumina/analysis/fullFres/db/variantdb.db ".backup /illumina/analysis/fullFres/db/backup/variantdb_$date.db"

# For copying db to other machine on network.
rsync -ae ssh /illumina/analysis/fullFres/db/backup/variantdb_"$date".db \
	"[user@ip]:/illumina/runs_diag/fullFres/variant_db_backup/variantdb_"$date".db
