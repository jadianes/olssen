#!/usr/bin/env python

import sys, json
from math import sqrt

try:
    from pyspark import SparkContext, SparkConf
    from pyspark.mllib.linalg import Vectors
    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

from flask import Flask, request
app = Flask(__name__)

@app.route("/stats", methods=["GET"])
def stats():
    stats = []
    human_stats = {}
    human_stats['species'] = "human"
    human_stats['peptide_count'] = human_spectrum_library.count()
    stats.append(human_stats)
    return json.dumps(stats)


@app.route("/search", methods = ["POST"])
def search():
    # get the query spectrum from the request object
    query_list = request.form.keys()[0].strip().split("\n")
    query_list = map(lambda x: x.split(" "), query_list)
    query = map(lambda x: (int(float(x[0])), float(x[1])), query_list)
    # we need to process the query peaks as we do with the spectrum lirbaries
    query = remove_low_intensity_peaks(("query", query))[1]
    query = scale_peaks(("query", query))[1]
    query = bin_spectrum(("query", query))[1]
    query = normalise_peaks(("query", query))[1]

    # we need to broadcast our query peaks to make it available accross the cluster workers
    query_peaks_bc = sc.broadcast(query)
    # then we can perform the dot product
    human_spectrum_library_vectors = \
        human_spectrum_library_with_bins_normalised.map(lambda peptide: score_and_peptide(peptide, query_peaks_bc))
    best_peptide_matches = \
        human_spectrum_library_vectors.takeOrdered(10, lambda pep_score: -pep_score[1])

    return json.dumps(best_peptide_matches)


def num_peaks_out_of_500_th(spectrum):
    """
    Count the number of peaks out of 500 thomson in the M/Z range
    """
    charge = int(spectrum[0].split("/")[-1])
    peaks_out = [peak for peak in spectrum[1] if peak[0]>(charge*500.0)]
    if not peaks_out:
        return 0
    else:
        return len(peaks_out)


def remove_low_intensity_peaks(spectrum):
    clean_peaks = [peak for peak in spectrum[1] if len(peak)==2 and peak[1]>=2.0]
    return (spectrum[0], clean_peaks)


def scale_peaks(spectrum):
    scaled_peaks = [(peak[0], sqrt(peak[1])) for peak in spectrum[1]]
    return (spectrum[0], scaled_peaks)


def to_bin(min_mz, bins, bin_size, value):
    val = value - min_mz
    bin_i = int(val / bin_size)
    return bin_i + int(min_mz)


def bin_spectrum(spectrum):
    ## TODO: do we use charge to convert Th to Da?
    peak_mzs = [peak[0] for peak in spectrum[1]]
    min_mz = min(peak_mzs)
    max_mz = max(peak_mzs)
    
    bins = xrange(int(min_mz), int(max_mz)+1, 1)
    # associate peaks with bins
    peaks_with_bins_list = [(to_bin(min_mz,bins,1, peak[0]), peak[1]) for peak in spectrum[1]]
    peaks_with_bins_dict = {}
    for peak in peaks_with_bins_list:
        if peak[0] in peaks_with_bins_dict:
            peaks_with_bins_dict.get(peak[0]).append(peak[1])
        else:
            peaks_with_bins_dict[peak[0]] = [peak[1]]
        
    # merge bins at the same mz value by averaging their peak intensities
    peaks_with_bins = [(peak[0], sum(peak[1])/len(peak[1])) for peak in peaks_with_bins_dict.items()]
    return (spectrum[0], peaks_with_bins)


def normalise_peaks(spectrum):
    magnitude = sqrt(sum([peak[1] ** 2 for peak in spectrum[1]]))
    norm_peaks = [(peak[0], peak[1]/magnitude) for peak in spectrum[1]]
    return (spectrum[0], norm_peaks)


def score_and_peptide(peptide, query_peaks_bc):
    
    # get max vector size based on bins
    peptide_mz_bins = [peak[0] for peak in peptide[1]]
    query_mz_bins = [peak[0] for peak in query_peaks_bc.value]
    max_bin_peptide = max(peptide_mz_bins)+1
    max_bin_query = max(query_mz_bins)+1
    max_size = max(max_bin_peptide,max_bin_query)
    
    # Create SparseVector for peptide
    peptide_sv = Vectors.sparse(max_size, peptide[1])

    # Create a SparseVector the query 
    query_sv = Vectors.sparse(max_size, query_peaks_bc.value)
    
    # return peptide and dot product result
    return (peptide[0], peptide_sv.dot(query_sv))



if __name__ == "__main__":
    # load spark context
    conf = SparkConf().setAppName("spectral-search-server") \
      .set("spark.executor.memory", "6g")
    sc = SparkContext(conf=conf)

    # load human library from pickle file
    human_spectrum_library = sc.pickleFile("./human/lib.file").cache()
    print "Successfully loaded Human spectrum library"

    print "Preparing Human library for search ..."

    human_spectrum_library_denoise = \
        human_spectrum_library.filter(lambda peptide: len(peptide[1]) >= 6)
    
#    human_spectrum_library_denoise = \
#        human_spectrum_library_denoise.filter(lambda peptide: num_peaks_out_of_500_th(peptide)==0)

    human_spectrum_library_denoise = \
        human_spectrum_library_denoise.map(remove_low_intensity_peaks).filter(lambda peptide: len(peptide[1])>0).map(scale_peaks)    

    human_spectrum_library_with_bins = \
        human_spectrum_library_denoise.map(bin_spectrum).cache()

    human_spectrum_library_with_bins_normalised = \
        human_spectrum_library_with_bins.map(normalise_peaks)

    print "Successfully pre-processed Human library: {} peptides left".format(human_spectrum_library_with_bins.count())

    # start server, visible outside localhost
    app.run(host= '0.0.0.0', port = 5432)

