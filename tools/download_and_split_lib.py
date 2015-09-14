import os, gzip, urllib, argparse

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def split_library(lib_path, destination_folder):
    # create destination folder if needed
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
        
    # open library file for reading
    input_f = gzip.open(lib_path, 'rb')
    
    # open destination file for writing
    i = 0
    target_f = open(os.path.join(destination_folder,str(i)+".mgf"), 'w')
    
    # process input library file
    for line in input_f.readlines():
        if line=="\n": # end of spectrum, move to next file
            target_f.close()
            i+=1
            target_f = open(os.path.join(destination_folder,str(i)+".mgf"), 'w')
        else: # write line
            target_f.write(line)

    target_f.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("lib_url", help="The URL of the PRIDE Cluster lib to download")
    parser.add_argument("destination_folder", help="The local folder where the library will be processed")
    args = parser.parse_args()

    # Download the library file
    lib_file_name = args.lib_url.split("/")[-1]
    logger.info("Downloading library file at %s as %s", args.lib_url, lib_file_name)
    f = urllib.urlretrieve (args.lib_url, lib_file_name)
    logger.info("Library file donwload complete")

    # Split the library file
    logger.info("Splitting library file into folder %s", args.destination_folder)
    split_library(lib_file_name, args.destination_folder)
    logger.info("Library file splitting complete")

    
    

if __name__=='__main__':
    main()
