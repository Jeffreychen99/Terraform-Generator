from bs4 import BeautifulSoup
import requests

def getProviderList():
	return []

def getResourceList(provider):
	url = 'https://www.terraform.io/docs/providers/' + provider + '/index.html'
	soup  = BeautifulSoup(requests.get(url).text, features="html.parser")

	resources = []
	for li in soup.find_all('li'):
		for ul in li.find_all("ul"):
			for a in ul.find_all("a", href=True):
				if '/r/' in a['href']:
					url = a['href']
					resources.append(url[url.index("/r/") + 3:url.index(".html")])
	return resources

def getDatasourceList(provider):
	url = 'https://www.terraform.io/docs/providers/' + provider + '/index.html'
	soup  = BeautifulSoup(requests.get(url).text)

	soup = getResourceList('aws')
	datasources = []
	for li in soup.find_all('li'):
		for ul in li.find_all("ul"):
			for a in ul.find_all("a", href=True):
				if '/d/' in a['href']:
					datasources.append(a['href'])
	return datasources