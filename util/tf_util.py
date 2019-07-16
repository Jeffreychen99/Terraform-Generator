import os

def init():
	os.system("terraform init")

def plan():
	os.system("terraform plan -out current_plan")

def apply():
	os.system("terraform apply current_plan")
	os.system("rm current_plan")

#######################################################

def writeProvider(terra):
	currdir = os.getcwd()
	provider_tf = open("provider.tf", "w")
	provider_tf.write(terra.tf_string())
	provider_tf.close()

def writeResources(terra):
	currdir = os.getcwd()
	resource_tf = open("resources.tf", "w")

	for res in terra.resources:
		resource_tf.write(res.tf_string() + "\n")

	resource_tf.close()

def writeDatasources(terra):
	currdir = os.getcwd()
	datasource_tf = open("datasources.tf", "w")

	for ds in terra.datasources:
		datasource_tf.write(ds.tf_string() + "\n")

	datasource_tf.close()

#######################################################


def checkValidPlan():
	return os.path.isfile("provider.tf") and os.path.isfile("current_plan")








