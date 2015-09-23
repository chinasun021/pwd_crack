#!/usr/bin/python
###########################################
#author：chinasun021
#date:2015-9-23
###########################################
import threadpool 
import time,random 
from ftplib import FTP
import sys
import socket
import pdb
import time
#下列参数可根据实际情况修改
onethread_num=100               #一个线程最多处理的任务,即一个tcp连接最多执行的密码尝试次数
onetime_num=100000                #一次循环处理的用户名密码对，这个数据会影响到列表的大小，进而影响到占用的内存
poolsize=20                     #线程池大小
tiao=0                           #密码字典的起始位置，在大字典时可以起到一定的作用
class FtpPasswordScan():
	def __init__(self,ip,port):
		self.ip = ip
		self.port = port
		self.user_list = []
		self.password_list = []
		self.data = []
		self.flag = 0
		self.pwd_num = 0
		self.weakuser = ''
		self.weakpwd = ''

	def passwordCorrect(self,data):
		client = FTP()
		client.connect(self.ip,self.port)
		num=0
		while (num<onethread_num) and (num<len(data)):
			try:
				username=data[num]['username']
				password=data[num]['password']
				num +=1
			#	print password
				client.login(username,password)
			except Exception, e:
				if str(e).find('unknown IP address')!=-1:
					client.close()
					return 2           #error
				continue
			self.weakuser = username
			self.weakpwd = password
			self.flag = 1
			client.close()
			return 1              #exsit weak password
		client.close()
		return 0                 #no weak password
		
	def getscanlist(self):
		self.data = []
		self.user_list = []
		self.password_list = []
		f=file('ftp_user.txt','r')
		while True: 
			line=f.readline()
			if len(line.strip()) == 0:
				break
			self.user_list.append(line.strip())
		f.close()
		f=file('ftp_pwd.txt','r')
		pwd_num=0
		f.seek((tiao+self.pwd_num)*7)
		while (pwd_num<onetime_num):
			line=f.readline()
			if len(line.strip()) == 0:
				break
			if pwd_num== 0:
				print line.strip()
			self.password_list.append(line.strip())
			self.pwd_num += 1
			pwd_num += 1
		f.close()
		temp_num=0
		temp=[]
		total_num=len(self.user_list)*len(self.password_list)
		for i in self.user_list:
			for j in self.password_list:
				temp.append({'username':i,'password':j})
				temp_num +=1
				if (temp_num % onethread_num==0) or (total_num-temp_num < onethread_num):
					self.data.append(temp)
					temp=[]

def passwordScan(ip,port=21):
	pwd_count=-1
	for pwd_count,line in enumerate(open('ftp_pwd.txt','rU')):
		pwd_count +=1
	print "total password:" + str(pwd_count)
	p=FtpPasswordScan(ip,int(port))
	while(pwd_count-tiao>p.pwd_num):
		thread_start=time.time()
		p.getscanlist()
		pool = threadpool.ThreadPool(poolsize) 
		requests = threadpool.makeRequests(p.passwordCorrect,p.data, None) 
		[pool.putRequest(req) for req in requests] 
		pool.wait() 
		pool.dismissWorkers(poolsize,do_join=True)
		if p.flag != 0:
			print 'exist weak password!', p.weakuser, ':', p.weakpwd
			break
		print str(p.pwd_num) + "passwords are checkd!"
		thread_end=time.time()
		print 'total time elapsed:', (thread_end - thread_start), 'seconds'
	if p.flag ==0:
		print "no weak password!"

if __name__ == "__main__":
	socket.setdefaulttimeout(10)
	start=time.time()
	print "start time:" + str(start)
	socket.setdefaulttimeout(10)
	if len(sys.argv)==2:
		passwordScan(sys.argv[1])
	elif len(sys.argv)==3:
		passwordScan(sys.argv[1],sys.argv[2])
	else:
		print 'usage: ', sys.argv[0], ' ip (port(default 21))'
	end=time.time()
	print "end time:" + str(end)
	print 'total time elapsed:', (end - start), 'seconds'
