# -*- coding:UTF-8 -*-

import csv
import cx_Oracle
import time
import os
import paramiko
from xml.etree import ElementTree as ET
from pathlib import Path


# 创建conn_oracle_expcsv函数，功能：根据给定的sql导出文件到系统指定目录；
def conn_oracle_expcsv(sql):
    """
    函数的参数为一个字符串类型的 SQL 语句
    返回值为一个 DataFrame 对象
    """
    # 初始化数据库oracle配置tnsname.ora
    # 注意这里linux系统和Windows下的调用方式不同
    # Linux的调用方式cx_Oracle.init_oracle_client(config_dir="/usr/local/monitor_core/chdata/interface/oracle/conf")
    # cx_Oracle.init_oracle_client(lib_dir=r"C:\oraclient\instantclient_21_6")
    # 建立链接数据库，调整链接数据库的方式使用密文的方式
    connection = cx_Oracle.connect(user="zhushida", password="zhushida", dsn="XE")
    # 执行定义的SQL，这个部分sql应该些成函数，读取系统配置文件指定sql文件
    with open(localfileallpath1, 'w', newline='') as outputfile:
        output = csv.writer(outputfile, dialect='excel')
        # 建立新游标
        curcsv = connection.cursor()
        curcsv.execute(sql)
        colnames = []
        # 生成文件标题
        for col in curcsv.description:
            colnames.append(col[0])
        output.writerow(colnames)
        # 生成文件数据
        for rowdata in curcsv:
            output.writerow(rowdata)
        outputfile.close()
    # 关闭数据库连接
    connection.close()


# 创建csv_filename函数，功能：生成csv文件名称（远程及本地路径名称+格式表名+时间戳）,可以将函数写入字典，这个函数重要目的是处理杂数据；
def base_finisher(tablename, localpath, remotepath):
    """
    :param tablename:
    :param localpath: 注意传入的参数path后面要加入‘/’
    :param remotepath: 注意传入的参数path后面要加入‘/’
    :return: 注意这里是返回的字典 这个字典用于提供其他方法如导出csv文件、传输sftp到远端路径、或其他后续扩展功能；
    """
    # 创建字典
    # 情况字典方法：注意内存优化csv_filename_Dict.clear()
    # 定义函数默认值dict.get(key, default=None)
    csv_filename_dict = {}
    csv_filename_dict.clear()
    datefilename = time.strftime("%Y%m%d%H%M%S")
    datepathname = time.strftime("%Y%m%d")
    #注意这里如果运行程序在Windows系统下需要调整文件路径名字“/”和 “\” 的区别，这里后期加个判断宿主机系统执行不同的定义；
    localpath_sub = localpath + datepathname + '\\'
    remotepath_sub = remotepath + datepathname + '/'
    tablecsv_name = tablename + datefilename + '.csv'
    localpath_sub_file = localpath_sub + tablecsv_name
    remotepath_sub_file = remotepath_sub + tablecsv_name
    csv_filename_dict = {"localfileallpath": localpath_sub_file, "remotefileallpath": remotepath_sub_file,
                         "mkdirlocalpath": localpath_sub, "mkdirremotepath": remotepath_sub}

    return csv_filename_dict


# 函数功能读取传输文件的本地路径、远端路径、通过sftp方式上传到指定服务器路径上、指定端口、用户、密码、服务器IP；
def upload_csvfile_targetsftp(sftpusername, sftppasswd, sftphostname, sftpport):
    """
    :param sftpusername:
    :param sftppasswd:
    :param sftphostname:
    :param sftpport:
    :return:
    """
    try:
        t = paramiko.Transport((sftphostname, sftpport))
        t.connect(username=sftpusername, password=sftppasswd)
        sftp = paramiko.SFTPClient.from_transport(t)
        try:
            sftp.mkdir(mkdirremotepath1)

        except Exception as E:
            print("--Remote directory exists without creation--")

        #sftp.mkdir(mkdirremotepath1)
        sftp.put(localfileallpath1, remotefileallpath1)
        print("--Upload data file succeeded--")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    #这个方法只能初始化一次；
    cx_Oracle.init_oracle_client(lib_dir=r"C:\oraclient\instantclient_21_6")
    # 定义读取定义的配置文件循环，包括：表明、sql路径、本地地址、远端地址、协议、用户密码、端口、IP地址；
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
        disorderly_data = base_finisher(tablename0, local_pathinit, remote_pathinit)
        localfileallpath1 = disorderly_data.get('localfileallpath')
        remotefileallpath1 = disorderly_data.get('remotefileallpath')
        mkdirlocalpath1 = disorderly_data.get('mkdirlocalpath')
        mkdirremotepath1 = disorderly_data.get('mkdirremotepath')
        # 下面语句可以根据系统创建目录路径，Windows和linux路径格式不同这里需要注意，本程序运行的宿主机的系统，下面需要优化进行判断路径是否存在；
        my_file = Path(mkdirlocalpath1)
        if my_file.exists():
            print("--Local directory exists and will not be created--")
        else:
            os.mkdir(mkdirlocalpath1)
        #os.mkdir(mkdirlocalpath1)
        # 下面是用于运行在Linux下的代码；
        #os.system("mkdir %s" % mkdirlocalpath1)
        conn_oracle_expcsv(sqlbody_object.text)
        upload_csvfile_targetsftp(username0, passwd0, ip0, port0)
        print('***Completion and success***')
