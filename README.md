# Olssen 
### an OnLine Spectral Search ENgine  

Our engine provides a [RESTful-like API](https://github.com/olssen/olssen-ws) to perform **on-line spectral search** for proteomics
spectral data. It is based on the [SpectraST](http://tools.proteomecenter.org/wiki/index.php?title=Software:SpectraST) 
algorithm for spectral search and uses [PRIDE Cluster spectral libraries](http://wwwdev.ebi.ac.uk/pride/cluster/#/libraries).  

## Components  

[Olssen Web Service](https://github.com/jadianes/olssen-ws)  

The [server](https://github.com/olssen/olssen-ws) is buit for scalability and performance working with big datasets. It uses 
[Flask](http://flask.pocoo.org/) on top of [CherryPy's server](http://www.cherrypy.org/) 
and performs its spectral searches using an engine based on [Apache Spark](https://spark.apache.org/) 
clusters.  

[Olssen GUI](https://github.com/jadianes/olssen-gui)  

The client [Web Application](https://github.com/olssen/olssen-gui) can be used on top of the web service and is ideal for data visualisation and individual spectral search.  

![center](images/main_screenshot.png) 
![center](images/search_screenshot.png)

This project is generated with [yo angular generator](https://github.com/yeoman/generator-angular)
version 0.12.0.

