import arcpy

# read in mxd file
mxd=arcpy.mapping.MapDocument(r"E:\test\4_24\data\urban2005.mxd")

# read in all rasters in the mxd which have names starting with "test"
rasters=arcpy.mapping.ListLayers(mxd,"URBAN_*") 

# apply the symbology lyr file to the rasters
for r in rasters:
    print(r,'ok')
    arcpy.ApplySymbologyFromLayer_management(r, r"E:\test\4_24\data\URBAN_2005_0.tif.lyr")