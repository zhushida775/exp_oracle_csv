# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


import csv
import cx_Oracle
# 建立数据库连接
connection  = cx_Oracle.connect(user="wbq", password="Wbq197711",dsn="localhost/orcl2")
curlist = connection.cursor()
# 读取导出配置表 我知道了这个是配置文件的表
sql = "SELECT a.Step,a.RuleType,a.RuleName,a.TableName,a.ExportSQL,a.CSVFileName FROM ProblemToCSVConfig a"
curlist.execute(sql)
# 获取相关配置信息
for row_data in curlist:
  vStep, vRuleType, vRuleName, vTableName, vExportSQL, vCSVFileName=row_data
  print('---------------{} 开始导出到 {} 中---------------'.format(vTableName,vCSVFileName))
  # 开始写文件
  with open(vCSVFileName,'w',newline='') as outputfile:
    output = csv.writer(outputfile, dialect='excel')
    # 建立新游标
    curcsv=connection.cursor()
    curcsv.execute(vExportSQL)
    colnames=[]
    # 生成文件标题
    for col in curcsv.description:
      colnames.append(col[0])
    output.writerow(colnames)
    # 生成文件数据
    for rowdata in curcsv:
      output.writerow(rowdata)
    outputfile.close()
    print('---------------{} 完成导出到 {} 中---------------'.format(vTableName, vCSVFileName))