# 阈值分割

1. get_utban.py 对二度格网按照目标面积进行阈值分割，然后把分割的结果镶嵌到10度格网栅格中

# 验证1
1. caculate_city_area.py 计算欧空局数据的城市面积

2. interpolate_area.py 使用欧空局1990，2000，2010年份的面积数据，插值出其它年份的面积数据

3. validation.py 根据城市缓冲区在欧空局下和NUACI下的面积差异，把NUACI面积比欧空局面积的50%还小的城市识别为异常城市。

4. repair1.py 对于validation.py识别出来的异常城市，使用相邻年份的非异常数据来mosaic

# 验证2
1. cell_statistic.py 对所有年份的指数数据使用最大值的方法统计，得到新的数据，使得指数数据缺失最少。

2. repair2 对于cell_statistic.py得到的数据，只在异常的城市缓冲区内做阈值分割，得到新的二值图像，然后使用最大值法mosaic到前面repair得到的结果数据中。


# 验证3

1. excel_to_csv.py 整理需要处理的id
2. link_csv_to_shp.py 将前一部输出的csv和提供的shp文件进行连接并插入year字段，输出一个新的shp
3. caculate_city_area.py 计算欧空局数据的城市面积
4. interpolate_area.py 使用欧空局1990，2000，2010年份的面积数据，插值出其它年份的面积数据
5. segementation.py 对于cell_statistic.py得到的数据，只在异常的城市缓冲区内做阈值分割，得到新的二值图像，然后输出保存。
6. mosaic_6km.py 将segementation.py输出的结果镶嵌回结果中

# 重建属性表

1. build_attribute_table.py 重建阈值分割得到的二值图像的属性表。

# 重采样和镶嵌

1. aggregate 将30米的数据聚集到990米
2. mosaic_all 将同一个年份的所有栅格镶嵌到一起

