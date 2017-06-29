# -*- encoding: utf-8 -*-
# 脚本功能： 用栅格城市数据计算缓冲区覆盖的区域的城市面积
#
import arcpy
import arcpy.sa

arcpy.CheckOutExtension("Spatial")


#data_file = u'E:/Data/city_extraction/1km_rar/1990/GHS_BUILT_LDS1990_GLOBE_R2016A_54009_1k_v1_0.tif'
#data_file = u'E:/Data/city_extraction/1km_rar/2000/GHS_BUILT_LDS2000_GLOBE_R2016A_54009_1k_v1_0.tif'
#data_file = u'E:/Data/city_extraction/1km_rar/2014/GHS_BUILT_LDS2014_GLOBE_R2016A_54009_1k_v1_0.tif'

config = {
    'buffer_file': u'E:/Data/city_extraction/validation/city_population_buffer.shp', # 缓冲区文件路径
    'data_file': u'E:/Data/city_extraction/1km_rar/2014/GHS_BUILT_LDS2014_GLOBE_R2016A_54009_1k_v1_0.tif', # 城市数据文件路径
    'area_field': '2014_area' # 面积字段，这个字段需要在shapefile文件中已经存在
}


if __name__ == '__main__':

    ghs_raster = arcpy.Raster(config['data_file'])
    with arcpy.UpdateCursor(config['buffer_file']) as cursor:
        for row in cursor:
            mask = row.getValue('Shape')
            fid = row.getValue('FID')
            city_raster = arcpy.sa.ExtractByMask(ghs_raster, mask)
            city_arr = arcpy.RasterToNumPyArray(city_raster)
            city_arr = city_arr[city_arr>0]
            actual_area = city_arr.sum() * 1
            row.setValue(config['area_field'], actual_area)        
            cursor.updateRow(row)       
            print(fid, actual_area)
    





