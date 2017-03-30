import arcpy
from arcpy.sa import *
from arcpy import env
import sys
import os

arcpy.CheckOutExtension("Spatial")
arcpy.CheckOutExtension("3D")

scriptPath = sys.path[0]
toolDataPath = os.path.join(scriptPath, 'ToolData')
# Environment Settings
arcpy.env.snapRaster = os.path.join(toolDataPath, 'demfill')
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference('NAD 1983 UTM ZONE 19N')
arcpy.env.workspace = os.path.join(scriptPath, 'Scratch\Scratch.gdb')
arcpy.env.scratchWorkspace = os.path.join(scriptPath, 'Scratch\Scratch.gdb')
arcpy.env.overwriteOutput = True

# Local variables
filled_dem = r'D:\Jackson\StorageCapacity\ToolData\demfill'
flow_direction = r'D:\Jackson\StorageCapacity\ToolData\flowdir'
flow_accumulation = r'D:\Jackson\StorageCapacity\ToolData\flowacc'
snap_distance = 500


# functions
def checkPourPoint(raster):
    try:
        max = arcpy.GetRasterProperties_management(raster, "MAXIMUM")
        if int(max.getOutput(0)) >= int(36569):
            return True
        else:
            return False
    except:
        return False


def getElev(raster):
    max = arcpy.GetRasterProperties_management(raster, "MAXIMUM")
    initElv = max.getOutput(0)
    return float(initElv)


# Script arguments
pour_point = arcpy.GetParameter(0)
height = arcpy.GetParameterAsText(1)
watershedFT = arcpy.GetParameterAsText(2)
reservoir = arcpy.GetParameterAsText(3)
volume = arcpy.GetParameterAsText(4)
results = arcpy.GetParameterAsText(5)
curve_number = arcpy.GetParameterAsText(6)


def Precip(watershed_poly):
    # Local variables
    precipchago = r'D:\Jackson\StorageCapacity\ToolData\precipchago'
    precip_raster = Raster(precipchago)
    prec_table = 'prec_table'
    prec_table_avg = 'prec_table_avg'

    if precipchago == '#' or not precipchago:
        precipchago = "precipchago"  # provide a default value if unspecified

    # Process
    arcpy.AddMessage("Extract precipitation values from raster to table")
    arcpy.ExtractValuesToTable_ga(watershed_poly, precip_raster, prec_table, "", "true")
    arcpy.AddField_management(watershed_poly, "Prec_ID", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED")
    arcpy.CalculateField_management(watershed_poly, "Prec_ID", 1, "PYTHON", "")
    arcpy.AddMessage("Determine Average precipitation across watershed")
    arcpy.Statistics_analysis(prec_table, prec_table_avg, "Value MEAN", "")
    arcpy.AddField_management(prec_table_avg, "Av_Prec", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED")
    arcpy.AddField_management(prec_table_avg, "ID")
    arcpy.CalculateField_management(prec_table_avg, "ID", 1, "PYTHON")
    arcpy.CalculateField_management(prec_table_avg, "Av_Prec", "!MEAN_Value!", "PYTHON", "")
    arcpy.JoinField_management(watershed_poly, "Prec_ID", prec_table_avg, "ID", "Av_Prec")


def Find_Slope(watershed_poly):
    # Local variables
    watershed_dem = 'watershed_dem'
    slope1 = 'slope1'
    slope_table = 'slope_table'
    slope_stats = 'slope_stats'

    # Extract slope raster by watershed polygon
    arcpy.AddMessage("clip DEM to watershed polygon")
    arcpy.gp.ExtractByMask_sa(filled_dem, watershed_poly, watershed_dem)
    arcpy.AddMessage("Calculate slope for watershed")
    arcpy.gp.Slope_sa(watershed_dem, slope1, "PERCENT_RISE", "1")
    arcpy.ExtractValuesToTable_ga(watershed_poly, slope1, slope_table)
    arcpy.AddMessage("Find average slope across the watershed")
    arcpy.Statistics_analysis(slope_table, slope_stats, "Value MEAN")
    arcpy.AddField_management(slope_stats, "Slope_Avg", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(slope_stats, "Slope_Avg", "!MEAN_Value!", "PYTHON", "")
    arcpy.AddMessage("Join field to polygon")
    arcpy.AddField_management(slope_stats, "Prec_ID")
    arcpy.CalculateField_management(slope_stats, "Prec_ID", 1, "PYTHON")
    arcpy.JoinField_management(watershed_poly, "Prec_ID", slope_stats, "OBJECTID", "Slope_Avg")


def CN(watershed_poly):
    curve_number = arcpy.GetParameterAsText(6)

    if curve_number == '#' or not curve_number:
        curve_number = 80  # provide default value if not specified

    arcpy.AddMessage("Assign curve number to watershed")
    arcpy.AddField_management(watershed_poly, "Curve_Number", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED")
    arcpy.CalculateField_management(watershed_poly, "Curve_Number", curve_number, "PYTHON")


def FDC_calc(watershed_poly):
    arcpy.AddMessage("Calculate watershed area in square kilometers")
    arcpy.AddField_management(watershed_poly, "Area_Sq_Km", "Double", "", "", "", "", "NULLABLE", "NON_REQUIRED",
                              "")
    data = arcpy.SearchCursor(watershed_poly)
    for row in data:
        Shape_Area = row.getValue("Shape_Area")
    arcpy.CalculateField_management(watershed_poly, "Area_Sq_Km", float(Shape_Area) / (1000 * 1000), "PYTHON", "")

    # Calculate FDC Values and populate list
    arcpy.AddMessage("Extract parameters from watershed")
    columns = "Area_Sq_Km; Av_Prec; Slope_Avg; Curve_Number"
    data = arcpy.SearchCursor(watershed_poly, "", "", columns)

    for row in data:
        area = row.getValue("Area_Sq_Km")
        precip = row.getValue("Av_Prec")
        slope = row.getValue("Slope_Avg")
        cn = row.getValue("Curve_Number")

        arcpy.AddMessage("Watershed area=" + str(area))
        arcpy.AddMessage("Watershed precipitation=" + str(precip))
        arcpy.AddMessage("Watershed slope=" + str(slope))
        arcpy.AddMessage("Watershed curve number=" + str(cn))

    def flowcalcs(percent, A, P, CN, S):
        if percent == 99:
            flow = 7.683 * 10 ** 2 * A ** .729 * P ** .916 * CN ** -3.826 * S ** .380
        elif percent == 95:
            flow = 2.785 * 10 ** 4 * A ** .695 * P ** .362 * CN ** -3.553 * S ** .473
        elif percent == 90:
            flow = 1.168 * 10 ** 4 * A ** .640 * P ** .292 * CN ** -3.118 * S ** .435
        elif percent == 85:
            flow = 1.088 * 10 ** 4 * A ** .636 * P ** .295 * CN ** -3.071 * S ** .435
        elif percent == 80:
            flow = 1.376 * 10 ** 4 * A ** .643 * P ** .319 * CN ** -3.15 * S ** .435
        elif percent == 75:
            flow = 2.065 * 10 ** 4 * A ** .659 * P ** .358 * CN ** -3.312 * S ** .444
        elif percent == 70:
            flow = 2.452 * 10 ** 4 * A ** .673 * P ** .397 * CN ** -3.413 * S ** .45
        elif percent == 60:
            flow = 2.386 * 10 ** 4 * A ** .699 * P ** .484 * CN ** -3.584 * S ** .464
        elif percent == 50:
            flow = 4.07 * 10 ** 4 * A ** .713 * P ** .551 * CN ** -3.758 * S ** .472
        elif percent == 40:
            flow = 2.734 * 10 ** 4 * A ** .666 * P ** .681 * CN ** -3.789 * S ** .432
        elif percent == 30:
            flow = 8.512 * 10 ** 4 * A ** .717 * P ** .611 * CN ** -3.954 * S ** .461
        elif percent == 20:
            flow = 3.221 * 10 ** 5 * A ** .74 * P ** .603 * CN ** -4.218 * S ** .484
        return flow

    with open(results, "wb") as f:
        f.write("Percent, Value\n")

        percent = [99, 95, 90, 85, 80, 75, 70, 60, 50, 40, 30, 20]
        for percentage in percent:
            flow = flowcalcs(percentage, area, precip, cn, slope)
            f.write(str(percentage) + "," + str(flow) + '\n')
            # flowlist.append(flow)
    arcpy.AddMessage(results)
    global flowlist


# Processsing
Snap_Point_output = SnapPourPoint(pour_point, flow_accumulation, snap_distance, "OBJECTID")

pourPointTest = Times(flow_accumulation, Snap_Point_output)
majorStreamCondition = checkPourPoint(pourPointTest)

if majorStreamCondition == True:
    Watershed_raster = Watershed(flow_direction, Snap_Point_output, "VALUE")
    arcpy.RasterToPolygon_conversion(Watershed_raster, watershedFT, "NO_SIMPLIFY", "VALUE")

    demCP = ExtractByMask(filled_dem, watershedFT)
    pointTest = Times(demCP, Snap_Point_output)

    initElev = getElev(pointTest)
    reservoirRS = Con(demCP <= float(initElev) + float(height), 1, "")
    arcpy.RasterToPolygon_conversion(reservoirRS, reservoir, "SIMPLIFY", "Value")

    reserElv = ExtractByMask(filled_dem, reservoir)
    arcpy.SurfaceVolume_3d(reserElv, volume, "BELOW", "", "1", "0")

    # call functions
    Precip(watershedFT)
    Find_Slope(watershedFT)
    CN(watershedFT)
    FDC_calc(watershedFT)

    # with open(results,'w') as text_file:
    #     text_file.write(str(flowlist))

else:
    with open(volume, "w") as text_file:
        text_file.write("Input point is not close enough to any major streams on record.\n")
