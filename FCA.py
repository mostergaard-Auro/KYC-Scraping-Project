from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import json


def name(soup):
	name = soup.find("h1", attrs={"class":"RecordName"})
	if name is None:
		print "NO NAME FOUND"
	return name.text.strip()


def regulator(soup):
	status = soup.find("span", attrs={"class":"statusbox"})
	if status is None:
		return "Not regulated"
	else:
		return status.text.strip()

def address(soup):
	line = soup.findAll("span", attrs={"class":"addressline"})
	if line is not None: 	
		print line[0].text.strip() 
		print line[1].text.strip() 
		print line[4].text.strip() 
		print line[7].text.strip() 
		data = {}
		data["Legal Address Line 1"] = line[0].text.strip()
		data["Legal Address Line 2"] =  line[1].text.strip()
		data["Legal Address Line 3"] =  line[4].text.strip()
		data["Legal Address Line 4"] =  line[7].text.strip()
		return data
		

def scrape(id):
	url = "https://register.fca.org.uk/ShPo_FirmDetailsPage?id=" + str(id)
	driver = webdriver.Chrome('/Users/Maddie/EXOStfp/chromedriver')
	driver.get(url)
	time.sleep(1)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	print "Name:"
	print name(soup)
	print "Regulator:"
	print regulator(soup)
	print "Address:"
	print address(soup)
	# data = {}
	# data["Legal Name"] = name(soup)
	# data["Approval Status"] = regulator(soup)
	# data["Legal Address"] = address(soup)
	# return data


print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v"
scrape("001b000000MfsgwAAB")
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"

