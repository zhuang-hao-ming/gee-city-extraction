# -*- encoding: utf-8 -*-
#
# 对指数数据进行阈值分割
#





import arcpy
from new_process import Process
from arcpy import env
from arcpy.sa import *
import os
import time
import sys

arcpy.CheckOutExtension("Spatial")



# 参数
config = {
    
    'fc': u'E:/tasks/gee0903/Targets1980_2015/Main_urban4_sj.shp',# 2度带shp文件, 记录2度网格和10度网格的对应关系和2度网格的目标城市数目
    'in_folder_path': u'F:/data/nuaci_1980',# 输入10度栅格路径, 规定输入栅格的路径是 {in_folder_path}/{input_prefix}{10_grid_code}.tif
    'out_folder_path': u'F:/data/output_1980',# 输出10度栅格路径, 规定输出栅格的路径是 {out_folder_path}/{output_prefix}{10_grid_code}.tif
    'target_count_field': 'Target1980',# 存储目标城市数量的字段
    'input_prefix': 'NUACI1980_', # 输入10度栅格名字前缀
    'output_prefix': 'URBAN_1980_', # 输出10度栅格名字前缀
    'threshold_max': 10000,
    'threshold_min': 3000,
    'threshold_step': 100,
    ' target_count_field': 'Target1980',
    'begin_fid': 0, #包含90
    'end_fid': 89, #包含134
    'log_file': './get_urban_log' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()) +'.txt',
}






def long_time_task(FID):
    '''
    处理一个FID，也就是一个2度网格的城市阈值计算，提取，和镶嵌。
    '''

    # arcpy的临时输出文件
    # --- 这段代码保证，不同的arcpy进程使用不同的临时空间，在多进程的环境下避免一些错误
    newTempDir = u"./tmp/tmp" + time.strftime('%Y%m%d%H%M%S') + str(FID)
    os.makedirs(newTempDir)
    os.environ["TEMP"] = newTempDir
    os.environ["TMP"] = newTempDir
    # ---

    for row in arcpy.SearchCursor(config['fc'], '"FID" = {0}'.format(FID)):
        begin_time = time.time()

        grid_code = int(row.getValue("grid_id"))# 10度网格号
        mask = row.getValue("Shape")# 2度网格shape
        row_code = row.getValue("code")# 2度网格号
        
        print '**** PID: ' + str(os.getpid()) + ' FID: ' + str(FID) + " grid_code: " + str(grid_code)

        target_area = row.getValue(config['target_count_field'])# 目标城市数目字段
        threshold_max = config['threshold_max']
        threshold_min = config['threshold_min']
        threshold_step = config['threshold_step']

        nuaci_path = '{0}/{1}{2}.tif'.format(config['in_folder_path'], config['input_prefix'], grid_code)

        # if not arcpy.Exists(nuaci_path):
        #     # arcpy.AddError(nuaci_path + ' not found ')
            
        print '####input', nuaci_path


        in_raster = Raster(nuaci_path)        
        in_raster_mask = ExtractByMask(in_raster, mask)
        del in_raster

        lower_left = arcpy.Point(in_raster_mask.extent.XMin,in_raster_mask.extent.YMin)
        cell_size = in_raster_mask.meanCellWidth
        dsc = arcpy.Describe(in_raster_mask)
        sr = dsc.SpatialReference
        no_data_value = in_raster_mask.noDataValue

        in_raster_arr = arcpy.RasterToNumPyArray(in_raster_mask,nodata_to_value=no_data_value)            
        del in_raster_mask

        actual_area = 0
        threshold_value = threshold_max
        in_raster_arr_bi = in_raster_arr > threshold_value

        while (actual_area < target_area) and (threshold_value >= threshold_min):
            in_raster_arr_bi = in_raster_arr > threshold_value
            actual_area = in_raster_arr_bi.sum() * 0.0009
            threshold_value -= threshold_step

        print('------------final area = ' + str(actual_area) + '---------------' + str(row_code))
        print('final threshold = ' + str(min([threshold_max,threshold_value + threshold_step])))

        in_raster_arr_dtype = in_raster_arr.dtype
        del in_raster_arr
        in_raster_arr_bi = in_raster_arr_bi.astype(in_raster_arr_dtype)    
        new_raster = arcpy.NumPyArrayToRaster(in_raster_arr_bi,lower_left, cell_size, cell_size, no_data_value)
        del in_raster_arr_bi


        arcpy.DefineProjection_management(new_raster, sr)                
        out_raster_path = '{0}/{1}{2}.tif'.format(config['out_folder_path'], config['output_prefix'], grid_code)
        arcpy.Mosaic_management(new_raster, out_raster_path, "LAST", "FIRST", "", "", "", "", "")
        del new_raster
        print 'Task %d - %d - %d runs %0.2f seconds.' % (os.getpid(), FID, grid_code,(time.time() - begin_time))

if __name__ == '__main__':

    fo = open(config['log_file'], 'w')# 错误记录文件
    
    cursor = arcpy.SearchCursor(config['fc'])
    for row in cursor:
        
        grid_code = int(row.getValue("grid_id")) # 10度带号
        FID = int(row.getValue('FID'))
        row_code = row.getValue("code") # 2度带号

        if grid_code < config['begin_fid'] or grid_code > config['end_fid']:                
            continue                                        
        print str(grid_code) + '-' + str(FID)

        #—————— 每次处理完成一个2度栅格就重新启动一个进程，避免进程长时间运行导致的内存错误和崩溃问题
        p = Process(target=long_time_task, args=(FID,))
        print 'Process will start.'
        p.start()
        p.join()
        if p.exception:
            error, traceback = p.exception
            print traceback
            fo.write('grid_code' + '---' + str(grid_code) + '---FID---' + str(FID) + '---row_code---' + row_code + '\n')#记录出错的FID
        #——————
    fo.close()