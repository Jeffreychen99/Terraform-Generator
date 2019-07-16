import os
import util.tf_util as tf_util

from tf_generation.terra import *
from tf_generation.terraResource import *
from tf_generation.terraDatasource import *

####################### AWS #######################

def init():
	tf_util.init()

def plan():
	plan_command = "terraform plan -out current_plan"
	plan_command += " -var access_key=/keys/access_key"
	plan_command += " -var secret_key=/keys/secret_key"
	os.system(plan_command)

def apply():
	tf_util.apply()

###################################################

def storeKeys(access_key, secret_key):
	if not os.path.isdir(os.getcwd() + "/keys"):
		os.mkdir(os.getcwd() + "/keys")

	accessKey_file = open(os.getcwd() + "/keys/access_key", "w")
	accessKey_file.write(access_key)
	accessKey_file.close()

	secretKey_file = open(os.getcwd() + "/keys/secret_key", "w")
	secretKey_file.write(secret_key)
	secretKey_file.close()







