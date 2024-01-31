import configparser
import os


config = configparser.ConfigParser()
config.read('/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/variantbrowser/backend/config.ini')
#print(config["Paths"])

print(os.path.isfile("/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/variantbrowser/variantbrowser/backend/config.ini"))
print(os.path.isfile("/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/tests/test_db/test_db.db"))
print(os.path.isfile("/illumina/analysis/dev/2024/sigvla/fullFres_dev_2024/fullFres/tests/test_db/test_db_user.db"))