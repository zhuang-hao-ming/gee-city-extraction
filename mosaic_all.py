# -*- encoding: utf-8 -*-
# 脚本功能： 将同一个年份的所有栅格镶嵌在一起，得到一个大的栅格文件

import arcpy


def main():
    for year in range(1990, 2011, 5):
        arcpy.env.workspace = u'F:/urban_result_1km/urban{0}'.format(year)    
        tif_name_arr = []
        base_name = 'URBAN_{0}_'.format(year)
        for idx in range(0, 224):
            tif_name_arr.append(base_name + str(idx) + '.tif')
        tif_name_str = ';'.join(tif_name_arr)
        print(tif_name_str)        
        arcpy.MosaicToNewRaster_management(input_rasters=tif_name_str, output_location='./mosaic_new', raster_dataset_name_with_extension='urban{0}.tif'.format(year), pixel_type='32_BIT_FLOAT', number_of_bands=1, mosaic_method='MAXIMUM')

        print('mosaic {0} finish'.format(year))


if __name__ == '__main__':
    main()
    