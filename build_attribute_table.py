# -*- encoding：utf-8 -*-
#
# 脚本功能：重新构建栅格图像属性表
#
#
import arcpy
import os.path
import multiprocessing


#
# 规定数据的路径是：{基础目录}/urban{年份}/URBAN_{年份}_{id}.tif
#
urban_data_base_dir = u'F:/urban_result' # 数据的基础目录




def build_attribute(year):
    print('{} begin'.format(year))
    for i in range(0, 224):

        tif_url = '{0}/urban{1}/URBAN_{2}_{3}.tif'.format(urban_data_base_dir, year, year, i)                
        try:
            arcpy.BuildRasterAttributeTable_management(tif_url)
            print 'build ' + tif_url + ' successfully!'
        except Exception:    
            print 'build ' + tif_url + ' fail!'
            
def main():
    #
    # 每个年份使用一个进程来运行
    #
    p_list = []
    for year in range(1990, 2011, 5):
        p = multiprocessing.Process(target=build_attribute, args=(year,))
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()
    print('end')

if __name__ == '__main__':
    main()
    
    
        
    
