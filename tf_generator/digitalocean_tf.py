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

def createProvider():
	currdir = os.getcwd()
	provider_tf = open("provider.tf", "w")
	provider_tf.write('variable "do_token" {} \n')
	provider_tf.write('variable "pub_key" {} \n')
	provider_tf.write('variable "pvt_key" {} \n')
	provider_tf.write('variable "ssh_fingerprint" {} \n\n')
	provider_tf.write('provider "digitalocean" { \n')
	provider_tf.write('    token = var.do_token \n} \n')
	provider_tf.close()

def createResource():
	pass

def generateKeys():
	tf_util.ssh_keygen("DO_key", "ecdsa")

def storeToken(token):
	if not os.path.isdir(os.getcwd() + "/keys"):
		os.mkdir(os.getcwd() + "/keys")
	token_file = open(os.getcwd() + "/keys/token", "w")
	token_file.write(token)
	token_file.close()

#######################################################

def checkValidPlan():
	return tf_util.checkValidPlan()






