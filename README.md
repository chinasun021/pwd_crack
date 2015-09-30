
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

##ftp暴力破解
###需要安装的软件
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool 

<code>
	apt-get install python-setuptools

	easy_install threadpool
</code>

##ssh暴力破解
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool、MySQLdb 

<code>
	apt-get install python-setuptools

	easy_install threadpool
<
	easy_install paramiko
</code>

##mysql暴力破解
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool、MySQLdb 

<code>
	apt-get install python-setuptools

	easy_install threadpool

	apt-get install python-mysqldb
</code>

##windows暴力破解
Linux系统（建议选用ubuntu）

安装python2.7,需要额外安装的python模块：threadpool、MySQLdb 

<code>
	apt-get install python-setuptools

	easy_install threadpool

	easy_install impacket
</code>
