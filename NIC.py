from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import json


def name(soup):
	name = soup.find("span", attrs={"id":"lblNm_lgl"})
	if name is None:
		print "NO NAME FOUND"
	return name.text.strip()


def regulator(soup):
	status = soup.find("a", attrs={"id":"hyplnkPrim_Fed_Reg_Txt"})
	if status is None:
		return "Not regulated"
	else:
		return status.text

def address(soup):
	line1 = soup.find("span", attrs={"id":"lblStreet_Line1"})
	if line1 is not None:
		return line1.text
	return "NO ADDRESS FOUND"

def scrape(id):
	url = "https://www.ffiec.gov/nicpubweb/nicweb/InstitutionProfile.aspx?parID_Rssd="+ str(id) + "&parDT_END=99991231"
	driver = webdriver.Chrome('/Users/Maddie/EXOStfp/chromedriver')
	driver.get(url)
	time.sleep(1)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	data = {}
	data["Legal Name"] = name(soup)
	data["Approval Status"] = regulator(soup)
	data["Legal Address"] = address(soup)
	return data


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v"
# scrape("1383951")
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"

