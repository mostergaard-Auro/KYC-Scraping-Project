import urllib2
from bs4 import BeautifulSoup
import json
import time


def approvedCheck(soup):
	table = soup.table.find(id="tbRegStatus")
	if table is None:
		return "Not currently registered"
	# print table.prettify()
	else:
		for row in table.findAll("tr")[1:]:
			status = row.findNext("td").findNext("td").text
			if row.findNext("td").text == "SEC":
				return status + " by the SEC"
			else:
				return status + " at the state level"


def name(soup):
	legalName = soup.find(id="ctl00_cphMain_landing_lblActiveOrgName")
	if legalName is not None:
		return legalName.text


def scrape(id):
	url = "https://www.adviserinfo.sec.gov/Firm/" + str(id)
	page = urllib2.urlopen(url)
	time.sleep(1)
	soup = BeautifulSoup(page, "html.parser")
	data = {}
	data['Legal Name'] = name(soup)
	data['Approval Status'] = approvedCheck(soup)
	return data

# print "~~~~~~~~~~~~~~~~~~~~~~~~~"
# scrape("163747")
# print "~~~~~~~~~~~~~~~~~~~~~~~~~"



