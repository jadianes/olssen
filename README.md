# Olssen Web Service  

Our server provides a RESTful-like API to perform **on-line spectral search** for proteomics
spectral data. It is based on the [SpectraST](http://tools.proteomecenter.org/wiki/index.php?title=Software:SpectraST) 
algorithm for spectral search and uses [PRIDE Cluster spectral libraries](http://wwwdev.ebi.ac.uk/pride/cluster/#/libraries).  

The server is buit for scalability and performance working with big datasets. It uses 
[Flask](http://flask.pocoo.org/) on top of [CherryPy's server](http://www.cherrypy.org/) 
and performs its spectral searches using an engine based on [Apache Spark](https://spark.apache.org/) 
clusters. The server has a very simple deployment cycle (see next).  

## Quick start  

The file `server/server.py` starts a [CherryPy](http://www.cherrypy.org/) server running a 
[Flask](http://flask.pocoo.org/) `app.py` to start a RESTful
web server wrapping a Spark-based `engine.py` context. Through its API we can 
perform on-line spectral search for proteomics data.  

In order to have the server working properly, the PRIDE Cluster libraries must
be downloaded and processed into the right folders. See **Getting the Libraries**.  

Once you have the libraries ready, run the server using:

    /path/to/spark/bin/spark-submit server.py  

Or have a look at the provided `start_server.sh` script as a guide.
After loading the Spark context and the spectral search library, the server
will be ready to be queried at the following end points, (speaking JSON 
format):  

- `GET /stats`: returns statistics about the spectral libraries that have been
loaded, including its name and peptide counts.  
 
- `POST /search`: spectral search for a given peak list as an array of 
(mz, intensity) pairs.  

#### Examples  

    curl --data-binary @samples/query.mgf http://<server_IP>:5432/search   

Where the file `query.mgf` contains the list of peaks to search for, and
`<server_IP>` is the IP address of the host where `server.py` is running.
Here we are asuming that we are at the root where `samples/` folder is located.      

## Getting the libraries  

In order to have the server working properly, we must have the PRIDE Cluster
spectrum libraries available for the Spark cluster. Each of the libraries has
to be downloaded using `tools/download_and_split_lib.py` and processed using
`tools/create_lib_file.py`. The final location of the libraries is hardcoded in the
server in the current version. So, from the folder where the server is started:  

- ../spectrumlibs/human/lib.file  
- ../spectrumlibs/mouse/lib.file  
- ../spectrumlibs/contaminants/lib.file  

How to use the two Python scripts is described below.  

#### `download_and_split_lib.py`  
 
This Python script downloads a PRIDE Cluster library and split it into a local folder. Example of use:

    python download_and_split_lib.py ftp://ftp.pride.ebi.ac.uk/pride/data/cluster/spectrum-libraries/1.0.1/Contaminants.msp.gz ./contaminants  

#### `create_lib_file.py`  

This Spark/Python script loads a split folder (created with the `download_and_split_lib.py` tool) into an RDD and persist it as a 
pickle file for later use by the server. Use it through the provided shell script, for example:  

    ./create_lib_file.sh ../spectrumlibs/contaminants ../spectrumlibs/contaminants/lib.file  

 
## Concepts  

These are some IPython/Jupyter notebooks to explore different spectral search concepts and
procedures used in our on-line search server.  

### [Loading a PRIDE Cluster library into a Spark RDD](notebooks/read-spectrum-lib.ipynb)  

### [The SpectraST algorithm for spectral search](notebooks/spectraST.ipynb)  
