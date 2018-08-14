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
	name = "BROKEN"
	if soup.find("div", attrs={"class":"renamedBank"}) is not None:
		name = soup.find("a", attrs={"tabindex":"132"})
	return name.text.strip()


def checkForApproval(soup):
	status = soup.find("span", attrs={"class":"active-status"})
	return status.text.strip()

def legalAddress(soup, url):
	myLink = soup.find('a', attrs={"tabindex":"132"})
	link =  myLink["href"]
	link = url + str(link)[2:]
	driver = webdriver.Chrome('/Users/Maddie/EXOStfp/chromedriver')
	driver.get(link)
	time.sleep(1)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	addy = soup.find('div', attrs={"id":"address"}).text.strip()
	return addy.lstrip("Headquarters:\n")


def scrape(id):
	url = "https://research.fdic.gov/bankfind/detail.html?bank="+ str(id)
	driver = webdriver.Chrome('/Users/Maddie/EXOStfp/chromedriver')
	driver.get(url)
	time.sleep(1)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	data = {}
	data["Legal Name"] = name(soup)
	data["Approval Status"] = checkForApproval(soup)
	data["Legal Address"] = legalAddress(soup, url.rstrip("detail.html?bank=" + str(id)))
	return data
	
	
	
	


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v"
# scrape("58979")
# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"



