# -*- encoding: utf-8 -*-
#
# 脚本功能：使用excel_to_csv.py产生的csv文件从shp文件中提取需要处理的feature并添加year字段，保存为新的shp
#
import csv
from osgeo import ogr
from osgeo import osr
import os







def main():
    
    row_dict = {}
    with open('grid0623.csv') as csvfile:
        reader = csv.DictReader(csvfile, delimiter = '\t')
        for row in reader:
            row_dict[str(row['FID'])] = row
            

    

    in_driver = ogr.GetDriverByName('ESRI Shapefile')
    in_data_set = in_driver.Open('./shp/Individual_1007.shp', 0)
    in_layer = in_data_set.GetLayer()
    in_srs = in_layer.GetSpatialRef()

    out_shp = 'out_shp0623.shp'
    out_driver = ogr.GetDriverByName('ESRI Shapefile')

    if os.path.exists(out_shp):
        out_driver.DeleteDataSource(out_shp)

    out_data_set = out_driver.CreateDataSource(out_shp)
    out_layer = out_data_set.CreateLayer('new', in_srs, ogr.wkbPolygon)

    in_layer_defn = in_layer.GetLayerDefn()
    for i in range(0, in_layer_defn.GetFieldCount()):
        field_defn = in_layer_defn.GetFieldDefn(i)        
        out_layer.CreateField(field_defn)

    year_field_defn = ogr.FieldDefn('year', ogr.OFTString)
    year_field_defn.SetWidth(24)
    out_layer.CreateField(year_field_defn)

    out_layer_defn = out_layer.GetLayerDefn()
    for i in range(0, in_layer.GetFeatureCount()):
        in_feature = in_layer.GetFeature(i)        
        unit_fid = str(in_feature.GetField(4))#  fid and geometry field are ignored

        if unit_fid in row_dict.keys():
            print unit_fid
            out_feature = ogr.Feature(out_layer_defn)
            field_count = out_layer_defn.GetFieldCount()
            for i in range(0, field_count - 1):
                out_feature.SetField(out_layer_defn.GetFieldDefn(i).GetNameRef(), in_feature.GetField(i))
            out_feature.SetField(out_layer_defn.GetFieldDefn(field_count - 1).GetNameRef(), row_dict[unit_fid]['year'])
            geom = in_feature.GetGeometryRef()
            out_feature.SetGeometry(geom)
            out_layer.CreateFeature(out_feature)
            out_feature = None

        in_feature = None

    in_data_set = None
    out_data_set = None

if __name__ == '__main__':
    main()