

# EDAC Sinkhole Toolbox


This tool is designed to provide the user with an ability to do a preliminary reconnaissance for possible sinkholes.  This tool allows for either LiDAR LAS or DEM tiles to be used as input.  Also the user can define the minimum and maximum size of sinkholes being searched.  In addition, the user can supply a mask shapefile.  After creating a DEM mosaic in a user-defined geodatabase, the tool applies an image segmentation method to derive the output sinkhole polygons.

## Requirements
This tool requries the Spatial Analyst extension

## Purpose

This tool does a preliminary search for possible sinkholes given LiDAR LAS files and/or DEM images.


**Credits**
The development of this tool was funded through a contract awarded by the Transportation Consortium of South-Central States (Tran-SET) - a consortium supported by USDoT.

**Use Limitations**
There are no use restrictions.




## Tools

**DEM Creator**

***Summary***
If there are not laready existing DEM/DSM tiles, this tool will create them from the LIDAR LAS tiles.

**Sinkhole Extractor**

***Summary***
The Sinhole Extractor tool uses DEM tiles to look for and extract potential sinkholes. The user can define the minimum and maximum size of sinkholes being searched. In addition, the user can supply a mask shapefile. After creating a DEM mosaic in a user-defined geodatabase, the tool applies an image segmentation method to derive the output sinkhole polygons.
