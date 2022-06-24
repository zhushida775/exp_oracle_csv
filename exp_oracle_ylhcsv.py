# /usr/bin/python3
import csv
import cx_Oracle
import time
import os
import paramiko

# 初始化数据库配置
cx_Oracle.init_oracle_client(config_dir="/usr/local/monitor_core/chdata/interface/oracle/conf")
# 建立数据库连接
connection = cx_Oracle.connect(user="net_admin", password="12123APP@web_2019", dsn="hlwdb105")
# 定义sql查询条件
sql1 = """
select a.sfzmmc,
       a.sfzmhm,
       a.lsh,
       a.rlzpurl,
       a.qzzpurl,
       a.cjsj,
       a.gxsj
  from NET_SYS_USER_AUTH_IMG a
 where a.cjsj >= to_date(to_char(SYSDATE - 1, 'yyyy-mm-dd') || ' 00:00:00',
                         'yyyy-mm-dd hh24:mi:ss')
   AND a.cjsj <= to_date(to_char(SYSDATE - 1, 'yyyy-mm-dd') || ' 23:59:59',
                         'yyyy-mm-dd hh24:mi:ss')
"""
sql2 = """
select b.sfzmhm,
       b.xm,
       b.ly,
       b.type,
       b.zp1,
       b.zp2,
       b.rlsbzt,
       b.rl_code,
       b.rl_msg,
       b.cjsj,
       b.similarity,
       b.bz,
       b.interval,
       b.fzjg,
       b.ywlx,
       b.glxh,
       b.gnid,
       b.jcqd,
       b.rzlsh
  from NET_MHS_FACE_RESULT b
 where b.cjsj >= to_date(to_char(SYSDATE - 1, 'yyyy-mm-dd') || ' 00:00:00',
                         'yyyy-mm-dd hh24:mi:ss')
   AND b.cjsj <= to_date(to_char(SYSDATE - 1, 'yyyy-mm-dd') || ' 23:59:59',
                         'yyyy-mm-dd hh24:mi:ss')
"""
# 定义文件输出名称
datefilename = time.strftime("%Y%m%d%H%M%S")
datepathname = time.strftime("%Y%m%d")
sendpath = '/usr/local/monitor_core/chdata/yhlsend_tables/send_data/' + datepathname + '/'
remotepath = '/home/xtd/' + datepathname + '/'
netsysuserauthimg_filename = 'XINTIANDI_NET_SYS_USER_AUTH_IMG' + datefilename + '.csv'
netmhsfaceresult_filename = 'XINTIANDI_NET_MHS_FACE_RESULT' + datefilename + '.csv'
netsysuserauthimg = sendpath + netsysuserauthimg_filename
netmhsfaceresult = sendpath + netmhsfaceresult_filename
netsysuserauthimg_r = remotepath + netsysuserauthimg_filename
netmhsfaceresult_r = remotepath + netmhsfaceresult_filename
os.system("mkdir %s" % (sendpath))

# 开始写文件
# with open(netsysuserauthimg,'w',newline='') as outputfile:
with open(netsysuserauthimg, 'w', newline='') as outputfile:
    output = csv.writer(outputfile, dialect='excel')
    # 建立新游标
    curcsv = connection.cursor()
    curcsv.execute(sql1)
    colnames = []
    # 生成文件标题
    for col in curcsv.description:
        colnames.append(col[0])
    output.writerow(colnames)
    # 生成文件数据
    for rowdata in curcsv:
        output.writerow(rowdata)
    outputfile.close()

with open(netmhsfaceresult, 'w', newline='') as outputfile:
    output = csv.writer(outputfile, dialect='excel')
    # 建立新游标
    curcsv = connection.cursor()
    curcsv.execute(sql2)
    colnames = []
    # 生成文件标题
    for col in curcsv.description:
        colnames.append(col[0])
    output.writerow(colnames)
    # 生成文件数据
    for rowdata in curcsv:
        output.writerow(rowdata)
    outputfile.close()

print('-------send-tables------')
print('-------send-tables------')
print('-------send-tables------')
print('-------send-tables------')
sftpusername = "xtd"
sftppasswd = "xtd@DsVte"
sftphostname = "192.159.139.4"
sftpport = 22

try:
    t = paramiko.Transport((sftphostname, sftpport))
    t.connect(username=sftpusername, password=sftppasswd)
    sftp = paramiko.SFTPClient.from_transport(t)

    sftp.mkdir(remotepath)
    sftp.put(netsysuserauthimg, netsysuserauthimg_r)
    sftp.put(netmhsfaceresult, netmhsfaceresult_r)

    print("Upload datafile complete!!!")

except Exception as e:
    print(e)