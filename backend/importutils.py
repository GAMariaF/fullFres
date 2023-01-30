import os
import configparser
import sys
import zipfile
import shutil
import re
config = configparser.ConfigParser()
config.read('backend/config.ini')
sys.path.insert(0, config['Paths']['backend_path'])
sys.path.insert(0, config['Paths']['db_path'])
from vcfutils import parse_thermo_vcf
from vcfutils import explode_format_gt
from vcfutils import explode_info
from vcfutils import explode_func
from vcfutils import get_sample_id
from vcfutils import get_run_id
from vcfutils import get_percent_tumor
from vcfutils import get_sample_diseasetype
from vcfutils import get_sequencing_date
from dbutils import populate_thermo_variantdb

# list files and directories in import directory
folder = config['Paths']['db_test_path']

def importVcfXls(folder):
    dir_list = os.listdir(folder)
    if len(dir_list)%2 != 0:
        raise FileNotFoundError
    num_zip = 0
    for file in dir_list:
        if file.endswith('.zip'):
            num_zip += 1
            #excelfile = folder + '/' + re.split("_GX", file)[0].lower()+'_variants.xlsx'
            # Get excel file immediately to uncover potential error
            for fileexcel in dir_list:
                if fileexcel.startswith(re.split("_GX", file)[0].lower()):
                    excelfile = folder + '/' + fileexcel   
                    break
            else:
                raise ValueError 

            # unzip vcf-file
            with zipfile.ZipFile(folder +'/'+ file, 'r') as zip_ref:
                zip_ref.extractall(folder +'/'+ file[:-4] + 'TEMP')
            # copy file from unzip-folder to folder
            filezip = os.listdir(folder +'/'+ file[:-4] + 'TEMP')
            shutil.copyfile(folder +'/'+ file[:-4] + 'TEMP/' + filezip[0], \
                folder + '/' + file[:-4] + '.vcf')
            # remove extra files and folders
            os.remove(folder +'/'+ file)
            shutil.rmtree(folder +'/'+ file[:-4] + 'TEMP/')
            vcffile = folder + '/' + file[:-4] + '.vcf'
            # set up path to DB and get run_id, sample_id etc from vcffile
            db = config['Paths']['db_full_path']
            run_id = get_run_id(vcffile)
            sample_id = get_sample_id(vcffile)
            print(sample_id)
            percent_tumor = get_percent_tumor(vcffile)
            sample_diseasetype = get_sample_diseasetype(vcffile)
            sequencing_date = get_sequencing_date(vcffile)
            # TRANSFER VCF TO DATAFRAME
            df = parse_thermo_vcf(vcffile,excelfile)
            df = explode_format_gt(df)
            df = explode_info(df)
            dfvariant = df[["CHROM","POS","ID","REF","ALTEND","Type","FUNC"]]
            dfvariant = explode_func(dfvariant)
            # Adding column for assigning possible correction of annotation
            dfvariant['annotation_variant2']=dfvariant['annotation_variant']
            # INSERT DATA INTO TABLE SAMPLE, VARIANT AND INTERPRETATION
            populate_thermo_variantdb(db, df, dfvariant, \
                run_id, sample_id, percent_tumor, sample_diseasetype, sequencing_date)

        elif not file.endswith('.xlsx'):
            # Should only be zip and excel files in the folder.
            raise ValueError
            
    if num_zip == 0:
        raise ValueError

    rm_dir_list = os.listdir(folder)
    for rm_file in rm_dir_list:
        os.remove(folder +'/'+ rm_file)





