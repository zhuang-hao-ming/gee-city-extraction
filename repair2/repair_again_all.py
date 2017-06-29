# -*- encoding: utf-8 -*-
#
# 功能：
# 对repair1.py中无法用相邻年份替换的栅格
# 使用cell_statistic.py产生的合成指数文件，在城市的缓冲区内重新进行阈值分割，然后将结果镶嵌回去
#

import csv
import arcpy
import arcpy.sa
import os
import sys
import uuid
from multiprocessing import Process
import time


arcpy.CheckOutExtension("Spatial")


config = {
    'no_data_val': -9999,
    'buffer_file': u'E:/Data/city_extraction/validation/buffer_to_grid10.shp',# 10度格网和城市连接后的shp
    'data_dir': u'E:/test/4_24/urbanSta/',
    'base_name': u'NUACI_',
    1990: {
        'outliar_file': u'E:/test/4_24/error_log/cannot_repair_file_1990.txt', 
        
        'area_field': 'F1990_area',
        'mosaic_data_dir': u'F:/urban_result/urban1990/',
        'mosaic_base_name': u'URBAN_1990_',
        'log_file': u'./error_log/actual_vs_target1990.txt',
    },
    1995: {
        'outliar_file': u'E:/test/4_24/error_log/cannot_repair_file_1995.txt', 
        
        'area_field': 'F1995_area',
        'mosaic_data_dir': u'F:/urban_result/urban1995/',
        'mosaic_base_name': u'URBAN_1995_',
        'log_file': u'./error_log/actual_vs_target1995.txt',
    },
    2000: {
        'outliar_file': u'E:/test/4_24/error_log/cannot_repair_file_2000.txt', 
        
        'area_field': 'F2000_area',
        'mosaic_data_dir': u'F:/urban_result/urban2000/',
        'mosaic_base_name': u'URBAN_2000_',
        'log_file': u'./error_log/actual_vs_target2000.txt',
    },
    2005: {
        'outliar_file': u'E:/test/4_24/error_log/cannot_repair_file_2005.txt', 
        
        'area_field': 'F2005_area',
        'mosaic_data_dir': u'F:/urban_result/urban2005/',
        'mosaic_base_name': u'URBAN_2005_',
        'log_file': u'./error_log/actual_vs_target2005.txt',
    },
    2010: {
        'outliar_file': u'E:/test/4_24/error_log/cannot_repair_file_2010.txt', 
        
        'area_field': 'F2010_area',
        'mosaic_data_dir': u'F:/urban_result/urban2010/',
        'mosaic_base_name': u'URBAN_2010_',
        'log_file': u'./error_log/actual_vs_target2010.txt',
    },
    
    
    
    'log_file': u'./error_log/actual_vs_target.txt',
    
    
    
    
    
    'begin_id': 0,
    'end_id': 223
}



fo = open(config['log_file'], "w")





# 读入异常的城市id
def read_csv(outliar_file):
    ret = []
    with open(outliar_file, 'r') as csvfile:    
        spam_readder = csv.reader(csvfile, delimiter='\t')
        for row in spam_readder:   
            ret.append(row[0])
    return ret

    

    
def repair(raster_dict, ghs_area, city_code, year):
    '''阈值计算和mosaic
    '''
    year_config = config[year]

    threshold_max = 10000
    threshold_min = 1000
    threshold_step = 100
    actual_area = 0
    target_area = float(ghs_area)

    print('******* city_code', city_code, 'begin find threshold')
    

    threshold_value = threshold_max
    array_list = [raster_dict[key]['array'] for key in raster_dict.keys()]
    array_list_b = [array > threshold_value for array in array_list]
    while (actual_area < target_area) and (threshold_value >= threshold_min):
        array_list_b = [array > threshold_value for array in array_list]
        sum_list = [array.sum() * 0.0009 for array in array_list_b]
        actual_area = sum(sum_list)
        threshold_value -= threshold_step

    print('city_code', city_code, 'find threshold', threshold_value, 'target_area', target_area, 'actual_area', actual_area,'threshold_value', threshold_value)

    if actual_area < target_area * 0.5:
        print('-------outliar', 'city_code', city_code, '-------------')
        fo.write('\t'.join([str(city_code), str(actual_area), str(target_area), str(threshold_value), str(year)]) + '\n')

    for key in raster_dict.keys():
        raster = raster_dict[key]['raster'] 
        lower_left = arcpy.Point(raster.extent.XMin,raster.extent.YMin)
        cell_size = raster.meanCellWidth
        dsc = arcpy.Describe(raster)
        sr = dsc.SpatialReference
        no_data_value = raster.noDataValue

        array = raster_dict[key]['array']
        array_b = array > threshold_value
        new_raster = arcpy.NumPyArrayToRaster(array_b.astype(array.dtype), lower_left, cell_size, cell_size, value_to_nodata=config['no_data_val'])
        arcpy.DefineProjection_management(new_raster, sr)

        #mosaic
        mosaic_target_path = year_config['mosaic_data_dir'] + year_config['mosaic_base_name'] + str(key) + '.tif'
        arcpy.Mosaic_management(new_raster, mosaic_target_path, "LAST", "FIRST", "", "", "", "", "")
        print('mosaic', mosaic_target_path, 'ok')

        # save_path = year_config['mosaic_base_name'] + str(key) + '_' + uuid.uuid1().hex + '.tif'
        # new_raster.save('./raster/' + save_path)
        # print(save_path)
        




def repair_city(fid, year):    
    '''修补一个城市
    '''
    ghs_area = 0        
    raster_dict = {}
    city_code = None

    year_config = config[year]

    for row in arcpy.SearchCursor(config['buffer_file'], '"TARGET_FID" = {0}'.format(fid)):
        
        mask = row.getValue('Shape')
        ghs_area = float(row.getValue(year_config['area_field']))

        
        city_code = str(row.getValue('City_Code'))
        

        grid_code = row.getValue('code')

        if int(grid_code) < config['begin_id'] or int(grid_code) > config['end_id']:
            return
        
        grid_code_file = config['data_dir'] + config['base_name'] + grid_code + '.tif'
        grid_raster = arcpy.Raster(grid_code_file)
        city_raster = arcpy.sa.ExtractByMask(grid_raster, mask)
        raster_dict[grid_code] = {
            'raster': city_raster,
            'array': arcpy.RasterToNumPyArray(city_raster, nodata_to_value=config['no_data_val']) 
        }
        
    if len(raster_dict.keys()) > 0:
        repair(raster_dict, ghs_area, city_code, year) 
        city_code = None 


def main(rets, year):

    #——————
    newTempDir = u"./tmp/tmp" + time.strftime('%Y%m%d%H%M%S')
    os.mkdir(newTempDir)
    os.environ["TEMP"] = newTempDir
    os.environ["TMP"] = newTempDir
    arcpy.env.workspace = newTempDir
    #——————

    cnt = 0
    print rets, len(rets)
    for fid in rets:
        cnt += 1
        repair_city(fid, year)
        print('current process: {0}/{1}'.format(cnt, len(rets)))



if __name__ == '__main__':

    for year in range(1990, 2011, 5):

        ret = read_csv(config[year]['outliar_file']) # 读取到每个年份的异常文件
        cnt = 0
        all_cnt = len(ret)
        print('{0} has {1} to repair'.format(year, all_cnt))
        for idx in range(0, all_cnt, 10): # 每个进程只处理10个项，然后重建进程，避免长时间运行导致资源泄漏
            print('rebuild process')
            p = Process(target=main, args=(ret[idx:idx+10],year))
            p.start()
            p.join()
            
            cnt += len(ret[idx:idx+10])
            print(ret[idx:idx+10], 'finish')
            print(str(cnt) + '/' + str(all_cnt))
        
                
    fo.close()

    print('repair finish')