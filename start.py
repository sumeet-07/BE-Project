import os
import time
import schedule

def init():
	print "##### Creating Database Directories #####"
	os.system('mkdir /opt/sass')
	os.system('mkdir /opt/sass/sassapp_mongodbdata')
	os.system('mkdir /opt/sass/sassapp_mysqldata')
	os.system('mkdir /opt/sass/sassbank_mysqldata')
	print "##### Creating Database Directories Finished #####"
	print ""
	print "##### Creating Docker Swarm #####"
	os.system('docker swarm init')	
	print "##### Creating Docker Swarm Finished #####"

def deploy_stack(filename,stackname):
	print ""
	print "##### Deploying "+stackname+" stack #####"
	os.system("docker stack deploy -c "+filename+" "+stackname)
	print "##### Deploying "+stackname+" stack finished #####"

def remove_stacks():
	print ""
	print "##### Removing Stacks #####"
	os.system('docker stack rm sassapp')
	os.system('docker stack rm sassbank')
	time.sleep(5)	
	os.system('docker stack rm sassapp')
	os.system('docker stack rm sassbank')
	time.sleep(10)	
	print "##### Removing Stacks Finished #####"
	

def config1():
	remove_stacks()
	print ""
	print "##### Deploying working hours stack #####"
	deploy_stack("bank-config1.yml","sassbank")
	deploy_stack("app-config1.yml","sassapp")
	print "##### Deploying working hours stack Finished #####"

def config2():
	remove_stacks()
	print ""
	print "##### Deploying non-working hours stack #####"
	deploy_stack("bank-config2.yml","sassbank")
	deploy_stack("app-config2.yml","sassapp")
	print "##### Deploying non-working hours stack Finished #####"

if __name__ == "__main__":
	init()
	t= time.localtime()

	if t.tm_hour>10 and t.tm_hour<17:
		config1()
	else:
		config2()

	schedule.every().day.at("10:00").do(config1)
	schedule.every().day.at("17:00").do(config2)

	while 1:
	    schedule.run_pending()
	    time.sleep(1)
