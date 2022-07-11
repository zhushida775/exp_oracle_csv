import csv
import cx_Oracle
import time
import os
import paramiko
from xml.etree import ElementTree as ET
from pathlib import Path


for conf_line in open(r"C:\Users\zhusd\Desktop\My experience\python\exp_oracle\init_info.conf"):
    # 读取配置文件存储列表；
    conf_list = conf_line.strip().split(',')
    tablename0 = conf_list[1]
    sql_path0 = conf_list[2]
    local_pathinit = conf_list[3]
    remote_pathinit = conf_list[4]
    protocol = conf_list[5]
    username0 = conf_list[6]
    passwd0 = conf_list[7]
    port0 = int(conf_list[8])
    ip0 = conf_list[9]
    # 对sqlpath进行处理及关联sql语句，并将sql语句存储到xml中以获取调用；
    tree = ET.parse(sql_path0)
    root = tree.getroot()
    # 如果调用表名字可以使用：tablename_object = root.find("tablename")；
    sqlbody_object = root.find("sqlbody")
    # 将配置文件定义的基础路径信息交给base_finisher函数处理，生成本程序识别的格式，base_finisher生成字典，及获取指定key的值；
    #disorderly_data = base_finisher(tablename0, local_pathinit, remote_pathinit)
    #localfileallpath1 = disorderly_data.get('localfileallpath')
    #remotefileallpath1 = disorderly_data.get('remotefileallpath')
    #mkdirlocalpath1 = disorderly_data.get('mkdirlocalpath')
    #mkdirremotepath1 = disorderly_data.get('mkdirremotepath')
    # 下面语句可以根据系统创建目录路径，Windows和linux路径格式不同这里需要注意，本程序运行的宿主机的系统，下面需要优化进行判断路径是否存在；
    #my_file = Path(mkdirlocalpath1)
    #if my_file.exists():
    #    print("--Local directory exists and will not be created--")
    #else:
    #    os.mkdir(mkdirlocalpath1)
    # os.mkdir(mkdirlocalpath1)
    # 下面是用于运行在Linux下的代码；
    # os.system("mkdir %s" % mkdirlocalpath1)
    #conn_oracle_expcsv(sqlbody_object.text)
    print(sqlbody_object.text)
    print(ip0)
    print(username0)