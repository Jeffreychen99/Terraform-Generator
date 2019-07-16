from util.tf_util import *

class Resource:

	tags = {}
	name = ""
	resource_type = ""

	arguments = {}

	def __init__(self, name, resource_type, arguments):
		self.name = name
		self.resource_type = resource_type

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

	def tf_string(self):
		resource_string = ""
		resource_string += 'resource "' + self.resource_type + '" "' + self.name + '" { \n'
		for arg in arguments.keys():
			resource_string += '    ' + arg +  ' = "' + arguments[arg] + '" \n'

		if len(tags.keys()) > 0:
			resource_string += '\n     tags = { \n'
			for tag in tags.keys():
				resource_string += '        ' + tag +  ' = "' + tags[tag] + '" \n'
			resource_string += '     } \n'
		resource_string += '} \n'

		return resource_string











