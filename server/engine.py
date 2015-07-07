import sys
from math import sqrt
from pyspark.mllib.linalg import Vectors

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
    """
    Returns a new spectrum without low intensity peaks
    """
    clean_peaks = [peak for peak in spectrum[1] if len(peak)==2 and peak[1]>=2.0]
    return (spectrum[0], clean_peaks)


def scale_peaks(spectrum):
    """
    Returns a new spectrum with scaled peaks
    """
    scaled_peaks = [(peak[0], sqrt(peak[1])) for peak in spectrum[1]]
    return (spectrum[0], scaled_peaks)


def to_bin(min_mz, bins, bin_size, value):
    """
    Assign a bin to a peak mz value
    """
    val = value - min_mz
    bin_i = int(val / bin_size)
    return bin_i + int(min_mz)


def bin_spectrum(spectrum):
    """
    Returns a new spectrum where peaks have been assigned to bins
    """
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
    """
    Returns a new spectrum with normalised peaks
    """
    magnitude = sqrt(sum([peak[1] ** 2 for peak in spectrum[1]]))
    norm_peaks = [(peak[0], peak[1]/magnitude) for peak in spectrum[1]]
    return (spectrum[0], norm_peaks)


def score_and_peptide(peptide, query_peaks_bc):
    """
    Given a peptide and a query, perform a dot product
    """
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


class SpectralSearch:
    """A spectral search engine
    """


    def get_stats(self):
        """Return stats from loeaded spectrum libraries
        """
        stats = []
        human_stats = {}
        human_stats['species'] = "human"
        human_stats['peptide_count'] = self.human_spectrum_library_RDD.count()
        stats.append(human_stats)
        contaminants_stats = {}
        contaminants_stats['species'] = "contaminants"
        contaminants_stats['peptide_count'] = self.contaminants_spectrum_library_RDD.count()
        stats.append(contaminants_stats)
        mouse_stats = {}
        mouse_stats['species'] = "mouse"
        mouse_stats['peptide_count'] = self.mouse_spectrum_library_RDD.count()
        stats.append(mouse_stats)

        return stats


    def search(self, query):
        """Return best pepetide matches for a given query
        """
        # we need to process the query peaks as we do with the spectrum lirbaries
        query = remove_low_intensity_peaks(("query", query))[1]
        query = scale_peaks(("query", query))[1]
        query = bin_spectrum(("query", query))[1]
        query = normalise_peaks(("query", query))[1]

        # then, we need to broadcast our query peaks to make it available accross the cluster workers
        query_peaks_bc = self.sc.broadcast(query)
        # then we can perform the dot product
        human_spectrum_library_vectors_RDD = \
            self.human_spectrum_library_with_bins_normalised_RDD.map(lambda peptide: score_and_peptide(peptide, query_peaks_bc))
        best_peptide_matches = \
            human_spectrum_library_vectors_RDD.takeOrdered(10, lambda pep_score: -pep_score[1])

        return best_peptide_matches


    def __process_library(self, spectrum_library_RDD):
        spectrum_library_denoise_RDD = \
            spectrum_library_RDD.filter(lambda peptide: len(peptide[1]) >= 6)
#        spectrum_library_denoise = \
#            spectrum_library_denoise.filter(lambda peptide: num_peaks_out_of_500_th(peptide)==0)
        spectrum_library_denoise_RDD = \
            spectrum_library_denoise_RDD.map(remove_low_intensity_peaks).filter(lambda peptide: len(peptide[1])>0).map(scale_peaks)
        spectrum_library_with_bins_RDD =  spectrum_library_denoise_RDD.map(bin_spectrum).cache()
        spectrum_library_with_bins_normalised_RDD = spectrum_library_with_bins_RDD.map(normalise_peaks)

        return spectrum_library_with_bins_normalised_RDD


    def __init__(self, sc):
        """
        Inits the search engine given a Spark context
        """
        self.sc = sc
        # load human library from pickle file
        self.human_spectrum_library_RDD = self.sc.pickleFile("../spectrumlibs/human/lib.file").cache()
        logger.info("Successfully loaded Human spectrum library")
        self.contaminants_spectrum_library_RDD = self.sc.pickleFile("../spectrumlibs/contaminants/lib.file").cache()
        logger.info("Successfully loaded Contaminants spectrum library")
        self.mouse_spectrum_library_RDD = self.sc.pickleFile("../spectrumlibs/mouse/lib.file").cache()
        logger.info("Successfully loaded Mouse spectrum library")

        logger.info("Preparing Human library for search ...")
        self.human_spectrum_library_with_bins_normalised_RDD = self.__process_library(self.human_spectrum_library_RDD)
        logger.info("Successfully pre-processed Human library: {} peptides left".format(self.human_spectrum_library_with_bins_normalised_RDD.count()))

        logger.info("Preparing Contaminant library for search ...")
        self.contaminants_spectrum_library_with_bins_normalised_RDD = self.__process_library(self.contaminants_spectrum_library_RDD)
        logger.info("Successfully pre-processed Contaminants library: {} peptides left".format(self.contaminants_spectrum_library_with_bins_normalised_RDD.count()))

        logger.info("Preparing Mouse library for search ...")
        self.mouse_spectrum_library_with_bins_normalised_RDD = self.__process_library(self.mouse_spectrum_library_RDD)
        logger.info("Successfully pre-processed Mouse library: {} peptides left".format(self.mouse_spectrum_library_with_bins_normalised_RDD.count()))
