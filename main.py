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


""" 
if __name__ == '__main__':
   allinfo_dict = base_finisher("abc","/root/kkk/","/home/aaa/")
   #使用get（）方法获取字典的键值,可以在这里引用也可以在Oracle生成csv函数里引用
   localfileallpath1 = allinfo_dict.get('localfileallpath')
   remotefileallpath1 = allinfo_dict.get('remotefileallpath')
   mkdirlocalpath1 = allinfo_dict.get('mkdirlocalpath')
   mkdirremotepath1 = allinfo_dict.get('mkdirremotepath')
   print(localfileallpath1)
   print(remotefileallpath1)
   print(mkdirlocalpath1)
   print(mkdirremotepath1)

   for conf_line in open(r"C:\Users\zhusd\Desktop\My experience\python\exp_oracle\init_info.conf"):
       conf_list = conf_line.strip().split(',')
       #conf_dist = {conf_line0}
       print(conf_list)

       tablename0 = conf_list[1]
       sql_path0 = conf_list[2]
       port0 = conf_list[8]
       ip0 = conf_list[9]
       local_pathinit = conf_list[3]

       print(tablename0)
       print(sql_path0)
       print(port0)
       print(ip0)
       print(local_pathinit)

   tree = ET.parse(r"C:\Users\zhusd\Desktop\My experience\python\exp_oracle\sql\tableA.xml")
   root = tree.getroot()
   tablename_object = root.find("tablename")
   sqlbody_object = root.find("sqlbody")
   print(tablename_object.text)
   print(sqlbody_object.text)
"""
