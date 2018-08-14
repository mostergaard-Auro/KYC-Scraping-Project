from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time


def name(soup):
	name = soup.find("title").text
	if checkForApproval(soup) == "Not regulated":
		return ""
	return name.rstrip(" - BrokerCheck")


def checkForApproval(soup):
	status = soup.find("bc-legend", attrs={"title":"Brokerage Firm"})
	if status is None:
		return "Not regulated"
	else:
		# return status.text.strip()
		return "Regulated"

def legalAddress(soup):
	line1 = soup.find("div", attrs={"ng-bind":"vm.data.getMainAddress().addressLineStreet1"})
	line2 = soup.find("div", attrs={"ng-bind":"vm.data.getMainAddress().addressLineStreet2"})
	line3 = soup.find("div", attrs={"ng-bind":"vm.data.getMainAddress().addressLineCityStateZip"})
	if line1 is not None:
		data = {}
		data["Legal Address Line 1"] = line1.text.strip()
		data["Legal Address Line 2"] =  line2.text.strip()
		data["Legal Address Line 3"] =  line3.text.strip()
		return data

def scrape(id):
	url = "https://brokercheck.finra.org/firm/summary/"+ str(id)
	driver = webdriver.Chrome('/Users/Maddie/EXOStfp/chromedriver')
	driver.get(url)
	time.sleep(10)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	data = {}
	data["Legal Name"] = name(soup)
	data["Approval Status"] = checkForApproval(soup)
	data["Legal Address"] = legalAddress(soup)
	return data


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v"
# scrape("15794")
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"

