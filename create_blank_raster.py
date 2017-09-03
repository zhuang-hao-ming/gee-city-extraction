# encoding: utf-8
import arcpy
from arcpy import env
from arcpy.sa import *
import multiprocessing

# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")


config = {


'in_folder_path': u'F:/data/nuaci_1980',# 输入10度栅格路径, 规定输入栅格的路径是 {in_folder_path}/{input_prefix}{10_grid_code}.tif
'out_folder_path': u'F:/data/output_1980',# 输出10度栅格路径, 规定输出栅格的路径是 {out_folder_path}/{output_prefix}{10_grid_code}.tif
'input_prefix': 'NUACI1980_', # 输入10度栅格名字前缀
'output_prefix': 'URBAN_1980_', # 输出10度栅格名字前缀
'begin_fid': 0, #包含90
'end_fid': 89, #包含134
}









# # try:
# NUACI_path = '{}/{}{}.tif'.format(config['in_folder_path'], config['input_prefix'], grid_code)   
# inRaster = Raster(NUACI_path)
# outRas_path = '{}/{}{}.tif'.format(config['out_folder_path'], config['output_prefix'], grid_code) 
# arcpy.Minus_3d(inRaster, inRaster, outRas_path)
# print('{} -> {}'.format(NUACI_path, outRas_path))
# # except Exception:
#     #print grid_code, 'error'

def do_task(grid_code):

    NUACI_path = '{}/{}{}.tif'.format(config['in_folder_path'], config['input_prefix'], grid_code)   
    inRaster = Raster(NUACI_path)
    outRas_path = '{}/{}{}.tif'.format(config['out_folder_path'], config['output_prefix'], grid_code) 
    arcpy.Minus_3d(inRaster, inRaster, outRas_path)
    print('{} -> {}'.format(NUACI_path, outRas_path))


if __name__ == '__main__':
    
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count(), maxtasksperchild=30)
    for grid_code in range(config['begin_fid'], config['end_fid']+1):
            pool.apply_async(do_task, args=(grid_code,))
    pool.close()
    pool.join()