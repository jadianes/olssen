#!/usr/bin/env python

import sys, json

try:
    from pyspark import SparkContext, SparkConf
    from pyspark.mllib.clustering import KMeans
    from pyspark.mllib.feature import StandardScaler
    print ("Successfully imported Spark Modules")
except ImportError as e:
    print ("Can not import Spark Modules", e)
    sys.exit(1)

from flask import Flask
app = Flask(__name__)

@app.route("/stats")
def stats():
    stats = []
    human_stats = {}
    human_stats['species'] = "human"
    human_stats['peptide_count'] = human_spectrum_library.count()
    stats.append(human_stats)
    return json.dumps(stats)

if __name__ == "__main__":
    # load spark context
    conf = SparkConf().setAppName("spectral-search-server") \
      .set("spark.executor.memory", "6g")
    sc = SparkContext(conf=conf)

    # load human library from pickle file
    human_spectrum_library = sc.pickleFile("./human/lib.file").cache()
    print "Human library loaded"

    # start server
    app.run()

