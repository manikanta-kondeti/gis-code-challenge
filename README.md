# gis-code-challenge
The code challenge for the position Software Developer, GIS. For Question refer to this link: https://github.com/door2door-io/gis-code-challenge

# Solution to gis-code-challenge

## How to run?
```
git clone https://github.com/manikanta-kondeti/gis-code-challenge
bash script.sh 
python server.py

Open http://localhost:8080/busstops to check the results.
```


## Algorithm:
We have points(X,Y) and routes as Linestrings [ (X,Y) ]. Let us explore the possibilities for P being a bus stop. For the sake of this document we’ll refer to P as Point(X,Y) and Way as Route(A,B).

  The sequence of steps(Algorithm) we followed to extract the bus stops are the following:
1. Filter all the activity points(P) based on their previous activity, current activity and speed.
  * P having
	  * pda == “in_vehicle”  or cda in [ “on_foot”, “on_bicycle”, “still”, "NULL" ] and speed < 70
    * cda == “in_vehicle”  or pda in [ “on_foot”, “on_bicycle”, “still” , "NULL"] and speed < 70

2. Remove all the features(points) which are not intersecting with routes. Buffer the point around 50m and check the intersections with given routes json file(I have used OGR python library for buffering and intersections) -- (We can optimize this step in terms of computations).

3. (This step is not yet done)Re-filter the points based on their attributes again. The reason for not thinking about this step is because the given activity points are not coinciding with actual bus stops that were extracted from Google Maps. However the architechture to complete this step is in place already.
   (Basic architecture setup is done and Need to rethink for this step)

## Code: 

* The entire application is wrriten in both python and javascript (along with html & css).
* `python server.py` starts the server and runs the application on port 8080 
* Open localhost:8080/busstops  in browser, which hits WebPageHandler class in server.py
* server.py : This file has Webhandlers to handle the incoming request, then run the algorithm(those 2 steps described above) and send web page(views/wms.html) as response along with little extra information using jinja2 library(For dynamic templates in webapp2).
* Modules:
  * Algorithm
  	* Method1 : Filter activity points based on attributes(Described above in step1) 
  	* Method2 : Remove activity points  which are not intersecting with given routes (Describe above in Step2) 
  * Utils
  	* GeoJson: This class holds the geojson data and also has methods that are useful to read and hold the json features in memory.
  	* WKT : This format is useful while doing buffer and intersections.  
* Views:
  * wms.html :
    * This html document also has javascript code that gets data from server.py/WebPageHandler(webhandler)
    * This web page displays three geojson vector layers.
      * Extracted Bus stops: Bus stops  that are extracted from the Algorithm mentioned
      * Bus stops that are extracted from Google maps(manual).
      * Routes : This file is given as input.

## Test: 
* Open models/Algorithm.py, Add your method or change the filtering conditions
* Save the changes and restart the server.
* Open http://localhost:8080/busstops to check the result.

** You can use print statements for debugging purposes.

## Knowledge and insights on the data given:


* Added all the vector data files(routes.json, activity_points.json and results.json from running above Algorithm) as vector layers in QGIS. Dots represented in Red color are the output from algorithm and green represents activity points.
![alt tag](https://postimg.org/image/b4df5sipr/)

* Also I have exported Dar es salaam busstops information from Goolge Maps as kml and converted into geojson. Added it as a layer to check the correlation between activity points and actual bus stops. Unfortunately I can not see any activity point(380) coincide with actual bus stops(10) from Google.

![alt tag](https://postimg.org/image/c8mhosit3/)


* However based on tweaking above buffered distance in step 2: I got various results
  * buffer_distance = 0.0005   -> 43 points
  * buffer_distace = 0.00005   -> 24 points.

* Also in step-1 if we add speed < 70, 
  * buffer_distance = 0.0005 and speed < 70 --> 6 points 
  * buffer_distace = 0.005 and speed < 70 --> 14 points


  