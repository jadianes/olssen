# Spectral search with Spark  

Experiences with Spark for spectral search.  

## Notebooks  

### [Loading a PRIDE Cluster library into a Spark RDD](read-spectrum-lib.ipynb)  

### [The SpectraST algorithm for spectral search](spectraST.ipynb)  

## The on-line spectral search server  

The file `server.py` uses [Flask](http://flask.pocoo.org/) to start a RESTful
web server wrapping a Spark context. Through its API we can perform on-line
spectral search.  

Run it using:

    /path/to/spark/bin/spark-submit server.py  

After loading the Spark context and the spectral search library, the server
will be ready to be queried at the following end points:  

- `/stats`: returns statistics about the spectral libraries that have been
loaded, including its name and peptide counts.  
 


