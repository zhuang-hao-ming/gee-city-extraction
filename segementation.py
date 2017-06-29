# -*- encoding: utf-8 -*-
# 
# 功能： 和get_urban.py类似，完成6km缓冲区的阈值分割，并保存结果



import csv
import arcpy
import arcpy.sa

arcpy.CheckOutExtension("Spatial")

arcpy.env.workspace = u'E:/Data/city_extraction/new_validation/work'



config = {
    'buffer_file': u'./shp/out_shp_buffer_all.shp',# link_csv_to_shp.py输出的shp文件
    'data_dir': u'E:/test/4_24/urbanSta/', # 规定输入指数文件路径 '{data_dir}{base_name}{10_grid_code}.tif'
    'base_name': u'NUACI_',
    'no_data_value': -9999,
    'log_file': './log_file0628',
    'threshold_max': 10000,
    'threshold_min': 1000,
    'threshold_step': 100,
    'area_factor': 1.5,
}
fo = open(config['log_file'], "w")

    

    
def repair(buffer_raster, ghs_area, unit_fid, year, grid_code):
    '''阈值计算和mosaic
    '''
    threshold_max = config['threshold_max']
    threshold_min = config['threshold_min']
    threshold_step = config['threshold_step']
    
    target_area = float(ghs_area) * config['area_factor']
    actual_area = 0

    print('******* Unit_FID {0} year {1} begin find threshold'.format(unit_fid, year))
    

    threshold_value = threshold_max
    arr = arcpy.RasterToNumPyArray(buffer_raster, nodata_to_value=config['no_data_value'])
    
    arr_bi = arr > threshold_value
    while (actual_area < target_area) and (threshold_value >= threshold_min):
        arr_bi = arr > threshold_value
        actual_area = arr_bi.sum() * 0.0009
        threshold_value -= threshold_step

    print('Unit_FID:{0},threshold:{1},target_area:{2},actual_area:{3},year:{4},grid_code:{5}'.format(unit_fid, threshold_value, target_area, actual_area, year,grid_code))
    fo.write('Unit_FID:{0},threshold:{1},target_area:{2},actual_area:{3},year:{4},grid_code:{5}'.format(unit_fid, threshold_value, target_area, actual_area, year, grid_code) + '\n')


    
    
    lower_left = arcpy.Point(buffer_raster.extent.XMin,buffer_raster.extent.YMin)
    cell_size = buffer_raster.meanCellWidth
    dsc = arcpy.Describe(buffer_raster)
    sr = dsc.SpatialReference
    #no_data_value = buffer_raster.noDataValue

    
    
    new_raster = arcpy.NumPyArrayToRaster(arr_bi.astype(arr.dtype), lower_left, cell_size, cell_size, config[''])
    arcpy.DefineProjection_management(new_raster, sr)

    #mosaic
    #mosaic_target_path = config['mosaic_data_dir'] + config['mosaic_base_name'] + str(key) + '.tif'
    #arcpy.Mosaic_management(new_raster, mosaic_target_path, "MAXIMUM", "FIRST", "", "", "", "", "")
    #print('mosaic', mosaic_target_path, 'ok')

    new_raster.save('./{0}/{1}.tif'.format(year, unit_fid))
        




def main():    
    '''修补一个城市


    '''
    cnt = 0

    for row in arcpy.SearchCursor(config['buffer_file']):
        cnt += 1
        print('{} row is processing'.format(cnt))
        mask = row.getValue('Shape')
        year_list = (row.getValue('year')).split(',')# 异常年份
        
        for year in year_list:
            ghs_area = float(row.getValue('area_'+year))# 欧空局面积                    
            grid_code = int(row.getValue('UrbanGrid'))# 10度格网号
            unit_fid = int(row.getValue('UnitFID'))# id
            
        
            grid_code_file = '{0}{1}{2}.tif'.format(config['data_dir'], config['base_name'], str(grid_code))# 指数文件
            grid_raster = arcpy.Raster(grid_code_file)
            buffer_raster = arcpy.sa.ExtractByMask(grid_raster, mask)
                    
            repair(buffer_raster, ghs_area, unit_fid, year, grid_code) 
    

if __name__ == '__main__':    
    main()
    fo.close()                