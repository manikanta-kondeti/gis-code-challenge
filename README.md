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
1. Filter all the activity points(P) based on their previous activity, current activity, their respective confidence attributes, speed and accuracy.
  * P having
	* pda == “in_vehicle”  or cda in [ “on_foot”, “on_bicycle”, “still” ]
    * cda == “in_vehicle”  or pda in [ “on_foot”, “on_bicycle”, “still” ]

2. Remove all the features(points) which are not intersecting with routes. Buffer the point around 10m and check the intersections(I have used OGR python library for buffering and intersections) -- (We can optimize this step).

3. Re-filter the points based on their attributes again.(This step is not yet done) because the  activity points are not coinciding with actual bus stops that were extracted from Google Maps.
   (Basic architecture is setup and Need to rethink for this step)

## Code: 

* The entire application is wrriten in both python and javascript (along with html & css).
* python server.py starts the server and runs the application on port 8080 
* When the user opens localhost:8080/busstops, it calls WMSWebPage in server.py
* server.py : Webhandlers to handle the request, run the algorithm and web page as response.
* Modules:
  * Algorithm
  	* Step1 : Filter activity points based on attributes 
  	* Step2 : Remove activity points  which are not intersecting with routes  
  * Utils
  	* GeoJson: This class holds the geojson data and methods are useful to read and write back the contents.
  	* WKT : This format is useful while doing buffer and intersections.  
* Views:
  * wms.html :
    * This html document also has javascript code that gets data from server.py/WMSWebPage(webhandler)
    * This web page displays three geojson vector layers.
      * Extracted Bus stops: Bus stops  that are extracted from the Algorithm mentioned
      * Bus stops that are extracted from Google maps(manual).
      * Routes : This file is given as input.

