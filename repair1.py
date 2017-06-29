# -*- encoding: utf-8 -*-
#
# 功能：
# 对于validation.py输出的异常城市，使用相邻年份的正常城市进行替换
#  
import csv
import arcpy
import arcpy.sa

arcpy.CheckOutExtension("Spatial")




buffer_file = u'E:/Data/city_extraction/validation/buffer_to_grid10.shp'# 10度格网和城市连接后的shp
dir_dict = {
    1990: {
        'data_dir': u'./data/urban1990/',# 1990年数据的目录
        'data_file_base': u'URBAN_1990_',# 1990年数据文件名的前缀  
		'outliar_file': u'./error_log1/validation1990_outliar.txt',# 1990年异常城市记录文件
		'area_file': u'./error_log1/validation1990_area.txt'
    },
    1995: {
        'data_dir': u'./data/urban1995/',
        'data_file_base': u'URBAN_1995_',
		'outliar_file': u'./error_log1/validation1995_outliar.txt',
        'area_file': u'./error_log1/validation1995_area.txt'
    },
    2000: {
        'data_dir': u'./data/urban2000/',
        'data_file_base': u'URBAN_2000_',
		'outliar_file': u'./error_log1/validation2000_outliar.txt',
        'area_file': u'./error_log1/validation2000_area.txt'
    },
    2005: {
        'data_dir': u'./data/urban2005/',
        'data_file_base': u'URBAN_2005_',
		'outliar_file': u'./error_log1/validation2005_outliar.txt',
        'area_file': u'./error_log1/validation2005_area.txt'
    },
    2010: {
        'data_dir': u'./data/urban2010/',
        'data_file_base': u'URBAN_2010_',
		'outliar_file': u'./error_log1/validation2010_outliar.txt',
        'area_file': u'./error_log1/validation2010_area.txt'
    },
}







# 把src_year的数据替换为target_year的数据
def replace_tif(row, src_year, target_year):
            
    # src_year的数据路径
    data_dir_src = dir_dict[src_year]['data_dir']
    data_file_base_src = dir_dict[src_year]['data_file_base']
    # target_year的数据路径
    data_dir_target = dir_dict[target_year]['data_dir']
    data_file_base_target = dir_dict[target_year]['data_file_base']

    mask = row.getValue('Shape')
    grid_code = row.getValue('code')
    grid_code_file_target = data_dir_target + data_file_base_target + grid_code + '.tif'
    grid_raster_target = arcpy.Raster(grid_code_file_target)
    city_raster_target = arcpy.sa.ExtractByMask(grid_raster_target, mask)
    grid_code_file_src = data_dir_src + data_file_base_src + grid_code + '.tif'

    
    arcpy.Mosaic_management(city_raster_target, grid_code_file_src, "LAST", "FIRST", "", "", "", "", "")


# 读入要修补的记录
def read_outlair(year_order_list):
    ret = {
        1990: {},
        1995: {},
        2000: {},
        2005: {},
        2010: {}
    }

    year_1, year_2, year_3, year_4, year_5 = year_order_list

    for year in range(1990, 2010+1, 5):
        if (year == year_1):
		    outliar_file = dir_dict[year]['outliar_file']
        else:
		    outliar_file = dir_dict[year]['area_file']      
            
        with open(outliar_file, 'rb') as csvfile:
            spam_readder = csv.reader(csvfile, delimiter='\t')
            for row in spam_readder:        
                ret[year][row[0]] = row[1:]
    return ret



def repair(year_order_list, outliar_dict, cannot_repair_file):
    fo_cannot_repair = open(cannot_repair_file, "w")
    
    year_1, year_2, year_3, year_4, year_5 = year_order_list

    print('--------',year_order_list,'-----------')



    for key in outliar_dict[year_1].keys():

        
        year1_ghs_area = float(outliar_dict[year_1][key][1]) * 0.5 # year1的欧空局城市面积


        if float(outliar_dict[year_2][key][0]) > year1_ghs_area: # 另一个年份的数据如果不异常，或者，值比要替换年份的欧空局数据的0.5倍大，既可以替换
            for row in arcpy.SearchCursor(buffer_file, '"TARGET_FID" = {0}'.format(int(key))):
                #从1995年中切一块，mosaic到1990年去            
                replace_tif(row, year_1, year_2)
            print('repair finish', key)                
        elif float(outliar_dict[year_3][key][0]) > year1_ghs_area:
            for row in arcpy.SearchCursor(buffer_file, '"TARGET_FID" = {0}'.format(int(key))):
                replace_tif(row, year_1, year_3)            
            print('repair finish', key)
        elif float(outliar_dict[year_4][key][0]) > year1_ghs_area:
            for row in arcpy.SearchCursor(buffer_file, '"TARGET_FID" = {0}'.format(int(key))):            
                replace_tif(row, year_1, year_4)
            print('repair finish', key)
        elif float(outliar_dict[year_5][key][0]) > year1_ghs_area:
            for row in arcpy.SearchCursor(buffer_file, '"TARGET_FID" = {0}'.format(int(key))):
                replace_tif(row, year_1, year_5)            
            print('repair finish', key)
        else:
            #补不了
            print('cannot to repair', key)
            fo_cannot_repair.write(str(key) + '\n')
    fo_cannot_repair.close()


if __name__ == '__main__':

    

    
    
    

    # # 修补1990
    # repair([1990, 1995, 2000, 2005, 2010], outliar_dict, cannot_repair_file)

    # 修补1995
    # repair([1995, 1990, 2000, 2005, 2010], outliar_dict)

    # # 修补2000
    # cannot_repair_file = './error_log/cannot_repair_file_2000.txt' # 记录不能修复的id
    # repair([2000, 1995, 2005, 2010, 1990], outliar_dict, cannot_repair_file)

    # 得到所有异常城市记录
    outliar_dict = read_outlair([2005, 2010, 2000, 1995, 1990])
    cannot_repair_file = './error_log/cannot_repair_file_2005_0602.txt' # 记录不能修复的id
    # 修补2005
    repair([2005, 2010, 2000, 1995, 1990], outliar_dict, cannot_repair_file)

    # cannot_repair_file = './error_log/cannot_repair_file_2010.txt' # 记录不能修复的id
    # # # 修补2010
    # repair([2010, 2005, 2000, 1995, 1990], outliar_dict, cannot_repair_file)