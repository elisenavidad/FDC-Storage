#Technical Specifications

##Software Details

This application was built for the purpose of computing reservoir volumes and flow-duration curves from a specified location and a specific curve number within the Dominican Republic (<a href="http://tethys.byu.edu/apps/storage-capacity/" target="_blank">Click here to go to the app</a>). The application builds on the work done by Michael Souffront in the Storage Capacity app.  The application was designed using a python script, which was added to an ArcGIS Server as a geoprocessing service, and Tethys platform in combination with the ArcGIS API for JavaScript for the front end of the app. This application was created by Elise Jackson.

For best results, ensure that pop-ups are allowed in the web browser.  This enables the results page to open when the analysis has finished.  The analysis takes an average of 7 minutes to run. Do not click within the map window while the process is running. 

####Installation:

######Prerequisites:
- Tethys Platform

Clone the repository:
```
$ git clone https://github.com/elisenavidad/FDC-Storage.git
```
Then install the app in Tethys Platform.

######Installation for App Development:
```
$ . /usr/lib/tethys/bin/activate
$ cd tethysapp-storage_capacity
$ python setup.py develop
$ tethys docker start
$ tethys manage start
```
######Installation for Production:
- For production installation follow the instructions in the following link: http://docs.tethysplatform.org/en/latest/production/app_installation.html

####Compatibility and Limitations

This application only works within the Dominican Republic. However, this same setup can be used with raster data from other places in order to get the app working at a different location. The features contained in this application are cross browser and will work with most current browsers. However, only Google Chrome and Mozilla Firefox were tested. Full functionality for other current browsers is expected but not guaranteed. An ArcGIS Server and general GIS knowledge is needed in order to implement the backend portion of this app; that is, preparing and loading raster and vector data and publising a geoprocessing service to an ArcGIS Server in order to calculate and store reservoir volume.

####License

This application is licensed under an open source MIT license.

####Application Design

A simple approach was taken when designing the front end part of the app. A help guide is provided in the app in case any of the steps necessary to run the app is not clear enough. The application was designed as a two-page website. It can be accessed from BYU Tethys portal (http://tethys.byu.edu/) as shown in Figure 1 below. A zoomed in image of the buttons used to calculate a potential dam and reservoir volume, and generate the flow-duration curve is shown in Figure 2. After running the application successfully, the calculated reservoir will appear on the main map window with the calculated reservoir volume in cubic meters, shown in Figure 3.  The flow-duration curve can be found on the results page of the application which automatically opens in a new browser window, shown in Figure 4. Ensure that pop-ups are allowed to view the Results page.  The analysis averages a 5-minute runtime.  Do not click on the map during analysis, or the geoprocessing task will reset. 

An alternative to using Tethys is possible, since this app mainly used the ArcGIS API for JavaScript for most of 
its functionality (see main.js file in the repository), however, an HTML page together with styling would need to be 
developed from zero to pursue this alternative.

<img border=0 width=396 height=245 id="Picture 1"
src="https://github.com/msouff/storageCapacityDR/blob/master/tethysapp/storage_capacity/public/images/chooseappSCREENSHOT.JPG">

Figure 1. Home page of Tethys Portal to access Storage Capacity-FDC application.

<img border=0 width=301 height=340 id="Picture 3"
src="https://github.com/elisenavidad/FDC-Storage/blob/master/tethysapp/storage_capacity/public/images/Functionality.png">

Figure 2. Functions used to properly run the application.

<img border=0 width=624 height=357 id="Picture 4"
src="https://github.com/elisenavidad/FDC-Storage/blob/master/tethysapp/storage_capacity/public/images/appScreenshot">

Figure 3. Final result after successfully running the Storage Capacity application.

<img border=0 width=624 height=357 id="Picture 6"
src="https://github.com/elisenavidad/FDC-Storage/blob/master/tethysapp/storage_capacity/public/images/Results.png">

####Main Files

The main files associated with this application include raster data (surface elevation, flow direction, and flow accumulation), a map service with the main streams in the Dominican Republic, and the geoprocessing service task to calculate storage capacity and the flow-duration curve values. 

####Code Structure

The basic structure of the Python script that calculates storage capacity is shown in the flowchart below, Figure 5. The yellow filled circles represent input features necessary for the geoprocessing task to run. The green filled shapes represent processing steps. The blue squares represent intermediate features, some of which are also saved as outputs (e.g. the watershed and reservoir features).

<img border=0 width=800 height=461 id="Picture 2"
src="https://github.com/elisenavidad/FDC-Storage/blob/master/tethysapp/storage_capacity/public/images/codestructure.JPG">

Figure 5. Python script structure diagram. This is a simplified diagram. The actual script uses more steps that the ones shown here.

The basic structure of the app is shown below in Figure 6.  The blue filled circles represent the user input necessary for the analysis.  The red-filled shape represent the processing tasks.  The green squares represent intermediate values generated by the geoprocessing service outlined above.  This data is then represented on two separate pages. 

<img border=0 width=800 height=461 id="Picture 6"
src="https://github.com/elisenavidad/FDC-Storage/blob/master/tethysapp/storage_capacity/public/images/model.jpg">

####Key Functions

The following were some of the most important functions used with the ArcGIS API for JavaScript.

<table>
 <tr>
  <td><p><strong>Function Name</strong></p></td>
  <td><p><strong>Comments</strong></p></td>
 </tr>
 <tr>
  <td><p>drawPoint</p></td>
  <td><p>End user places point on map</p></td>
 </tr>
 <tr>
  <td><p>submitJob</p></td>
  <td><p>Application runs the geoprocessing task</p></td>
 </tr>
 <tr>
  <td><p>completeCallback</p></td>
  <td><p>Calls functions to draw results on successfull job requeset</span></p></td>
 </tr>
 <tr>
  <td><p>drawWatershed</p></td>
  <td><p>Outlines resulting watershed polygon on map</span></p></td>
 </tr>
 <tr>
  <td><p>drawReservoir</p></td>
  <td><p>Outlines resulting reservoir polygon on map</span></p></td>
 </tr>
 <tr>
  <td><p>getVolume</p></td>
  <td><p>Makes request to retrieve volume data and calls function to display resulting reservoir volume</p></td>
 </tr>
 <tr>
 <td><p>completeCallback</p></td>
 <td><p>Makes request to retrieve flow duration data from the geoserver, and posts the data to the controller to create the Flow-Duration curve.</p></td>
 </tr>
</table>
