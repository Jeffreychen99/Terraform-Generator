import os

def init():
	os.system("terraform init")

def plan():
	os.system("terraform plan -out current_plan")

def apply():
	os.system("terraform apply current_plan")
	os.system("rm current_plan")

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


def checkValidPlan():
	return os.path.isfile("provider.tf") and os.path.isfile("current_plan")

#######################################################

class Resource:

	name = ""
	resourceType = ""

	ami = ""
	instanceType = ""
	tags = {}
	provisioner = None

	def __init__(self, resourceName):
		self.name = resourceName


class Data:

	name = ""
	dataType = ""

	ami = ""
	instanceType = ""
	tags = {}
	provisioner = None

	def __init__(self, resourceName):
		self.name = resourceName








