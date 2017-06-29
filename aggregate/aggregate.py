# -*- encoding: utf-8 -*-
# author: haoming
# 功能：
# 将30米的城市数据aggregate到990米


import arcpy
import os.path
import os
import multiprocessing
config = {
    1990: {                
        'data_dir': u'F:/urban_result/urban1990/',
        'base_name': u'URBAN_1990_',
        'out_dir': u'F:/urban_result_1km/urban1990/',        
    },
    1995: {        
        'data_dir': u'F:/urban_result/urban1995/',
        'base_name': u'URBAN_1995_',
        'out_dir': u'F:/urban_result_1km/urban1995/',
    },
    2000: {        
        'data_dir': u'F:/urban_result/urban2000/',
        'base_name': u'URBAN_2000_',
        'out_dir': u'F:/urban_result_1km/urban2000/',
    },
    2005: {        
        'data_dir': u'F:/urban_result/urban2005/',
        'base_name': u'URBAN_2005_',
        'out_dir': u'F:/urban_result_1km/urban2005/',
    },
    2010: {        
        'data_dir': u'F:/urban_result/urban2010/',
        'base_name': u'URBAN_2010_',        
        'out_dir': u'F:/urban_result_1km/urban2010/',
    },
}
arcpy.CheckOutExtension("Spatial")

          

def aggregate(year):
    for id in range(0, 224):     
        print('{0} - {1} begin'.format(year, id))               
        year_config = config[year]
        in_raster_name = year_config['data_dir'] + year_config['base_name'] + str(id) + '.tif'
        out_raster_name = year_config['out_dir'] + year_config['base_name'] + str(id) + '.tif'
        result = arcpy.sa.Aggregate(in_raster=in_raster_name, cell_factor=33, aggregation_type="MEAN", extent_handling="EXPAND", ignore_nodata="DATA")
        result.save(out_raster_name)
        print('{0} - {1} save to {2}'.format(year, id, out_raster_name))               

def main():

    # 设置工作空间
    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')
    arcpy.env.workspace = './tmp'
    

    # 每个年份的数据使用一个进程来处理
    p_list = []
    for year in range(1990, 2011, 5):
        p = multiprocessing.Process(target=aggregate, args=(year,))
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()

    # 
    # for year in range(1990, 2011, 5):
    #     aggregate(year)

    # pool = multiprocessing.Pool(processes=8, maxtasksperchild=30)
    # for year in range(1990, 1991, 5):
    #     for id in range(0, 224):
    #         aggregate_id(year, id)
    #         pool.apply_async(aggregate_id, args=(year, id))
    # pool.close()
    # pool.join()

    print('end')
    


if __name__ == '__main__':
    main()
