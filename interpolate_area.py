# -*- encoding: utf-8 -*-
#
# 使用1990，2000，2014年的面积插值出1995，2005，2010年的面积



import arcpy
import arcpy.sa
import numpy as np
arcpy.CheckOutExtension("Spatial")

buffer_file = u'E:/Data/city_extraction/validation/city_population_buffer.shp'





if __name__ == '__main__':
    
    cursor = arcpy.UpdateCursor(buffer_file)
    for row in cursor:
        
        fid = row.getValue('FID')
        
        area_1990 = float(row.getValue('1990_area')) 
        area_2000 = float(row.getValue('2000_area'))
        area_2014 = float(row.getValue('2014_area'))

        xp = [1990, 2000, 2014]
        yp = [area_1990, area_2000, area_2014]

        new_area = np.interp([1995, 2005, 2010], xp, yp)
        
        
        row.setValue('1995_area', float(new_area[0]))
        row.setValue('2005_area', float(new_area[1]))
        row.setValue('2010_area', float(new_area[2]))

        cursor.updateRow(row)       
        
        print(fid, new_area)
    del cursor





