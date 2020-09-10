#!/usr/bin/python

# DCM organizer script:
#   - To organize directory full of DCM files into a subdirectories based on SeriesInstanceUID 
#     to be able to execute the dicom2stl script.
# Author: Juan F. Pinzon, Academgene LLC
# 09.2020

import os, shutil, sys, getopt, json, datetime
import pydicom
from tqdm import tqdm

def main(argv):

    start = datetime.datetime.now()

    BODYPART = 'HEAD'
    MODALITY = 'CT'
    LOG_FNAME = os.getcwd() + '/logs/dcm_org.log'
    seriesUID = []
    counter = 0
    error_count = 0

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifolder=","ofolder="])
    except getopt.GetoptError:
        print('USAGE: dcm_organizer.py -i <input_dicom_folder> -o <output_folder> ')
        sys.exit()
        exit()

    for opt, arg in opts:
        if opt == '-h':
            print('USAGE: dcm_organizer.py -i <input_dicom_folder> -o <output_folder>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            SRC = arg
        elif opt in ("-o", "--ofolder"):
            OUT = arg

    #loading the log file in order to exclude already processed series
    try:
        with open(LOG_FNAME, 'r') as infile:
            processed_dcms = set(json.load(infile))
    except:
        processed_dcms = set()

    input_dcms = os.listdir(SRC)

    #excluding already processed files
    input_dcms = [x for x in input_dcms if x not in processed_dcms]

    for i, dcm in tqdm(enumerate(input_dcms), total=len(input_dcms)):
        try:
            ds = pydicom.dcmread(SRC + input_dcms[i])
            if ds.Modality == MODALITY and ds.BodyPartExamined == BODYPART:
                out_dir = OUT + ds.SeriesInstanceUID
                src_path = SRC + dcm
                out_path = out_dir + '/' + dcm
                if not os.path.exists(out_dir):
                    os.makedirs(out_dir)
                shutil.move(src_path, out_path)
                counter += 1
                if ds.SeriesInstanceUID not in seriesUID: 
                    seriesUID.append(ds.SeriesInstanceUID)  
        except Exception as e:
            print('Error processing file: ', dcm, str(e), '\n')
            error_count += 1
            continue

    #updating and writing the log
    processed_dcms.update(seriesUID)
        
    with open(LOG_FNAME, 'w') as infile:
        json.dump(list(processed_dcms), infile)

    
    print(counter, ' files organized')
    print('Into ', len(seriesUID), ' unique Series sub-directories')
    print('# of Errors found: ', error_count, ' - {0:.0%}'.format(error_count/counter))
    print('Execution Time: ', datetime.datetime.now() - start)

if __name__ == "__main__":
   main(sys.argv[1:])