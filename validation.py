# -*- encoding: utf-8 -*-
# 
# 功能：验证get_urban.py输出的结果在给定的城市上的正确性
# 规定，如果get_urban结果在给定的城市上城市像元数量比欧空局的数据少50%这认为是异常 
# 输出两个文件，area_file：所有城市记录， outliar_file: 异常城市记录
#
import arcpy
import arcpy.sa

arcpy.CheckOutExtension("Spatial")
arcpy.env.extent = 'Default'


def validate(buffer_file, data_dir, data_file_base, area_field, outliar_file, area_file, begin_grid, end_grid):
    fo_outliar = open(outliar_file, 'w')
    fo_area = open(area_file, 'w')

    def get_area(raster_file, row):
        mask = row.getValue('Shape')
        city_raster = arcpy.sa.ExtractByMask(raster_file, mask)
        city_arr = arcpy.RasterToNumPyArray(city_raster)
        city_arr = city_arr == 1    
        actual_area = city_arr.sum() * 0.0009                        
        return actual_area



    def validate_city(fid):
        actual_area = 0
        ghs_area = 0
        grid_code = 0
        for row in arcpy.SearchCursor(buffer_file, '"TARGET_FID" = {0}'.format(fid)):
            ghs_area = float(row.getValue(area_field))
            city_code = str(row.getValue('City_Code'))
            grid_code = row.getValue('code')

            if int(grid_code) < begin_grid or int(grid_code) > end_grid:
                return
            
            grid_code_file = data_dir + data_file_base + grid_code + '.tif'


            grid_raster = arcpy.Raster(grid_code_file)
            actual_area += get_area(grid_raster, row)
        print('fid', fid, 'actual_area : ', actual_area, 'ghs_area', ghs_area)
        fo_area.write(str(fid) + '\t' + str(actual_area) + '\t' + str(ghs_area) + '\t' + str(grid_code) + '\n')
        if not (actual_area > ghs_area * (1 - 0.5)):
            print('outliar')
            fo_outliar.write(str(fid) + '\t' + str(actual_area) + '\t' + str(ghs_area) + '\t' + str(grid_code) + '\n')
        
    for fid in range(0, 1692):
        validate_city(fid)

    fo_outliar.close()
    fo_area.close()



if __name__ == '__main__':

    buffer_file = u'E:/Data/city_extraction/validation/buffer_to_grid10.shp'# 十度格网和城市连接后的shp
    data_dir = u'F:/Data/urban2005/'# 栅格数据所在的文件夹
    data_file_base = u'URBAN_2005_' # 栅格数据文件名的前缀
    area_field = 'F2005_area' # 欧空局的面积字段
    outliar_file = './error_log/urban2005_outliar.txt' # 输出异常城市记录到该文件
    area_file = './error_log/urban2005_area.txt'
    begin_grid = 0# 开始的10度格网号
    end_grid = 223# 结束的10度格网号 
    validate(buffer_file, data_dir, data_file_base, area_field, outliar_file, area_file, begin_grid, end_grid)


    
            




