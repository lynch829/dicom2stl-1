#!/usr/bin/python

import os, shutil, sys, getopt, datetime

start = datetime.datetime.now()

def main(argv):

    clean_tmp = True
    dicom_dir = ''
    output = ''
    isovalue = 150
    lowq_threshold = 100

    try:
        opts, args = getopt.getopt(argv,"hi:o:n:v:q:",["ifolder=","ofolder=","noclean","value=", "qualityt="])
    except getopt.GetoptError:
        print('USAGE: dicom2skull_pipe.py -i <input_dicom_folder> -o <output_folder> -n <no_clean> --value <num> --qualityt <num>')
        sys.exit()
        exit()
    for opt, arg in opts:
        if opt == '-h':
            print('USAGE: dicom2skull_pipe.py -i <input_dicom_folder> -o <output_folder> -n <no_clean> --value <num> --qualityt <num>')
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            dicom_dir = arg
        elif opt in ("-o", "--ofolder"):
            output = arg
        elif opt in ("-n", "--no_clean"):
            clean_tmp = False
        elif opt in ("-v", "--value"):
            isovalue = float(arg)
        elif opt in ("-q", "--qualityt"):
            lowq_threshold = int(arg)

    # temporary directory to store stl 1st stage files:
    pwd = os.getcwd()
    tmp_dir = pwd + '/tmp/'
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)    

    # Executing 1st stage: dicom2stl:
    os.system(f"python3 dicom2stl_tuned.py -c -i {isovalue} -q {lowq_threshold} -o {tmp_dir} {dicom_dir}")

    # Executing 2nd stage: Skull-extraction:
    os.system(f"python3 skull_extraction.py -i {tmp_dir} -o {output}")

    # Clean tmp directory:
    if clean_tmp:
        shutil.rmtree(tmp_dir)
        print('\n Temp. directory succesfully removed.')

    print('\n\nFULL PIPELINE EXECUTION TIME: ', datetime.datetime.now() - start, '\n')

if __name__ == "__main__":
   main(sys.argv[1:])
