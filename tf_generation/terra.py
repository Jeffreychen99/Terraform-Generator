from util.tf_util import *

class tf_variable:

	def __init__(self, name):
		self.name = name

class Terra:

	provider = ""
	resources = []
	datasources = []

	arguments = {}
	parameters = []

	def __init__(self, provider, arguments, params):
		self.provider = provider
		self.arguments = arguments
		self.parameters = params

	def checkRequiredArgs(self):
		# DO THIS USING HTML PARSING
		required = []
		for i in required:
			if i not in self.arguments:
				return False
		return True

	def tf_string(self):
		provider_string = ""
		for param in self.parameters:
			provider_string += 'variable "' + param + '" {} \n'
		provider_string += '\nprovider "' + self.provider + '" { \n'
		for arg in self.arguments:
			argValue = self.arguments[arg]
			if type(self.arguments[arg]) != tf_variable:
				provider_string += '    ' + arg + ' = "' + argValue + '" \n'
			else:
				provider_string += '    ' + arg + ' = var.' + argValue.name + ' \n'
		provider_string += '} \n'

		return provider_string























