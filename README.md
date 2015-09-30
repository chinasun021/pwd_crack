
# pwd_crack
cert、ftp、ssh、mysql、windows 暴力破解

cert和ftp的程序对大容量字典支持较好，其他的几个是之前写的，暂时没有修改（对大容量字典支持较差，需一次性将字典所有数据读取出来）

##cert暴力破解
###需要安装的软件
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool 

<code>
	apt-get install python-setuptools

	easy_install threadpool
</code>
安装expect软件：

<code>apt-get install expect</code>
###使用方法：
./cert_crack.py cert filename
##ftp暴力破解
###需要安装的软件
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool 

<code>
	apt-get install python-setuptools

	easy_install threadpool
</code>
###使用方法：
./ftp_crack.py ip (port(default 21))
##ssh暴力破解
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool、MySQLdb 

<code>
	apt-get install python-setuptools

	easy_install threadpool

	easy_install paramiko
</code>
###使用方法：
./ssh_crack.py ip (port(default 22))

##mysql暴力破解
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool、MySQLdb 

<code>
	apt-get install python-setuptools

	easy_install threadpool

	apt-get install python-mysqldb
</code>
###使用方法：
./mysql_crack.py ip (port(default 3306))

##windows暴力破解
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool、MySQLdb 

<code>
	apt-get install python-setuptools

	easy_install threadpool

	easy_install impacket
</code>
###使用方法：
./win_crack.py ip (port(default 3389))
