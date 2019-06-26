from bs4 import BeautifulSoup
import requests

def getProviderList():
	return []

def getResourceList(provider):
	url = 'https://www.terraform.io/docs/providers/' + provider + '/'
	soup  = BeautifulSoup(requests.get(url).text)
	return soup
	#print(soup.body.)