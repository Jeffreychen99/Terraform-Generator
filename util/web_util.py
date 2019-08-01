from bs4 import BeautifulSoup
import requests

def getProviderList():
	return []

def getResourceList(provider):
	url = 'https://www.terraform.io/docs/providers/' + provider + '/index.html'
	soup = BeautifulSoup(requests.get(url).text, features="html.parser")

	resources = []
	for li in soup.find_all('li'):
		for ul in li.find_all("ul"):
			for a in ul.find_all("a", href=True):
				if '/r/' in a['href']:
					url = a['href']
					resources.append(url[url.index("/r/") + 3:url.index(".html")])
	resources = list( dict.fromkeys(resources) )
	return resources

def getResourceArgs(provider, resource):
	url = 'https://www.terraform.io/docs/providers/' + provider + '/r/' + resource + '.html'
	print(url)
	soup = BeautifulSoup(requests.get(url).text, features="html.parser")
	args = []

	inner = soup.find("div", {"id":"inner"} )
	argsRef = inner.find("ul").find_all("li")
	for a in argsRef:
		print(a)
		print("*****************************")
		if "Required" in str(a):
			argName = str( a.find("code") )
			print(argName)
			argName = argName[argName.index(">") + 1:]
			argName = argName[:argName.index("<")]
			args.append(argName)

	args = list( dict.fromkeys(args) )

	return args





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