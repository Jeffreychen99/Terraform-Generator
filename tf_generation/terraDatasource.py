from util.tf_util import *

class Datasource:

	tags = {}
	name = ""
	datasource_type = ""

	arguments = {}

	def __init__(self, name, datasource_type, arguments):
		self.name = name
		self.datasource_type = datasource_type

		self.arguments = arguments

	def addArgument(self, key, value):
		arguments[key] = value

	def removeArgument(self, key, value):
		arguments.pop(key)

	def addTag(self, key, value):
		tags[key] = value

	def removeTag(self, key):
		tags.pop(key)

	def checkRequiredArgs(self):
		# DO THIS USING HTML PARSING
		required = []
		for i in required:
			if i not in self.arguments:
				return False
		return True

	def getString(self):
		currdir = os.getcwd()
		resources_tf = open("datasource.tf", "w")
		resources_tf.write('datasource "' + self.datasource_type + '" "' + self.name + '" { \n')
		for arg in arguments.keys():
			resources_tf.write('    ' + arg +  ' = "' + arguments[arg] + '" \n')

		if len(tags.keys()) > 0:
			resources_tf.write('\n     tags = { \n')
			for tag in tags.keys():
				resources_tf.write('        ' + tag +  ' = "' + tags[tag] + '" \n')
			resources_tf.write('     } \n')
		resources_tf.write('} \n')











