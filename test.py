import sqlite3
import json
from time import gmtime, strftime	
from datetime import date, timedelta
import pymysql, math

def addClient(newClient):
	db = pymysql.connect(unix_socket='/cloudsql/' + "kyc-scraping:us-central1:kyc-scraping-db",
                             user='maddie',
                             password='exostfp',
                             db='Corporate_Store_DB')
	c = db.cursor()
	cmd = 'insert into Client (exosID, client, amountLeft2018, amountLeft2019, amountLeft2020, amountLeft2021, amountLeft2022, amountLeft2023, amountLeft2024, amountLeft2025, amountLeft2026, amountLeft2027, amountLeft2028) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);' 
	sel = c.execute(cmd, newClient)
	db.commit()
	db.close()

def printClients():
	db = pymysql.connect(unix_socket='/cloudsql/' + "kyc-scraping:us-central1:kyc-scraping-db",
                             user='maddie',
                             password='exostfp',
                             db='Corporate_Store_DB')
	c = db.cursor()
	cmd = 'Select * from Client;' 
	sel = c.execute(cmd)
	results = c.fetchall()
	for record in results:
	 	print record
	 	print ""
	db.commit()
	db.close()

def removeClients():
	db = pymysql.connect(unix_socket='/cloudsql/' + "kyc-scraping:us-central1:kyc-scraping-db",
                             user='maddie',
                             password='exostfp',
                             db='Corporate_Store_DB')
	c = db.cursor()
	cmd = 'delete from Client;' 
	sel = c.execute(cmd)
	db.commit()
	db.close()


# removeClients()

# addClient([1,"Maddie Co.", 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100])
# addClient([2,"Oren Inc.", 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50])


printClients()