#!/usr/bin/python
from impacket import smb
import threadpool 
import time,random 
import sys
import socket
import pdb
poolsize=50
class WinPasswordScan():
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
		password=data['password']
		try:
			client = smb.SMB('*SMBSERVER',ip)
			client.login(username,password)
		except Exception:
			return False
		self.weakuser = username
		self.weakpwd = password
		self.flag = 1
		return True

	def getscanlist(self):
		f=file('win_user.txt','r')
		while True:
			line=f.readline()
			if len(line.strip()) == 0:
				break
			self.user_list.append(line.strip())
		f.close()
		f=file('win_pwd.txt','r')
		while True:
			line=f.readline()
			if len(line.strip()) == 0:
				break
			self.password_list.append(line.strip())
		f.close()

		for i in self.user_list:
			for j in self.password_list:
				self.data.append({'ip':self.ip,'port':self.port,'username':i,'password':j})

def passwordScan(ip,port=3389):
	start=time.time()
	sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sk.settimeout(5)
	try:
		sk.connect((ip,port))
	except Exception:
		print 'Server port',port,' not connect!'
		return -1
	sk.close()
	p=WinPasswordScan(ip,port)
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
		print 'usage: ', sys.argv[0], ' ip (port(default 3389))'
