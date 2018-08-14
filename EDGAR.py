from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import json


def name(soup):
	name = soup.find("span", attrs={"class":"companyName"})
	if name is not None: 
		name = str(name.text).split("CIK")[0]
		return name.strip()

def mailingAddress(soup):
	lines = soup.findAll("span", attrs={"class":"mailerAddress"})
	if lines is list:
		data = {}
		data["Mailing Address Line 1"] = lines[0].text.strip()
		data["Mailing Address Line 2"] = lines[1].text.strip()
		return data

def businessAddress(soup):
	lines = soup.findAll("span", attrs={"class":"mailerAddress"})
	if lines is list:
		data = {}
		data["Business Address Line 1"] = lines[2].text.strip()
		data["Business Address Line 2"] = lines[3].text.strip()
		return data

def scrape(id):
	url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+ str(id)
	driver = webdriver.Chrome('/Users/Maddie/EXOStfp/chromedriver')
	driver.get(url)
	time.sleep(2)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	data = {}
	data["Legal Name"] = name(soup)
	data["Mailing Address"] = mailingAddress(soup)
	data["Business Address"] = businessAddress(soup)
	return data


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v"
# scrape("0000320193")

# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"

