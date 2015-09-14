import os, argparse
from pyspark import SparkContext, SparkConf

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_spark_context():
    # load spark context
    conf = SparkConf().setAppName("create-lib-file")
    sc = SparkContext(conf=conf)

    return sc


def parse_file_entry(file_entry):
    """Parse a line in the format:
    /path/to/file file_contents
    """
    # each file entry is a tuple with the first element being the file path and the second its contents
    file_split = file_entry[1].split("\n")
    # name is the first element in the split, we need to remove the 'name: ' prefix
    name = file_split[0].split(" ")[1]
    # number of peaks is the third element, removed 'Num peaks: ' prefix
    num_peaks = int(file_split[2].split(" ")[2])
    # read the peaks themselves, that are in the next num_peaks lines, space separated (there is an extra space after each peak)
    peak_list = [tuple(map(float, peak.split(" ")[0:2])) for peak in file_split[3:3+num_peaks]]
    
    return (name, peak_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("split_folder", help="The folder where the PRIDE Cluster library split resides")
    parser.add_argument("lib_file", help="The destination file where the RDD representing the spectrum library will be persisted to")
    args = parser.parse_args()

    # Init spark context and load libraries
    sc = init_spark_context()

    # Load it
    logger.info("Loading the split in folder %s into an RDD...", args.split_folder)
    logger.info("There are %s spectrum files in the folder", \
        len([name for name in os.listdir(args.split_folder) if os.path.isfile(os.path.join(args.split_folder, name))]))
    raw_files_RDD = sc.wholeTextFiles (args.split_folder)
    # Parse files with content length > 0 (some files happen to be empty!)
    spectrum_library_RDD = raw_files_RDD.filter(lambda x: len(x[1])>0).map(parse_file_entry)
    logger.info("Library loaded with %s peptides", spectrum_library_RDD.count())

    # Save it
    logger.info("Persisting RDD into file %s", args.lib_file)
    spectrum_library_RDD.saveAsPickleFile(args.lib_file)
    logger.info("Library persisted")


if __name__ == '__main__':
    main()
