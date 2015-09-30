#!/usr/bin/python
#coding=utf-8
###########################################
#author：chinasun021
#date:2015-9-25
###########################################
import threadpool
import threading
import os
import sys
import re
import time
onetime_num=10000     #一次最多读取的密码个数
poolsize=100          #线程池大小
lock = threading.Lock()
class CertPasswordScan():
	def __init__(self,cert):
		self.cert=cert
		self.password_list=[]
		self.weakpwd=''
		self.pos=0
		self.num=0
		self.flag=0

	def checklog(self,logfile):
		flag=1
		myfile = file(logfile, "r+")
		for line in myfile:
			line=line.strip()
			if len(line)!=0 and line=="unable to load key":
				flag=0
		myfile.close()
		return flag

	def passwordCorrect(self,password):
		if len(password)>=4:
			lock.acquire()
			os.system('./cert_crack.sh ' + self.cert + ' ' + password + ' 1>CertScan.log')
			if self.checklog('CertScan.log') == 1:
				self.weakpwd = password
				self.flag=1
			lock.release()

	def getscanlist(self):
		self.password_list=[]
		f=file('password.txt','r')
		num=0
		f.seek(self.pos)
		while (num<onetime_num):
			line=f.readline()
			if len(line.strip()) == 0:
				break
			self.pos=f.tell()
			num+=1
			self.num+=1
			self.password_list.append(line.strip())
		f.close()
def passwordScan(cert):
	start=time.time()
	print "start time:" + str(start)
	pwd_count=-1
	for pwd_count,line in enumerate(open('password.txt','rU')):
		pwd_count +=1
	print "total password:" + str(pwd_count)
	p=CertPasswordScan(cert)
	while(pwd_count>p.num):
		p.getscanlist()
		pool = threadpool.ThreadPool(poolsize) 
		requests = threadpool.makeRequests(p.passwordCorrect,p.password_list, None) 
		[pool.putRequest(req) for req in requests] 
		pool.wait() 
		pool.dismissWorkers(poolsize,do_join=True)
		if p.flag == 1:
			print "exsit weak password '",p.weakpwd,"'!"
			break
	if p.flag == 0:
		print "no weak password"
	os.remove('CertScan.log')
	os.remove('privatekey.tmp')
	end=time.time()
	print "end time:" + str(end)
	print 'total time elapsed:', (end - start), 'seconds'

if __name__ == '__main__':
	if len(sys.argv) ==2:
		if os.path.exists(sys.argv[1]):
			passwordScan(sys.argv[1])
		else:
			print sys.argv[1],'not exists!'
	else:
		print 'usage: ',sys.argv[0],'cert filename'
		print 'eg: ',sys.argv[0],'test.pem'
