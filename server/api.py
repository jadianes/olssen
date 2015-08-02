from flask import Blueprint
main = Blueprint('main', __name__)

import json
from flask.ext.cors import CORS
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
    best_peptide_matches = []
    # Right now we are assuming exactly one file - TODO: process zero or more file into the same query or 
    # aggregate multiple results objects
    data = request.files.items()[0][1].read()
    query_list = data.strip().split("\n")
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

    # One of the simplest configurations. Exposes all resources matching /api/* to
    # CORS and allows the Content-Type header, which is necessary to POST JSON
    # cross origin.
    CORS(app, resources=r'/*', allow_headers='Content-Type')

    return app 
