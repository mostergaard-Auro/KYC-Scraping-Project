from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
from pprint import pprint
import json


def name(soup):
	name = soup.find("strong", attrs={"class":"legalNameStyle"})
	if name is not None:
		return name.text


def checkForApproval(soup):
	status = soup.find("div", attrs={"class":"col-md-8 col-sm-8"})
	if status is not None:
		return status.text.strip()

def legalAddress(soup):
	line1 = soup.findAll("div", attrs={"class":"break-word"})
	if line1 is list:
		data = {}
		data["Legal Address Line 1"] = line1[1].text
		data["Legal Address Line 2"] =  line1[2].text
		data["Legal Address Line 3"] =  line1[3].text
		data["Legal Address Line 4"] =  line1[0].text + soup.findAll("span")[81].text + soup.findAll("span")[82].text
		return data

def headquarterAddress(soup): 
	line1 = soup.findAll("div", attrs={"class":"break-word"})
	line2 = soup.findAll("span", attrs={"class":"break-word"})
	if line1 is list:
		data = {}
		data["Headquarter Address Line 1"] =  line1[5].text
		data["Headquarter Address Line 2"] =  line2[2].text + soup.findAll("span")[85].text + soup.findAll("span")[86].text
		return data

def scrape(id):
	url = "https://www.gmeiutility.org/actions/RecordDetails/viewRecordDetails/"+ str(id)
	driver = webdriver.Chrome('/Users/Maddie/EXOStfp/chromedriver')
	driver.get(url)
	time.sleep(2)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	data = {}
	data["Legal Name"] = name(soup)
	data["Approval Status"] = checkForApproval(soup)
	data["Legal Address"] = legalAddress(soup)
	data["Headquarter Address"] = headquarterAddress(soup)
	return data


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
# scrape("720355843735711115")
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

