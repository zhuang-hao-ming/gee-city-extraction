# -*- encoding: utf-8 -*-
#
# 脚本功能： 找出excel表格中所有黄色背景的年份格子，输出一个csv文件
#
from openpyxl import load_workbook
import csv

f = open('grid0623.csv', 'wb') # 输出的csv文件的路径
csv_writer = csv.writer(f, delimiter='\t')
xlsx_name = './shp/data0623.xlsx' # 输出excel表格的路径
wb = load_workbook(xlsx_name)
sheet = wb[u'Sheet1']




csv_writer.writerow([cell.value for cell in sheet[1][:3]] + ['year']) # 输出csv文件的表头

cnt = 0# 黄色格子总数
for row in sheet.rows:
    year_list=[]
    for cell in row:        
        if cell.fill.bgColor.indexed ==64L:
            year_column = cell.column# 年份所在的列            
            year_list.append(str(sheet[year_column + '1'].value))                        
            cnt+=1
    
    if len(year_list) > 0: # 如果该行有黄色格子的年份输出这一行
        cell_row = str(cell.row)# 当前的行
        print(','.join(year_list))# year                    
        print(sheet['A'+cell_row].value)# FID
        print(sheet['B'+cell_row].value)# UE_ID
        print(sheet['C'+cell_row].value)# UrbanGrid_ID
        csv_writer.writerow([sheet['A'+cell_row].value, sheet['B'+cell_row].value,sheet['C'+cell_row].value,','.join(year_list)])

print(cnt)
f.close()
            

