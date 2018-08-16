import sqlite3, EDGAR, FDIC, FINRA, GMEI, NIC, SEC, FCA, Beta
import json, selenium
from time import gmtime, strftime	
from datetime import date, timedelta
import pymysql, math

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ KYC_CLIENT_MASTER_LIST TABLE  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def addClient(params): # Params is a list of the exosID, and the IDs for the various sites to scrape. If a site is not needed, put "Null"
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	cmd = 'INSERT INTO KYC_Client_Master_List (exosID, client, EDGAR, FDIC, FINRA, GMEI, NIC, SEC, active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);' 
	c.execute(cmd, params)

	db.commit()
	db.close()

def removeClients(): 
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'DELETE FROM KYC_Client_Master_List;' 
	c.execute(cmd)

	db.commit()
	db.close()
	return

def removeClient(exosID): 
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'DELETE FROM KYC_Client_Master_List WHERE exosID = %s;' 
	c.execute(cmd, exosID)

	db.commit()
	db.close()
	return

def printClients():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM KYC_Client_Master_List;' 
	sel = c.execute(cmd)
	results = c.fetchall()
	for record in results:
		print record
		print ""
	db.commit()
	db.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SCRAPING & LOGGING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def scrapeAll():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = "SELECT * FROM KYC_Client_Master_List;"
	sel = c.execute(cmd)
	log = []
	results = c.fetchall()
	ctr = 0
	for record in results:
		if record[8]: # active?
			log.append(scrapeClient(record, db, c))
	logAll(log)
	db.commit()	
	db.close()
	
def logAll(log):
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = "SELECT MAX(logID) FROM Scraper_Log;"
	sel = c.execute(cmd)
	logNum = 0
	results = c.fetchall()
	for record in results:
		if record[0] != None:
			logNum = record[0]
	for entry in log:
		entry = [logNum + 1] + list(entry)
		c.execute('INSERT INTO Scraper_Log VALUES(%s,%s,%s,%s);', entry)
		logNum = logNum + 1
	db.commit()
	db.close()

def scrapeClient(client, db, c):
	data = {}
	if client[2] is not None:
		# print "calling EDGAR"
		data["EDGAR"] = EDGAR.scrape(client[2])
	if client[3] is not None:
		# print "calling FDIC"
		data["FDIC"] = FDIC.scrape(client[3])
	if client[4] is not None:
		# print "calling FINRA"
		data["FINRA"] = FINRA.scrape(client[4])
	if client[5] is not None:
		# print "calling GMEI"
		data["GMEI"] = GMEI.scrape(client[5])
	if client[6] is not None:
		# print "calling NIC"
		data["NIC"] = NIC.scrape(client[6])
	if client[7] is not None:
		# print "calling SEC"
		data["SEC"] = SEC.scrape(client[7])
	if client[9] is not None:
		# print "calling SEC"
		data["FCA"] = FCA.scrape(client[8])
	if client[10] is not None:
		# print "calling SEC"
		data["Beta"] = Beta.scrape(client[9])
	d = json.dumps(data)
	timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	log = (client[0], timestamp, str(d))
	return log

def printLog():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM Scraper_Log;' 
	sel = c.execute(cmd)
	print ""
	print "****** LOG ******"
	print ""
	results = c.fetchall()
	for record in results:
		print record
		print ""
	db.commit()
	db.close()

def clearLog(): 
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'DELETE FROM Scraper_Log;' 
	c.execute(cmd)

	db.commit()
	db.close()
	return

def clearAlertLog(): 
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'DELETE FROM Alert_Log;' 
	c.execute(cmd)

	db.commit()
	db.close()
	return

def addLog(entry):
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'INSERT INTO Scraper_Log Values(%s,%s,%s,%s);' 
	c.execute(cmd, entry)

	db.commit()
	db.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ INSPECTING SCRAPER_LOG FOR CHANGES  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def getListOfClients():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT exosID FROM KYC_Client_Master_List WHERE active=1;' 
	sel = c.execute(cmd)
	li = []
	results = c.fetchall()
	for record in results:
		li.extend(record)
	db.commit()
	db.close()
	return li

	
def changes():
	clientList = getListOfClients()
	log = []
	for client in clientList:
		if clientList == []:
			break
		db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
		c = db.cursor()
		cmd = 'SELECT * FROM Scraper_Log WHERE exosID = %s ORDER BY logID DESC LIMIT 2;' 
		sel = c.execute(cmd, str(client))
		results = c.fetchall()
		logs = []
		for record in results:
			logs.append(record)
		recordY = logs[1]
		record = logs[0]
		if recordY[0] != record[0]:
				if recordY[3] != record[3]: 
					nameFinder = json.loads(recordY[3])
					name = ""
					listOfRegs = ['EDGAR', 'FDIC', 'FINRA', 'GMEI', 'NIC', 'SEC', 'FCA', 'Beta']
					for regulator in listOfRegs:
						try: 
							name =  nameFinder[regulator]['Legal Name'] 
						except KeyError:
							pass
					log.append(searchForProblem(record, recordY, name))
				db.commit()
				db.close()
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	logAllAlerts(log)
	db.commit()
	db.close()
	return



def searchForProblem(newData, oldData, name):
	newLog = newData
	oldLog = oldData
	newData = json.loads(newData[3])
	oldData = json.loads(oldData[3])
	timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	params = [newLog[1], name, timestamp, "", {}, "n/a", False, "n/a", False]
	try: 
		if newData['EDGAR'] != oldData["EDGAR"]:
			data = {}
			if newData['EDGAR']['Legal Name'] != oldData['EDGAR']["Legal Name"]:
				params[3] = params[3] + "EDGAR found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['EDGAR']["Legal Name"], oldData['EDGAR']["Legal Name"])
			if newData['EDGAR']["Mailing Address"] != oldData['EDGAR']["Mailing Address"]:
				params[3] = params[3] + "EDGAR found a Mailing Address Change. "
				data["EDGAR"] = SFPHelperMailingAddress(newData['EDGAR']["Mailing Address"], oldData['EDGAR']["Mailing Address"])
			if newData['EDGAR']["Business Address"] != oldData['EDGAR']["Business Address"]:
				params[3] = params[3] + "EDGAR found a Business Address Change. "
				data["EDGAR"] = SFPHelperBusinessAddress(newData['EDGAR']["Business Addresss"], oldData['EDGAR']["Business Address"])
			params[4]["EDGAR"] = data
			# print params[2]
	except KeyError:
		pass
	try:
		if newData['FDIC'] != oldData["FDIC"]:
			data = {}
			if newData['FDIC']['Legal Name'] != oldData['FDIC']["Legal Name"]:
				params[3] = params[3] + "FDIC found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['FDIC']["Legal Name"], oldData['FDIC']["Legal Name"])
			if newData['FDIC']["Approval Status"] != oldData['FDIC']["Approval Status"]:
				params[3] = params[3] + "FDIC found an Approval Status Change. "
				data["Approval Status"] = SFPHelperApprovalStatus(newData['FDIC']["Approval Status"], oldData['FDIC']["Approval Status"])
			if newData['FDIC']["Legal Address"] != oldData['FDIC']["Legal Address"]:
				params[3] = params[3] + "FDIC found a Legal Address Change. "
				data["Legal Address"] = SFPHelperLegalAddress(newData['FDIC']["Legal Address"], oldData['FDIC']["Legal Address"])
			params[4]["FDIC"] = data
	except KeyError:
		pass
	try: 
		if newData['FINRA'] != oldData["FINRA"]:
			data = {}
			if newData['FINRA']['Legal Name'] != oldData['FINRA']["Legal Name"]:
				params[3] = params[3] + "FINRA found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['FINRA']["Legal Name"], oldData['FINRA']["Legal Name"])
			if newData['FINRA']["Approval Status"] != oldData['FINRA']["Approval Status"]:
				params[3] = params[3] + "FINRA found an Approval Status Change. "
				data["Approval Status"] = SFPHelperApprovalStatus(newData['FINRA']["Approval Status"], oldData['FINRA']["Approval Status"])
			if newData['FINRA']["Legal Address"] != oldData['FINRA']["Legal Address"]:
				params[3] = params[3] + "FINRA found a Legal Address Change. "
				data["Legal Address"] = SFPHelperLegalAddress(newData['FINRA']["Legal Address"], oldData['FINRA']["Legal Address"])
			params[4]["FINRA"] = data
	except KeyError:
		pass
	try: 
		if newData['NIC'] != oldData["NIC"]:
			data = {}
			if newData['NIC']['Legal Name'] != oldData['NIC']["Legal Name"]:
				params[3] = params[3] + "NIC found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['NIC']["Legal Name"], oldData['NIC']["Legal Name"])
			if newData['NIC']["Approval Status"] != oldData['NIC']["Approval Status"]:
				params[3] = params[3] + "NIC found an Approval Status Change. "
				data["Approval Status"] = SFPHelperApprovalStatus(newData['NIC']["Approval Status"], oldData['NIC']["Approval Status"])
			if newData['NIC']["Legal Address"] != oldData['NIC']["Legal Address"]:
				params[3] = params[3] + "NIC found Legal Address Change. "
				data["Legal Address"] = SFPHelperLegalAddress(newData['NIC']["Legal Address"], oldData['NIC']["Legal Address"])
			params[4]["NIC"] = data
	except KeyError:
		pass
	try: 
		if newData['GMEI'] != oldData["GMEI"]:
			data = {}
			if newData['GMEI']['Legal Name'] != oldData['GMEI']["Legal Name"]:
				params[3] = params[3] + "GMEI found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['GMEI']["Legal Name"], oldData['GMEI']["Legal Name"])
			if newData['GMEI']["Approval Status"] != oldData['GMEI']["Approval Status"]:
				params[3] = params[3] + "GMEI found an Approval Status Change. "
				data["Approval Status"] = SFPHelperApprovalStatus(newData['GMEI']["Approval Status"], oldData['GMEI']["Approval Status"])
			if newData['GMEI']["Legal Address"] != oldData['GMEI']["Legal Address"]:
				params[3] = params[3] + "GMEI found a Legal Address Change. "
				data["Legal Address"] = SFPHelperLegalAddress(newData['GMEI']["Legal Address"], oldData['GMEI']["Legal Address"])
			if newData['GMEI']["Headquarter Address"] != oldData['GMEI']["Headquarter Address"]:
				params[3] = params[3] + "GMEI found a Headquarter Address Change. "
				data["Headquarter Address"] = SFPHelperHeadquarterAddress(newData['GMEI']["Headquarter Address"], oldData['GMEI']["Headquarter Address"])
			params[4]["GMEI"] = data
	except KeyError:
		pass
	try: 
		if newData['SEC'] != oldData["SEC"]:
			data = {}
			if newData['SEC']['Legal Name'] != oldData['SEC']["Legal Name"]:
				params[3] = params[3] + "SEC found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['SEC']["Legal Name"], oldData['SEC']["Legal Name"])
			if newData['SEC']["Approval Status"] != oldData['SEC']["Approval Status"]:
				params[3] = params[3] + "SEC found an Approval Status Change. "
				data["Approval Status"] = SFPHelperApprovalStatus(newData['SEC']["Approval Status"], oldData['SEC']["Approval Status"])
			params[4]["SEC"] = data
	except KeyError:
		pass
	try: 
		if newData['FCA'] != oldData["FCA"]:
			data = {}
			if newData['FCA']['Legal Name'] != oldData['FCA']["Legal Name"]:
				params[3] = params[3] + "FCA found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['FCA']["Legal Name"], oldData['FCA']["Legal Name"])
			if newData['FCA']["Legal Address"] != oldData['FCA']["Legal Address"]:
				params[3] = params[3] + "FCA found a Legal Address Change. "
				data["FCA"] = SFPHelperMailingAddress(newData['FCA']["Legal Address"], oldData['FCA']["Legal Address"])
			if newData['FCA']["Approval Status"] != oldData['FCA']["Approval Status"]:
				params[3] = params[3] + "FCA found an Approgval Status Change. "
				data["FCA"] = SFPHelperBusinessAddress(newData['FCA']["Approval Status"], oldData['FCA']["Approval Status"])
			params[4]["FCA"] = data
	except KeyError:
		pass
	try: 
		if newData['Beta'] != oldData["Beta"]:
			data = {}
			if newData['Beta']['Legal Name'] != oldData['Beta']["Legal Name"]:
				params[3] = params[3] + "Beta found a Name Change. "
				data["Legal Name"] = SFPHelperLegalName(newData['Beta']["Legal Name"], oldData['Beta']["Legal Name"])
			if newData['Beta']["Legal Address"] != oldData['Beta']["Legal Address"]:
				params[3] = params[3] + "Beta found a Legal Address Change. "
				data["Beta"] = SFPHelperMailingAddress(newData['Beta']["Legal Address"], oldData['Beta']["Legal Address"])
			if newData['Beta']["Approval Status"] != oldData['Beta']["Approval Status"]:
				params[3] = params[3] + "Beta found an Approgval Status Change. "
				data["Beta"] = SFPHelperBusinessAddress(newData['Beta']["Approval Status"], oldData['Beta']["Approval Status"])
			params[4]["Beta"] = data
	except KeyError:
		pass
	params[4] = str(json.dumps(params[4]))
	return params

def SFPHelperLegalName(newLN, oldLN):
	data = {}
	data["Old Legal Name"] = oldLN
	data["New Legal Name"] = newLN
	return data

def SFPHelperMailingAddress(newMA, oldMA):
	data = {}
	data["Old Mailing Address"] = oldMA
	data["New Mailing Address"] = newMA
	return data

def SFPHelperBusinessAddress(newBA, oldBA):
	data = {}
	data["Old Business Address"] = oldBA
	data["New Business Address"] = newBA
	return data

def SFPHelperApprovalStatus(newAS, oldAS):
	data = {}
	data["Old Approval Status"] = oldAS
	data["New Approval Status"] = newAS
	return data

def SFPHelperLegalAddress(newLA, oldLA):
	data = {}
	data["Old Legal Address"] = oldLA
	data["New Legal Address"] = newLA
	return data

def SFPHelperHeadquarterAddress(newHA, oldHA):
	data = {}
	data["Old Headquarter Address"] = oldHA
	data["New Headquarter Address"] = newHA
	return data

def logAllAlerts(log):
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = "SELECT MAX(logID) FROM Alert_Log;"
	sel = c.execute(cmd)
	logNum = 0
	results = c.fetchall()
	for record in results:
		if record[0] != None:
			logNum = record[0]
	for entry in log:
		entry = [logNum + 1] + list(entry)
		db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
		c = db.cursor()
		cmd = 'insert into Alert_Log values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'	
		c.execute(cmd, entry)
		cmd = 'insert into Pending_Alerts values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'	
		c.execute(cmd, entry)
		logNum = logNum + 1
		print "logging..."
	db.commit()
	db.close()

def printAlertLog():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM Alert_Log;' 
	sel = c.execute(cmd)
	print ""
	print "****** Alert LOG ******"
	print ""
	ctr = 0
	results = c.fetchall()
	for record in results:
		print record
		print ""
	db.commit()
	db.close()

def addToAlertLog(entry):
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'INSERT INTO Alert_Log Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);' 
	c.execute(cmd, entry)
	cmd = 'INSERT INTO Pending_Alerts Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);' 
	c.execute(cmd, entry)

	db.commit()
	db.close()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SORTING ALERTS  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def updateAlertStatus():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM Pending_Alerts;' 
	sel = c.execute(cmd)
	ctr = 0
	results = c.fetchall()
	completed = []
	active = []
	for record in results:
		li = list(record)
		active.append(li)
		if li [-1] and li [-3]:
			completed.append(li)
	for entry in completed:
		c.execute('INSERT INTO Completed_Alerts VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', entry)
	for entry in active:
		li = list(entry)
		values = li[6:]
		values.append(li[0])
		logEntry = c.execute('UPDATE Alert_Log SET reviewer=%s, addressed=%s, secondReviewer=%s, done=%s WHERE logID = %s', values)
	for entry in completed:
		cmd = 'DELETE FROM Pending_Alerts where logID = %s'
		c.execute(cmd, entry[0]) 
	db.commit()
	db.close()

def clearPendingAlerts(): 
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'DELETE FROM Pending_Alerts;' 
	c.execute(cmd)

	db.commit()
	db.close()
	return

def clearCompletedAlerts(): 
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()

	cmd = 'DELETE FROM Completed_Alerts;' 
	c.execute(cmd)

	db.commit()
	db.close()
	return

def printPendingAlerts():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM Pending_Alerts;' 
	sel = c.execute(cmd)
	results = c.fetchall()
	print ""
	print "****** Pending_Alerts ******"
	print ""
	for record in results:
		print record
		print ""
	db.commit()
	db.close()

def printCompletedAlerts():
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM Completed_Alerts;' 
	sel = c.execute(cmd)
	results = c.fetchall()
	print ""
	print "****** Completed_Alerts ******"
	print ""
	for record in results:
		print record
		print ""
	db.commit()
	db.close()

def changePendingAlert(update):
	db = pymysql.connect(host='localhost',
                            user='maddie',
                            password='exostfp',
                            db='KYC_Scraping_DB')
	c = db.cursor()
	c.execute('UPDATE Pending_Alerts SET reviewer=%s, addressed=%s, secondReviewer=%s, done=%s WHERE logID = %s', update)
	db.commit()
	db.close()


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~v"

# removeClient()
# addClient([2, "Apple Inc", "0000320193", None, None, None, None, None, True])
# addClient([3, "BankUnited, National Association", None, "58979", None, None, None, None, True])
# addClient([4, "BNP PARIBAS SECURITIES CORP.", None, None, "15794", None, None, None, True])
# addClient([5, "Pacific Investment Management Company LLC", None, None, None, "720355843735711115", None, None, True])
# addClient([6, "MORGAN STANLEY SMITH BARNEY PRIVATE MANAGEMENT II LLC", None, None, None, None, None, "163747", True])
# printClients()
# clearLog()
# printClients()

scrapeAll() # <~~~~~~ NEEDED TO MAINTAIN SCRAPERS

# scrapeAll()
# printLog()
# clearAlertLog()
# clearPendingAlerts()
# clearCompletedAlerts()
# addToAlertLog((1, 22, 'PUTNAM INVESTMENT MANAGEMENT, LLC', '2018-08-09 20:26:06', 'GMEI found a Legal Address Change. ', '{"GMEI": {"Legal Address": {"New Legal Address": "Six PO Box Square Boston Massachusetts, 02109 United States", "Old Legal Address": "One Post Office Square Boston, Massachusetts, 02109 United States"}}}', 'n/a', 0, 'n/a', 0))
# addToAlertLog((2, 56, 'ABC Client', '2018-08-09 20:26:06', 'SEC found an Approval Status Change. ', '{"SEC": {"Approval Status": {"New Approval Status": "Revoked", "Old Approval Status": "Approved"}}}', 'n/a', 0, 'n/a', 0))
# addToAlertLog((3, 33, 'Sovereign Bank, National Association', '2018-08-09 20:26:06', 'FDIC found a Name Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Santander Bank, National Association", "Old Legal Name": "Sovereign Bank, National Association"}}}', 'n/a', 0, 'n/a', 0))
# addToAlertLog((4, 1, 'Banana Inc', '2018-07-22 20:26:06', 'FDIC found a Name Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Pear Co.", "Old Legal Name": "Banana Inc"}}}', 'maddie.ostergaard@exosfinancial.com', 1, 'oren.mor@exosfinancial.com', 1))
# addToAlertLog((5, 1, 'Banana Inc', '2018-07-22 20:26:06', 'FDIC found a Name Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Pear Co.", "Old Legal Name": "Banana Inc"}}}', 'maddie.ostergaard@exosfinancial.com', 1, 'n/a', 0))
# addLog([])

changes() # <~~~~~~ NEEDED TO MAINTAIN SCRAPERS

# printPendingAlerts()
# printAlertLog()
# changePendingAlert(['mads', 1, 'jill', 1, 1])
# changePendingAlert(['jill', 1, 'mads', 0, 2])

updateAlertStatus() # <~~~~~~ NEEDED TO MAINTAIN SCRAPERS

# printCompletedAlerts()
# printPendingAlerts()
# printAlertLog()


# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"


