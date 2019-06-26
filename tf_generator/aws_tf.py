import os
import util.tf_util as tf_util

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

def createProvider(region):
	currdir = os.getcwd()
	provider_tf = open("provider.tf", "w")
	provider_tf.write('variable "access_key" {} \n')
	provider_tf.write('variable "secret_key" {} \n\n')
	provider_tf.write('provider "aws" { \n')
	provider_tf.write('    region = "' + region + '" \n')
	provider_tf.write('    access_key = var.access_key\n')
	provider_tf.write('    secret_key = var.secret_key\n} \n')
	provider_tf.close()

def createResource(resource):
	currdir = os.getcwd()
	provider_tf = open("resource.tf", "w")
	provider_tf.write('resource "' + resource.resourceType + '" "' + resource.name + '" { \n')
	provider_tf.write('    ami = "' + resource.ami + '" \n')
	provider_tf.write('    instance_type = "' + resource.instanceType + '" \n')

	if provisioner != None:
		# TODO: figure out how to create custom provisioner and then generate TF code from python provisioner object
		provider_tf.write('\n    provisioner "' + provisioner.name + ' { \n')

	provider_tf.write('\n    tags = { \n')
	for k in resource.tags:
		provider_tf.write('        ' + k + " = \"" + resource.tags[k] + "\" \n")
	provider_tf.write('    } \n\n')

	provider_tf.write('} \n')
	provider_tf.close()

def createOutput(name, var_name):
	currdir = os.getcwd()
	provider_tf = open("output.tf", "w")
	provider_tf.write('output "' + name + '" { \n')
	provider_tf.write('    value = "' + var_name + '" \n} \n')
	provider_tf.close()

def storeKeys(access_key, secret_key):
	if not os.path.isdir(os.getcwd() + "/keys"):
		os.mkdir(os.getcwd() + "/keys")

	accessKey_file = open(os.getcwd() + "/keys/access_key", "w")
	accessKey_file.write(access_key)
	accessKey_file.close()

	secretKey_file = open(os.getcwd() + "/keys/secret_key", "w")
	secretKey_file.write(secret_key)
	secretKey_file.close()


###################################################

def checkValidPlan():
	return tf_util.checkValidPlan()







