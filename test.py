import cx_Oracle
import time
import xml
from xml.etree import ElementTree as ET
import paramiko

"""
#注意这里linux和Windows下调用的方式不一样
cx_Oracle.init_oracle_client(lib_dir=r"C:\oraclient\instantclient_21_6")
# 下面的是Linux下的调用方式
#cx_Oracle.init_oracle_client(config_dir="C:\oraclient\instantclient_21_6")
# 建立链接数据库，调整链接数据库的方式使用密文的方式
connection = cx_Oracle.connect(user="zhushida", password="zhushida", dsn="XE")

connection.close()
"""


def base_finisher(tablename, localpath, remotepath):
    """
    这里一共三个参数，表名用于生成对应表明csv文件、本地目录路径+文件名、远端路径和文件名、本函数后续可以在增加参数用于其他扩展用途；
    将传入参数加入字典中进行后期调用；
    :param tablename:
    :param localpath: 注意传入的参数path后面要加入‘/’
    :param remotepath: 注意传入的参数path后面要加入‘/’
    :return: 注意这里是返回的字典 这个字典用于提供其他方法如导出csv文件、传输sftp到远端路径、或其他后续扩展功能；
    """
    # 创建字典
    # csv_filename_Dict.clear(),如果要使用字典这里要有个判断是否有值，或者上来就删除，然后在加入
    # dict.get(key, default=None)
    # 返回指定键的值，如果键不在字典中返回 default 设置的默认值
    csv_filename_Dict = {}
    csv_filename_Dict.clear()
    datefilename = time.strftime("%Y%m%d%H%M%S")
    datepathname = time.strftime("%Y%m%d")
    localpath_sub = localpath + datepathname + '/'
    remotepath_sub = remotepath + datepathname + '/'
    tablecsv_name = tablename + datefilename + '.csv'
    localpath_sub_file = localpath_sub + tablecsv_name
    remotepath_sub_file = remotepath_sub + tablecsv_name
    csv_filename_Dict = {"localfileallpath": localpath_sub_file, "remotefileallpath": remotepath_sub_file,
                         "mkdirlocalpath": localpath_sub, "mkdirremotepath": remotepath}
    # localfileallpath1 = csv_filename_Dict.get('localfileallpath')
    # remotefileallpath1 = csv_filename_Dict.get('remotefileallpath')
    # mkdirlocalpath1 = csv_filename_Dict.get('mkdirlocalpath')
    # mkdirremotepath1 = csv_filename_Dict.get('mkdirremotepath')
    return csv_filename_Dict


def upload_csvfile_targetsftp(sftpusername, sftppasswd, sftphostname, sftpport):
    try:
        t = paramiko.Transport((sftphostname, sftpport))
        t.connect(username=sftpusername, password=sftppasswd)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.mkdir('/home/xtd/20222')
        sftp.put(
            r'C:\Users\zhusd\Desktop\My experience\python\exp_oracle\SEND\20220702\EXP_DATA_TEST20220702195945.csv',
            '/home/xtd/20222/table.csv')
        print("Upload datafile complete!!!")

    except Exception as e:
        print(e)


if __name__ == '__main__':
    upload_csvfile_targetsftp('xtd','xtd@505!','119.40.37.126',2210)
