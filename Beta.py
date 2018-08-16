# import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time
import json


def name(soup):
	name = soup.find("p", attrs={"id":"company-name"})
	if name is None:
		print ("NO NAME FOUND")
	return name.text.strip()


def regulator(soup):
	status = soup.find("dd", attrs={"id":"company-status"})
	if status is None:
		return "Not regulated"
	else:
		return status.text.strip()

def address(soup):
	line = soup.findAll("dd", attrs={"class":"text data"})
	if line is not None: 	
		addressline1 = (line[0].text.strip())
		ext = ","
		addresslineone = addressline1[:addressline1.find(ext) + len(ext)]
		print (addresslineone)
		addressline2 = (line[0].text.strip())
		start = ", "
		end = ","
		addresslinetwo = ((addressline2.split(start))[1].split(end)[0])
		print(addresslinetwo)
		addresslinethree = (addressline1[addressline1.find(addresslinetwo)+len(addresslinetwo + ", "):addressline1.rfind(",")])
		print(addresslinethree)
		addresslinefour = (addressline1[addressline1.find(addresslinethree)+len(addresslinethree + ", "):])
		print(addresslinefour)
		data = {}
		data["Legal Address Line 1"] = addresslineone
		data["Legal Address Line 2"] = addresslinetwo
		data["Legal Address Line 3"] = addresslinethree
		data["Legal Address Line 4"] = addresslinefour
		return data
		

def scrape(id):
	url = "https://beta.companieshouse.gov.uk/company/" + str(id)
	driver = webdriver.Chrome('/Users/manavdhaliwal/desktop/pysandbox/selenium-3.14.0/selenium/webdriver/chromedriver')
	driver.get(url)
	time.sleep(1)
	html = driver.page_source
	driver.quit()
	soup = BeautifulSoup(html, "html.parser")
	# print ("Name:")
	# print (name(soup))
	# print ("Regulator:")
	# print (regulator(soup))
	# print ("Address:")
	# print (address(soup))
	data = {}
	data["Legal Name"] = name(soup)
	data["Approval Status"] = regulator(soup)
	data["Legal Address"] = address(soup)
	return data


# print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v")
# scrape("02263951")
# print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^")

