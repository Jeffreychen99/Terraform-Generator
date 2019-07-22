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
		for arg in self.arguments.keys():
			resource_string += '    ' + arg +  ' = "' + self.arguments[arg] + '" \n'

		if len(self.tags.keys()) > 0:
			resource_string += '\n     tags = { \n'
			for tag in self.tags.keys():
				resource_string += '        ' + tag +  ' = "' + self.tags[tag] + '" \n'
			resource_string += '     } \n'
		resource_string += '} \n'

		return resource_string











