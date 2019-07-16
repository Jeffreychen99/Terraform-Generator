import os
import util.tf_util as tf_util

#################### Digital Ocean ####################

def init():
	tf_util.init()

def plan():
	plan_command = "terraform plan -out current_plan"
	plan_command += " -var do_token=/keys/token"
	plan_command += " -var pub_key=/keys/DO_key.pub"
	plan_command += " -var pvt_key=/keys/DO_key"
	plan_command += " -var ssh_fingerprint=/keys/DO_key.fingerprint"
	os.system(plan_command)

def apply():
	tf_util.apply()

#######################################################

def ssh_keygen(keyName, protocol):
	if not os.path.isdir(os.getcwd() + "/keys"):
		os.mkdir(os.getcwd() + "/keys")
	else:
		os.system("rm /keys/*")

	os.system("echo " + os.getcwd() + "/keys/" + keyName + " | ssh-keygen -t " + protocol)
	os.system("ssh-keygen -E md5 -lf " + os.getcwd() + "/keys/" + keyName + ".pub > temp_fingerprint")
	with open("temp_fingerprint") as temp_fingerprint:
		fp = temp_fingerprint.readline()
		fp = fp[fp.index(":") + 1:]
		fp = fp[:fp.index(" ")]
		fingerprint = open(os.getcwd() + "/keys/" + keyName + ".fingerprint", "w")
		fingerprint.write(fp)
		fingerprint.close()
	os.system("rm temp_fingerprint")





