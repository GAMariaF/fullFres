# read excel-file to dataframe
# send dataframe to four different
# tables in database.
import pandas as pd
from sqlalchemy import create_engine
import configparser

config = configparser.ConfigParser()
config.read('backend/config.ini')
db = config['Paths']['db_full_path']

excel = '/illumina/analysis/dev/2022/mfahls/fullFres/Tolkningsskjema_NyVersjon_130422_import3.xlsx'

dfTolkning = pd.read_excel(excel, header = 0)
dfTolkning.Perc_Tumor *= 100

colSamples              = ["runid", "sampleid", \
                                "Genelist", "Perc_Tumor", \
								"User_Signoff", "Date_Signoff", \
								"User_Approval", "Date_Approval"]
colVariantsPerSample    = ["runid", "sampleid", "CHROM_POS_ALTEND_DATE",\
								"DATE_CHANGED_VARIANT_BROWSER","Reply"]
colClassification       = ["CHROM_POS_ALTEND_DATE",\
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
colVariants             = [ "CHROM_POS_ALTEND_DATE", \
                                "CHROM", \
                                "POS", \
                                "ID", \
                                "REF", \
                                "ALTEND", \
                                "DATE", \
                                "Type", \
                                "gene", \
                                "exon", \
                                "oncomineGeneClass", \
                                "oncomineVariantClass", \
                                "origPos", \
                                "origRef", \
                                "normalizedRef", \
                                "normalizedPos", \
                                "normalizedAlt", \
                                "gt", \
                                "codon", \
                                "coding", \
                                "transcript", \
                                "annotation_variant", \
                                "function", \
                                "protein", \
                                "location", \
                                "origAlt", \
                                "CLNACC1", \
                                "CLNSIG1", \
                                "CLNREVSTAT1", \
                                "CLNID1", \
                                "polyphen", \
                                "sift", \
                                "grantham" ]

dfSamples           = pd.DataFrame(dfTolkning, columns = colSamples)
dfVariantsPerSample = pd.DataFrame(dfTolkning, columns = colVariantsPerSample)
dfClassification    = pd.DataFrame(dfTolkning, columns = colClassification)
dfVariants          = pd.DataFrame(dfTolkning, columns = colVariants)

dfSamples           = dfSamples.drop_duplicates()
dfVariantsPerSample = dfVariantsPerSample.drop_duplicates()
dfClassification    = dfClassification.drop_duplicates()
dfVariants          = dfVariants.drop_duplicates()

engine = create_engine("sqlite:///"+db, echo=False, future=True)
dfSamples.to_sql('Samples', engine, if_exists='append', index=False)
dfVariantsPerSample.to_sql('VariantsPerSample', engine, if_exists='append', index=False)
dfClassification.to_sql('Classification', engine, if_exists='append', index=False)
dfVariants.to_sql('Variants', engine, if_exists='append', index=False)