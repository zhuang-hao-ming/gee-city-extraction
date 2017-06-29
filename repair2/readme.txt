# 文件功能

1.cell_statistic.py

对所有年份的指数数据使用最大值的方法统计，得到新的数据，使得指数数据缺失最少。

2.repair_again.py

对于cell_statistic.py得到的数据，只在异常的城市缓冲区内做阈值分割，得到和缓存区对应的新的二值图像，然后使用最大值法mosaic到前面repair得到的结果数据中。

# 操作流程

1.每人负责自己所分的块的所有年份。

2.先修改cell_statistic.py文件头部的config，和workspace参数，然后运行，完成最大值统计，得到新数据。

3.
修改repair_again.py文件头部的config和buffer_file参数，然后完成每个年份的修补。注意：每个年份的参数是不一样的。

 
