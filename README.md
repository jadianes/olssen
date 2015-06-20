# An on-line Spectral Search server  

Our server provides a RESTful-like API to perform **on-line spectral search** for proteomics
spectral data. It is based on the [SpectraST](http://tools.proteomecenter.org/wiki/index.php?title=Software:SpectraST) 
algorithm for spectral search and uses [PRIDE Cluster spectral libraries](http://wwwdev.ebi.ac.uk/pride/cluster/#/libraries).  

The server is buit for scalability and performance working with big datasets. It uses 
[Flask](http://flask.pocoo.org/) and performs its spectral searches on 
[Apache Spark](https://spark.apache.org/) clusters. It has a very simple 
deployment cycle (see next).  

## Quick start  

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

#### Examples  

    curl --data "query=[(514, 71.320754342617548),
  		(1030, 11.717081547894082),
  		(195, 7.6380625815713241),
  		(668, 160.64071712987339),
  		(545, 100.8157725755251),
  		(554, 75.973482215836341),
  		(699, 37.12007543095784)]" http://127.0.0.1:5000/search   

## Other tools  

### Spectrum library loader  
 
/TODO
 
## Concepts  

These are some IPython/Jupyter notebooks to explore different spectral search concepts and
procedures used in our on-line search server.  

### [Loading a PRIDE Cluster library into a Spark RDD](notebooks/read-spectrum-lib.ipynb)  

### [The SpectraST algorithm for spectral search](notebooks/spectraST.ipynb)  
