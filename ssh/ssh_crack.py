#!/usr/bin/python
import threadpool 
import paramiko
from paramiko import AutoAddPolicy
import time,random 
import sys
import socket
import pdb
from time import clock as now
poolsize=10
class SSHPasswordScan():
	def __init__(self,ip,port):
		self.ip = ip
		self.port = port
		self.user_list = []
		self.password_list = []
		self.data = []
		self.flag = 0
		self.weakuser = ''
		self.weakpwd = ''

	def passwordCorrect(self,data):
		ip=data['ip']
		port=data['port']
		username=data['username']
		passwd=data['password']
		try:
			client = paramiko.SSHClient()
			client.load_system_host_keys()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(ip, port, username, passwd)
			client.close()
			self.flag = 1
		except paramiko.AuthenticationException, e1:
			print '[-] Try passwd\t\t%-30s failed.' % passwd
			client.close()
			return -1
		print '[+] Try passwd\t\t%-30s ok.' % passwd
		self.weakuser=username
		self.weakpwd=passwd
		return 0

	def getscanlist(self):
		f=file('ssh_user.txt','r')
		while True:
			line=f.readline()
			if len(line.strip()) == 0:
				break
			self.user_list.append(line.strip())
		f.close()
		f=file('ssh_pwd.txt','r')
		while True:
			line=f.readline()
			if len(line.strip()) == 0:
				break
			self.password_list.append(line.strip())
		f.close()

		for i in self.user_list:
			for j in self.password_list:
				self.data.append({'ip':self.ip,'port':self.port,'username':i,'password':j})

def passwordScan(ip,port=22):
	start=time.time()
	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sk.settimeout(5)
	try:
		sk.connect((ip,port))
	except Exception:
		print 'Server port',port,' not connect!'
		return -1
	sk.close()
	print 'ssh check user and pass:'
	p=SSHPasswordScan(ip,port)
	p.getscanlist()
	pool = threadpool.ThreadPool(poolsize) 
	requests = threadpool.makeRequests(p.passwordCorrect,p.data, None) 
	[pool.putRequest(req) for req in requests] 
	pool.wait()
	pool.dismissWorkers(poolsize,do_join=True)
	if p.flag == 0:
		print 'no weak password!'
	else:
		print 'exist weak password!', p.weakuser, ':', p.weakpwd
	end=time.time()
	print 'total time elapsed:', (end - start), 'seconds'

if __name__ == "__main__":
	socket.setdefaulttimeout(10)
	if len(sys.argv)==2:
		passwordScan(sys.argv[1])
	elif len(sys.argv)==3:
		passwordScan(sys.argv[1],sys.argv[2])
	else:
		print 'usage: ', sys.argv[0], ' ip (port(default 22))'
