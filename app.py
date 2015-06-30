from flask import Blueprint
main = Blueprint('main', __name__)

import json
from engine import SpectralSearch

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from flask import Flask, request


@main.route("/stats", methods=["GET"])
def stats():
    logger.debug("Stats requested")
    stats = spectral_search.get_stats()
    return json.dumps(stats)


@main.route("/search", methods = ["POST"])
def search():
    # get the query spectrum from the request object
    query_list = request.form.keys()[0].strip().split("\n")
    query_list = map(lambda x: x.split(" "), query_list)
    query = map(lambda x: (int(float(x[0])), float(x[1])), query_list)
    # perform spectral search
    best_peptide_matches = spectral_search.search(query)

    return json.dumps(best_peptide_matches)


def create_app(spark_context):
    global spectral_search 
    spectral_search = SpectralSearch(spark_context)    
    
    app = Flask(__name__)
    app.register_blueprint(main)
    return app 
