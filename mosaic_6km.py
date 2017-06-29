# -*- encoding: utf-8 -*-
#
# 脚本功能：完成6km缓冲区的镶嵌
#

import os
import os.path
import arcpy
from multiprocessing import Process

urban_data_base_dir = 'F:/urban_result'



# 从shp文件中得到，6公里缓冲区id和对应的10度格网的对应关系
fc_name = './shp/Individual_1007.shp'
id_grid_dict = {}
with arcpy.da.SearchCursor(fc_name, ['UnitFID', 'UrbanGrid']) as search_cursor:
    for row in search_cursor:
        id_grid_dict[row[0]] = row[1]

# 读取指定目录下所有待镶嵌栅格的文件名
def get_tif_id_list(dir_name='./1990'):
    file_list = os.listdir(dir_name)
    tif_id_list = []
    for item in file_list:
        if os.path.splitext(item)[1] == '.tif':        
            tif_id_list.append(int(os.path.splitext(item)[0]))
    return tif_id_list


def mosaic(year,tif_id_list):
    
    for tif_id in tif_id_list:
        grid_id = int(id_grid_dict[tif_id])
        # 把tif_id镶嵌到grid_id中
        input_file = './{0}/{1}.tif'.format(year, tif_id)
        target_file = '{0}/urban{1}/URBAN_{2}_{3}.tif'.format(urban_data_base_dir, year, year, grid_id)    
        arcpy.Mosaic_management(input_file, target_file, mosaic_type='LAST')
        print('{0} -> {1} mosaic ok'.format(input_file, target_file))




def main():

    #——每个年份使用一个进程
    p_list = []
    for year in range(1990, 2011, 5):        
        print('{} start'.format(year))
        tif_id_list = get_tif_id_list('./{0}'.format(year))        
        p = Process(target=mosaic, args=(year, tif_id_list))
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    print('end')

if __name__ == '__main__':
    main()
    




        

    
    





