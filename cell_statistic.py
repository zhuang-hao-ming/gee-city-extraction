# -*- encoding: utf-8 -*-
# author: haoming
# 脚本功能： 对不同年份的指数数据进行最大值叠加来尽量减少指数数据缺失
#

import arcpy
import arcpy.sa


arcpy.env.workspace = u'E:/Data/city_extraction/python'
arcpy.CheckOutExtension('Spatial')

#
# 规定输入和输出的数据文件的路径为：
# {data_dir}{name_prefix}{id}.tif
#
config = {
    1990: {
        'data_dir': u'E:/Data/city_extraction/1990/',
        'name_prefix': 'NUACI1990_'
    },
    1995: {
        'data_dir': u'E:/Data/city_extraction/1995/',
        'name_prefix': 'NUACI1995_'
    },
    2000: {
        'data_dir': u'E:/Data/city_extraction/2000/',
        'name_prefix': 'NUACI2000_'
    },
    2005: {
        'data_dir': u'E:/Data/city_extraction/2005/',
        'name_prefix': 'NUACI2005_'
    },
    2010: {
        'data_dir': u'E:/Data/city_extraction/2010/',
        'name_prefix': 'NUACI2010_'
    },
    'output': {
        'data_dir': u'E:/Data/city_extraction/cell_statistics/',
        'name_prefix': 'NUACI_'        
    },
    'begin_id': 90,
    'end_id': 134    
}

if __name__ == '__main__':
    for id in range(config['begin_id'], config['end_id']+1):
        raster_list = []
        for year in range(1990, 2010+1, 5):
            file_path = config[year]['data_dir'] + config[year]['name_prefix'] + str(id) + '.tif'
            if arcpy.Exists(file_path):
               raster_list.append(file_path)
        output_raster = arcpy.sa.CellStatistics(raster_list, 'MAXIMUM') 
        output_raster.save(config['output']['data_dir'] + config['output']['name_prefix'] + str(id) + '.tif')
        print(id, raster_list, 'finish')
            

