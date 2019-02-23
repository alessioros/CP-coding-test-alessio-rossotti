import zipfile
import os
import re
from constants import RECORD_HEADERS

def unzip_and_process_file(zip_path, output_path, db_utils, remove=False):
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    # extract only .txt files
    for file in zip_ref.namelist():
        file_info = zip_ref.getinfo(file).filename
        if file_info.endswith('.txt') and 'Geraete' in file_info:
                print('extracting and processing {}'.format(file))
                zip_ref.extract(file, output_path)
                process_file(os.path.join(output_path, file), db_utils, remove)

    zip_ref.close()
    if remove:
        os.remove(zip_path)

    return True

def process_file(file_name, db_utils, remove=False):
        variable_name = file_name.split('Geraete')[1][1:]
        variable_name = re.sub('\d', '', variable_name).replace('_.txt', '')

        with open(file_name, 'r') as input_file:
                # skip header
                line = input_file.readline()
                while line:
                        line = input_file.readline()
                        # avoid footer
                        if ';' in line:
                                values = line.strip().split(';')
                                values.insert(2, variable_name)
                                values = values[:-1]
                                db_utils.insert_data(values)
                        else:
                                break
        
        if remove:
                os.remove(file_name)
        return True

def format_record(record):
        record_json = {}
        for i in range(len(RECORD_HEADERS)):
                record_json[RECORD_HEADERS[i]] = record[i]
        

        return record_json