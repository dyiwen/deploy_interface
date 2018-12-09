#!/usr/bin/env python
# -*-coding:utf8 -*-
import os
import time
import datetime
import re
import sys
import traceback

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


def show_line(func):
	def wrapper(*args,**kwargs):
		print "-"*80
		return func(*args,**kwargs)
	return wrapper

@show_line
def check_tomcat(pid_name):
	cmd = "sudo ps -ef | grep '{}bin/tomcat'".format(pid_name)
	result = os.popen(cmd).read()
	#print result 
	return result

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
def kill_tomcat(dirpath):
	cmd = "sudo sh {}bin/startup.sh stop".format(dirpath)
	result = os.popen(cmd).read()
	print result
	time.sleep(2)
	while True:
		if dirpath+"conf" in check_tomcat(dirpath):
			cmd = "sudo ps -ef | grep '%sbin/tomcat'|awk {'print $2'}"%dirpath
			print cmd
			pid_str = os.popen(cmd).read()
			xx = r'\d{3,5}'
			rex = re.compile(xx)
			pid = rex.findall(pid_str)[0]
			cmd_kill = "sudo kill {}".format(pid)
			result = os.popen(cmd_kill).read()
			print result
			print check_tomcat(dirpath)
		else:
			print "无特定tomcat进程"
			break

@show_line
def file_info(dir_root):
	for file_name in os.listdir(dir_root):
		file_path = os.path.join(dir_root,file_name)
		print str(file_name)+'   '+str(get_FileCreateTime(file_path))+"   "+str(get_FileSize(file_path))+"MB"

@show_line
def alter(file_,old_str,new_str):
	file_data = ""
	with open(file_,"r") as f:
		for line in f:
			if old_str in line:
				line = line.replace(old_str,new_str)
			file_data += line
	with open(file_,"w") as f:
		f.write(file_data)
		print "修改配置文件完成"

@show_line
def up_tomcat(dir_path):
	cmd = "sudo sh {}bin/startup.sh satrt".format(dir_path)
	result = os.popen(cmd).read()
	print result,"启动tomcat"

#-------------------------------------------------------------------------

def sys_argv():
	if len(sys.argv) < 2:
		print "\nUsage:\n  python deploy_app.py [options]\n"
		print "  --app_web    THIS IS THE PROGRAM FOR DEPLOYING APP.WEB PROJECT TO TESTY\n               发布app.web"
		print "  --app_job    THIS IS THE PROGRAM FOR DEPLOYING APP.JOB PROJECT TO TESTY\n               发布app.job"
		print "  --afc        THIS IS THE PROGRAM FOR DEPLOYING AFC PROJECT TO TESTY\n               发布afc"
		print "  --we_chat    THIS IS THE PROGRAM FOR DEPLOYING WE_CHAT PROJECT TO TESY\n               发布we_chat"
		print "  --aftmp      THIS IS THE PROGRAM FOR DEPLOYING AFTMP PROJECT TO TESY\n               发布afc+小程序"
		sys.exit()
	if sys.argv[1].startswith('--'):
		option = sys.argv[1][2:]

		if option == 'app_web':

			print "This is the program for deploying app.web project testy\n"
			root = "/data/xl_app_server/webapps/"
			pid_name = "/data/xl_app_server/"
			try:
				if os.path.exists(root+"xl_app_server.war"):
					rm_job(root+"*")
					print "清空webapps目录------DONE!"
				if os.path.exists("/tmp/web.war"):
					cp_job("/tmp/web.war",root+"xl_app_server.war")
					if os.path.exists(root+"xl_app_server.war"):
						print "移动文件：web.war---->xl_app_server.war-----DONE!"
					        file_info(root)
			except:
				traceback.print_exc()

			try:
				kill_tomcat(pid_name)
				check_tomcat(pid_name)
				up_tomcat(pid_name)
				check_tomcat(pid_name)
			except:
				traceback.print_exc()
                elif option == 'app_job':
			print 'This is the program for deploying app_job project to testy\n'
			root = "/data/xl_app_job_server/"
			pid_name = "java -jar xl_app_job_server.jar"
			try:
				if os.path.exists(root+"xl_app_job_server.jar"):
					rm_job(root+"xl_app_job_server.jar")
					print "删除之前的jar包------DONE!"
				if os.path.exists("/tmp/xl_app_job_server.jar"):
					cp_job("/tmp/xl_app_job_server.jar",root)
					if os.path.exists(root+"xl_app_job_server.jar"):
						print "移动文件：tmp/.jar---->xl_app_job_server/.jar-----DONE!"
						file_info(root)
			except:
				traceback.print_exc()

			try:
				kill_tomcat(pid_name)
				check_tomcat(pid_name)
				up_tomcat(pid_name)
				check_tomcat(pid_name)
			except:
				traceback.print_exc()


		elif option == "afc":
			print "This is the program for deploying afc project to testy\n"
			root = "/data/tqlh_af/webapps/"
			config_root = "/opt/xinluo/"
			pid_name = "/data/tqlh_af/"
			try:
				if os.path.exists(root+"af.war"):
					rm_job(root+"*")
					print "清空webapps目录------DONE!"
				if os.path.exists("/tmp/jenkins_tmp/atrial_fibrillation.war"):
					cp_job("/tmp/jenkins_tmp/atrial_fibrillation.war",root+"af.war")
					print "移动文件：atrial_fibrillation.war---->/webapps/-----DONE!"
					file_info(root)
				else:
					print "jenkins_tmp目录下没有该文件"
			except:
				traceback.print_exc()

			try:
				cp_job(config_root+'server_noaf.xml',pid_name+"conf/server.xml")
				print "更新配置文件server.xml"
				kill_tomcat(pid_name)
				check_tomcat(pid_name)
				time.sleep(3)
				up_tomcat(pid_name)
				time.sleep(15)
				cmd = "sudo sh /root/afconfig.sh"
				result = os.popen(cmd).read()
				print result
				cp_job(config_root+"server.xml",pid_name+"conf/server.xml")
				kill_tomcat(pid_name)
				check_tomcat(pid_name)
				time.sleep(3)
				up_tomcat(pid_name)
				print check_tomcat(pid_name)
			except:
				traceback.print_exc()

		elif option == "aftmp":
			root = "/data/aftmp/tqlh_af/webapps/"
			pid_name = "/data/aftmp/tqlh_af/"
			try:
				if os.path.exists(root+"af.war"):
					rm_job(root+"*")
					print "清空webapps目录-----DONE!"
				if os.path.exists("/tmp/jenkins_tmp/atrial_fibrillation.war"):
					cp_job("/tmp/jenkins_tmp/atrial_fibrillation.war",root+"af.war")
					print "移动文件: atrial_fibrillation.war------>/webapps/----DONE!"
					file_info(root)
				else:
					print "jenkins_tmp目录下没有该文件"
			except:
				traceback.print_exc()

			try:
				kill_tomcat(pid_name)
				check_tomcat(pid_name)
				time.sleep(2)
				up_tomcat(pid_name)
				time.sleep(15)
				while True:
					if os.path.exists(root+"af/WEB-INF/classes/elasticsearch.properties"):
						alter(root+"af/WEB-INF/classes/elasticsearch.properties","clusterHsotNameVsPorts.a.host_name=119.23.202.156","#clusterHsotNameVsPorts.a.host_name=119.23.202.156")
						alter(root+"af/WEB-INF/classes/elasticsearch.properties","#clusterHsotNameVsPorts.a.host_name=172.18.204.168","clusterHsotNameVsPorts.a.host_name=172.18.204.168")
						break
					else:
						time.sleep(1)
						print "正在修改es配置文件"
				kill_tomcat(pid_name)
				time.sleep(3)
				up_tomcat(pid_name)
				check_tomcat(pid_name)
			except:
				traceback.print_exc()


		elif option == "we_chat":
			print "This is the program for deploying we_chat project to testy\n"
			root = "/data/afc_wechat_server/webapps/"
			pid_name = "/data/afc_wechat_server/"
			try:
				if os.path.exists(root+"afc_wechat_server.war"):
					rm_job(root+"*")
					print "清空webapps目录------DONE!"
				if os.path.exists("/tmp/jenkins_tmp/afc_wechat_server.war"):
					cp_job("/tmp/jenkins_tmp/afc_wechat_server.war",root)
					print "移动文件：afc_wechat_server.war---->/webapps/-----DONE!"
					file_info(root)
			except:
				traceback.print_exc()

			try:
				kill_tomcat(pid_name)
				check_tomcat(pid_name)
				time.sleep(2)
				up_tomcat(pid_name)
				time.sleep(15)
				alter("/data/afc_wechat_server/webapps/afc_wechat_server/WEB-INF/classes/elasticsearch.properties","clusterHsotNameVsPorts.a.host_name=119.23.202.156","#clusterHsotNameVsPorts.a.host_name=119.23.202.156")
				alter("/data/afc_wechat_server/webapps/afc_wechat_server/WEB-INF/classes/elasticsearch.properties","#clusterHsotNameVsPorts.a.host_name=172.18.204.168","clusterHsotNameVsPorts.a.host_name=172.18.204.168")
				kill_tomcat(pid_name)
				time.sleep(3)
				up_tomcat(pid_name)
				check_tomcat(pid_name)
			except:
				traceback.print_exc()


if __name__ == '__main__':
	#init_war()
	#update_config()
	sys_argv()

	
	

