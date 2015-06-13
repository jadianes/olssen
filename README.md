# Spectral search with Spark  

Experiences with Spark for spectral search.  

## Notebooks  

Some IPython/Jupyter notebooks to explore different spectral search
concepts.  

### [Loading a PRIDE Cluster library into a Spark RDD](notebooks/read-spectrum-lib.ipynb)  

### [The SpectraST algorithm for spectral search](notebooks/spectraST.ipynb)  

## The on-line spectral search server  

The file `server.py` uses [Flask](http://flask.pocoo.org/) to start a RESTful
web server wrapping a Spark context. Through its API we can perform on-line
spectral search.  

Run it using:

    /path/to/spark/bin/spark-submit server.py  

After loading the Spark context and the spectral search library, the server
will be ready to be queried at the following end points, (speaking JSON 
format):  

- `GET /stats`: returns statistics about the spectral libraries that have been
loaded, including its name and peptide counts.  
 
- `POST /search`: spectral search for a given peak list as an array of 
(mz, intensity) pairs.  

