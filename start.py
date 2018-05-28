import os
import time
import schedule

def init():
	os.system('mkdir sassapp_mongodbdata')
	os.system('mkdir sassapp_mysqldata')
	os.system('mkdir sassbank_mysqldata')
	os.system('docker swarm init')	

def deploy_stack(filename,stackname):
	os.system("docker stack deploy -c "+filename+" "+stackname)

def remove_stacks():
	os.system('docker stack rm sassapp')
	os.system('docker stack rm sassbank')
	time.sleep(5)	
	

def job1():
	print "Working hours"
	remove_stacks()
	deploy_stack("bank-config1.yml","sassbank")
	deploy_stack("app-config1.yml","sassapp")

def job2():
	print "Non-working hours"
	remove_stacks()
	deploy_stack("bank-config2.yml","sassbank")
	deploy_stack("app-config2.yml","sassapp")


if __name__ == "__main__":

	t= time.localtime()

	if t.tm_hour>10 and t.tm_hour<17:
		print "Working hours"
		deploy_stack("bank-config1.yml","sassbank")
		deploy_stack("app-config1.yml","sassapp")
	else:
		print "Non-working hours"
		deploy_stack("bank-config2.yml","sassbank")
		deploy_stack("app-config2.yml","sassapp")

	schedule.every().day.at("10:00").do(job1)
	schedule.every().day.at("17:00").do(job2)

	while 1:
	    schedule.run_pending()
	    time.sleep(1)
