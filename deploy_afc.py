#!/usr/bin/env python
# -*-coding:utf8 -*-
import os
import time
import datetime
import re

#--------------------------------------------------------------
def TimeStampToTime(timestamp):
	timeStruct = time.localtime(timestamp)
	return time.strftime("%Y-%m-%d %H:%M:%S",timeStruct)

def get_FileSize(filePath):
	filePath = unicode(filePath,'utf8')
	fsize = os.path.getsize(filePath)
	fszie = fsize/float(1024*1024)
	return round(fsize,2)

def get_FileCreateTime(filePath):
	filePath = unicode(filePath,'utf8')
	t = os.path.getctime(filePath)
	return TimeStampToTime(t)

@show_line
def check_tomcat():
	cmd = "sudo ps -ef | grep '/data/tqlh_af/bin/tomcat'"
	result = os.popen(cmd).read()
	print result 
	return result

def show_line(func):
	def wrapper(*args,**kwargs):
		print "-"*80
		return func(*args,**kwargs)
	return wrapper
@show_line
def rm_job(rm_path):
	cmd = "rm -rf {}".format(rm_path)
	result = os.popen(cmd).read()
	print result

@show_line
def cp_job(cp_from,cp_to):
	cmd = "cp {} {}".format(cp_from,cp_to)
	result = os.popen(cmd).read()
	print result

@show_line
def mv_job(mv_from,mv_to):
	cmd = "mv {} {}".format(mv_from,mv_to)
	result = os.popen(cmd).read()
	print result

@show_line
def kill_tomcat():
	cmd = "sudo sh /root/startup.sh stop"
	result = os.popen(cmd).read()
	print result
	time.sleep(2)
	while True:
		if "/data/tqlh_af/conf" in check_tomcat():
			cmd = "sudo ps -ef | grep '/data/tqlh_af/bin/tomcat'|awk {'print $2'}"
			pid_str = os.popen(cmd).read()
			xx = r'\d{4,5}'
			rex = re.compile(xx)
			pid = rex.findall(result)[0]
			cmd_kill = "sudo kill -9 {}".format(pid)
		else:
			print "杀掉tomcat"
			break

@show_line
def file_info(dir_root):
	for file_name in os.listdir(dir_root):
		file_path = os.path.join(root,file_name)
		print str(file_name)+'   '+str(get_FileCreateTime(file_path))+"   "+str(get_FileSize(file_path))+"MB"


@show_line
def up_tomcat()
	cmd = "sudo sh /root/startup.sh satrt"
	result = os.popen(cmd).read()
	print result,"启动tomcat"

#----------------------------------------------------------------------------
webapps_root = "/data/tqlh_af/webapps/"
config_root = "/opt/xinluo/"
tom_config = "/data/tqlh_af/conf/"
def init_war():
	rm_job(webapps_root+'*')
	print "清空webapps"
	cp_job("/tmp/atrial_fibrillation.war",webapps_root+"af.war")
	file_info(webapps_root)

def update_config():
	cp_job(config_root+'server_noaf.xml',tom_config+'server.xml')
	print "更新配置文件server.xml"
	kill_tomcat()
	time.sleep(3)
	up_tomcat()
	time.sleep(15)
	cmd = "sudo sh /root/afconfig.sh"
	result = os.popen(cmd).read()
	print result
	cp_job(config_root+"server_noaf.xml",tom_config+'server.xml')
	kill_tomcat()
	time.sleep(3)
	up_tomcat()


if __name__ == '__main__':
	init_war()
	update_config()

	
	

