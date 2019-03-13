import arcpy
import os
import datetime
from arcpy import env
from time import sleep
from arcpy.sa import *
import glob
import arceditor

arcpy.env.overwriteOutput = True
timestamp = datetime.datetime.now()


class Toolbox(object):
    def __init__(self):
        self.label = "Sinkhole Toolbox"
        self.alias = "EDAC Sinkhole Toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [Sinkhole_Extractor,DEMCreator]

class DEMCreator(object):
    def __init__(self):
        self.label = "DEM Creator"
        self.description = "This tool creates DEM tiles from the LAS tiles which can be used for the Sinkhole Extractor tool if bare earth DEM tiles are not available."
        self.canRunInBackground = False
    def getParameterInfo(self):
        lasdir = arcpy.Parameter(displayName="LAS Input Directory", name="LAS Input Directory", datatype="DEFolder", parameterType="Required", direction="Input")
        outputraster = arcpy.Parameter(displayName="Output Raster Directory", name="Output Raster Directory", datatype="DEFile", parameterType="Required", direction="Output")
        crs = arcpy.Parameter(displayName="Output Coordinate System", name="Output Coordinate System", datatype="GPCoordinateSystem", parameterType="Required", direction="Input")
        binningcell = arcpy.Parameter(displayName="Cell Assignment Type",name="Cell Assignment Type",datatype="GPString",parameterType="Optional",direction="Input")
        binningcell.value = "MINIMUM"
        binningcell.filter.type = "ValueList"
        binningcell.filter.list = ["AVERAGE","MINIMUM","MAXIMUM","IDW","NEAREST"]
        binningvoid = arcpy.Parameter(displayName="Void Fill Method",name="Void Fill Method",datatype="GPString",parameterType="Optional",direction="Input")
        binningvoid.value = "LINEAR"
        binningvoid.filter.type = "ValueList"
        binningvoid.filter.list = ["NONE","SIMPLE","LINEAR","NATURAL_NEIGHBOR"]
        outputdatatype = arcpy.Parameter(displayName="Output Data Type",name="Output Data Type",datatype="GPString",parameterType="Optional",direction="Input")
        outputdatatype.value = "FLOAT"
        outputdatatype.filter.type = "ValueList"
        outputdatatype.filter.list = ["FLOAT","INT"]
        cell_size = arcpy.Parameter(displayName="Cell Size", name="Cell Size", datatype="GPDouble",parameterType="Required", direction="Input" )
        cell_size.value = 1
        z_factor = arcpy.Parameter(displayName="Z Factor", name="Z Factor", datatype="GPDouble",parameterType="Required", direction="Input" )
        z_factor.value = 1
        parameters = [lasdir,outputraster,crs,binningcell,binningvoid,outputdatatype,cell_size,z_factor]
        return parameters
    def isLicensed(self):  # optional
        return True

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        lasdir = parameters[0].valueAsText
        outputraster = parameters[1].valueAsText
        crs = parameters[2].valueAsText
        return_values = "Last Return"
        binningcell=parameters[3].valueAsText
        binningvoid=parameters[4].valueAsText
        outputdatatype=parameters[5].valueAsText
        cell_size=parameters[6].valueAsText
        z_factor=parameters[7].valueAsText
      
        class_code="2"
        
    #define output paths
        temp=os.environ.get("TEMP")
        lasd=os.path.join(temp,"tempLASD.lasd")
        lasd2=os.path.join(temp,"tempLASD2.lasd")

    # Execute CreateLasDataset
        arcpy.AddMessage("Execute Create Las Dataset")
        arcpy.management.CreateLasDataset(lasdir,lasd,spatial_reference=crs)
        

    # Execute Make LAS Dataset Layer
        arcpy.AddMessage("Make LAS Dataset Layer")
        if class_code is not None and return_values is not None:
            arcpy.MakeLasDatasetLayer_management(lasd,lasd2,class_code=class_code,return_values=return_values)
        elif class_code is not None:
            arcpy.MakeLasDatasetLayer_management(lasd,lasd2,class_code=class_code)
        elif return_values is not None:
            arcpy.MakeLasDatasetLayer_management(lasd,lasd2,return_values=return_values)
        else:
            arcpy.MakeLasDatasetLayer_management(lasd,lasd2)


    # Execute Las Dataset To Raster
        arcpy.AddMessage("Execute Las Dataset To Raster")
        arcpy.LasDatasetToRaster_conversion (lasd2, outputraster,"ELEVATION", "BINNING "+binningcell+" "+binningvoid , outputdatatype, "CELLSIZE", cell_size, z_factor)







class Sinkhole_Extractor(object):
    def __init__(self):
        self.label = "Sinkhole Extractor"
        self.description = "This tool extracts sinkholes"
        self.canRunInBackground = False
    def getParameterInfo(self):
     # Input parameters
        outputdir = arcpy.Parameter(displayName="Output Directory", name="Output Directory", datatype="DEFolder", parameterType="Required", direction="Input")
        demdir = arcpy.Parameter(displayName="DEM Input Directory", name="DEM Input Directory", datatype="DEFolder", parameterType="Required", direction="Input")
        crs = arcpy.Parameter(displayName="Output Coordinate System", name="Output Coordinate System", datatype="GPCoordinateSystem", parameterType="Required", direction="Input")
        mask = arcpy.Parameter(displayName="Extract Mask", name="Extract Mask", datatype="DEFeatureClass", parameterType="Optional", direction="Input")
        proc_bit_depth = arcpy.Parameter(displayName="Processing Bit Depth",name="Processing Bit Depth",datatype="GPString",parameterType="Optional",direction="Input")
        proc_bit_depth.value = "32_BIT_SIGNED"
        proc_bit_depth.filter.type = "ValueList"
        proc_bit_depth.filter.list = ["32_BIT_SIGNED","32_BIT_FLOAT","64_BIT"]
        spectral_detail = arcpy.Parameter(displayName="Spectral Detail", name="Spectral Detail", datatype="GPDouble", parameterType="Required", direction="Input")
        spectral_detail.value = 15.5
        spatial_detail = arcpy.Parameter(displayName="Spatial Detail", name="Spatial Detail", datatype="GPLong", parameterType="Required", direction="Input")
        spatial_detail.value = 15
        min_segment_size = arcpy.Parameter(displayName="Min Segment Size", name="Min Segment Size", datatype="GPLong", parameterType="Required", direction="Input")
        min_segment_size.value = 20
        shapeareaMin = arcpy.Parameter(displayName="Minimum Area (in map distance units squared)", name="Minimum Area", datatype="GPLong", parameterType="Required", direction="Input")
        shapeareaMin.value=100
        shapeareaMax = arcpy.Parameter(displayName="Maximum Area (in map distance units squared)", name="Maximum Area", datatype="GPLong", parameterType="Required", direction="Input")
        shapeareaMax.value=1000000
        parameters = [outputdir, demdir, crs, mask, proc_bit_depth,spectral_detail, spatial_detail, min_segment_size, shapeareaMin,shapeareaMax]
        return parameters

    def isLicensed(self):  # optional
        return True

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        arcpy.SetProgressor("default", "Working...", 0, 2, 1)
        outputdir = parameters[0].valueAsText
        dem_tiles = parameters[1].valueAsText
        crs = parameters[2].valueAsText
        mask = parameters[3].valueAsText
        proc_bit_depth = parameters[4].valueAsText
        spectral_detail = parameters[5].valueAsText
        spatial_detail = parameters[6].valueAsText
        min_segment_size = parameters[7].valueAsText
        shapeareaMin = parameters[8].valueAsText
        shapeareaMax = parameters[9].valueAsText


# Local variables:
        sinkhole_gdb = os.path.join(outputdir, "Sinkhole.gdb")
        Mosaic_Dataset = os.path.join(outputdir, "Sinkhole.gdb", "dem_mosaic")
        Mosaic_Dataset_Final = os.path.join(outputdir, "Sinkhole.gdb", "dem_mosaic_final")
        sinkholeDissolve = os.path.join(outputdir, "Sinkhole.gdb", "sinkholeDissolve")
        Sinkhole_polygons = os.path.join(outputdir, "Sinkhole.gdb", "Sinkhole_polygons")
        dem_fill_img = os.path.join(outputdir, "dem_fill.img")
        dem_diff_img = os.path.join(outputdir, "dem_diff.img")
        dem_diff2_img = os.path.join(outputdir, "dem_diff2.img")
        dem_diff2mask_img = os.path.join(outputdir, "dem_diff2mask.img")
        dem_diff2_is_img = os.path.join(outputdir, "dem_diff2_is.img")
        sinkhole_polys_shp = os.path.join(outputdir, "sinkhole_polys.shp")
        SegmentMeanShiftInput = None
# Process: Create output file geodatabase
        arcpy.AddMessage("Creating file GDB")
        arcpy.CreateFileGDB_management(outputdir, "Sinkhole.gdb")
        productname=arcpy.GetInstallInfo()['ProductName']
        arcpy.AddMessage(productname)
# Process: Create Mosaic Dataset
        arcpy.AddMessage("Creating Mosaic Dataset")
        arcpy.CreateMosaicDataset_management(sinkhole_gdb, "dem_mosaic", crs, "", proc_bit_depth, "NONE", "")

# Process: Add Rasters To Mosaic Dataset
        arcpy.AddMessage("Adding files from "+str(dem_tiles)+" to mosaic dataset.")
        arcpy.AddRastersToMosaicDataset_management(Mosaic_Dataset, "Raster Dataset", dem_tiles)
# Process: Set Null 
        arcpy.AddMessage("Setting any value less than 0 to Null for Mosaic Dataset.")
        OutSetNull=SetNull(Mosaic_Dataset, Mosaic_Dataset, "VALUE <= 0")
        OutSetNull.save(Mosaic_Dataset_Final)
# Process: Fill
        arcpy.AddMessage("Running fill on mosaic dataset.")
        outFill=Fill(Mosaic_Dataset_Final, "")
        outFill.save(dem_fill_img)

# Process: Raster Calculator
        arcpy.AddMessage("Subtracting mosaic from mosaic fill.")
        arcpy.Minus_3d(dem_fill_img, Mosaic_Dataset_Final, dem_diff_img)
# Process: Set Null 
        arcpy.AddMessage("Setting any value less than 0 to Null for resulting raster values.")
        OutSetNull=SetNull(dem_diff_img, dem_diff_img, "VALUE <= 0")
        OutSetNull.save(dem_diff2_img)
# Process: Extract by Mask if one is given
        if mask is not None:
                arcpy.AddMessage("Mask is provided, so extracting data by mask.")
                ExtractBy=ExtractByMask(dem_diff2_img, mask)
                ExtractBy.save(dem_diff2mask_img)
                SegmentMeanShiftInput=dem_diff2mask_img
        else:
                arcpy.AddMessage("No mask provided by user.")
                SegmentMeanShiftInput=dem_diff2_img
# Process: Segment Mean Shift
        arcpy.AddMessage("Grouping adjacent pixels together that have similar spectral characteristics.")
        SegMeShOut=SegmentMeanShift(SegmentMeanShiftInput, spectral_detail, spatial_detail, min_segment_size)
        SegMeShOut.save(dem_diff2_is_img)
# Process: Raster to Polygon
        arcpy.AddMessage("Saving Raster to polygon.")
        arcpy.RasterToPolygon_conversion(dem_diff2_is_img, sinkhole_polys_shp, "NO_SIMPLIFY", "Value")

# Process: Write Polygon to sinkhole geodatabase
        arcpy.AddMessage("Writing Polygon to GDB.")
        arcpy.FeatureClassToGeodatabase_conversion(sinkhole_polys_shp, sinkhole_gdb)

# Process: Dissolve the polygons
        arcpy.AddMessage("Dissolving polygons.")
        arcpy.Dissolve_management(sinkhole_polys_shp, sinkholeDissolve, "", "", "SINGLE_PART", "")

# Process: Select tool to select and output all polygons GTE 100 sq meters(or value provided by user).
        arcpy.AddMessage("Selecting area greater than or equal to "+str(shapeareaMin)+" and less than or equal to "+ str(shapeareaMax) +" sq meters.")
        where="Shape_Area >= "+ shapeareaMin + " AND " + "Shape_Area <= "+ shapeareaMax
        arcpy.Select_analysis(sinkholeDissolve, Sinkhole_polygons, where)

# Process: Clean up extraneous files
        arcpy.AddMessage("Cleaning up extraneous files")
        arcpy.Delete_management(dem_fill_img)
        arcpy.Delete_management(dem_diff_img)
        arcpy.Delete_management(dem_diff2_img)
        arcpy.Delete_management(dem_diff2mask_img)
        arcpy.Delete_management(dem_diff2_is_img)
        arcpy.Delete_management(sinkhole_polys_shp)
        arcpy.Delete_management(os.path.join(outputdir, "Sinkhole.gdb", "sinkhole_polys"))
        arcpy.Delete_management(sinkholeDissolve)



#Message to ArcGISPro users.
        if productname=="ArcGISPro":
            arcpy.AddMessage("Will not display output in ArcGIS Pro.")
        

        elif productname=="Desktop":
            mxd = arcpy.mapping.MapDocument("CURRENT")
            arcpy.mapping.ListDataFrames(mxd)[0].name = "Sinkhole Output"
            addLayer = arcpy.mapping.Layer(Sinkhole_polygons)
            df = arcpy.mapping.ListDataFrames(mxd)[0]
            arcpy.mapping.AddLayer(df, addLayer, "BOTTOM")


