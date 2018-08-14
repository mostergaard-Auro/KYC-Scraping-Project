import sqlite3
import json
from time import gmtime, strftime	
from datetime import date, timedelta
import pymysql, math
db = pymysql.connect(unix_socket='/cloudsql/' + "kyc-scraping:us-central1:kyc-scraping-db",
                             user='maddie',
                             password='exostfp',
                             db='KYC_Scraping_DB')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Client Search  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def findClient(search):
	db = pymysql.connect(unix_socket='/cloudsql/' + "kyc-scraping:us-central1:kyc-scraping-db",
                             user='maddie',
                             password='exostfp',
                             db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM KYC_Client_Master_List;' 
	sel = c.execute(cmd)
	results = c.fetchall()
	findings = []
	for record in results:
		try:
			search = int(search)
			if record[0] == search:
				regulators = record[2:8]
				ctr = 0
				while ctr < 6:
					if regulators[ctr] != None:
						findings.append([exosIDToURL(regulators[ctr], ctr), record[1]])
					ctr += 1
		except:
			pass
		try:
			search = string(search)
			if record[1] == search:
				regulators = record[2:8]
				ctr = 0
				while ctr < 6:
					if regulators[ctr] != None:
						findings.append([exosIDToURL(regulators[ctr], ctr), record[1]])
					ctr += 1
		except:
			pass
	db.commit()
	db.close()
	if findings == []:
		return None
	else:
		return findings
		

def exosIDToURL(exosID, num):
	print "here"
	if num == 0:
		return "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+ str(exosID)
	if num == 1:
		return "https://research.fdic.gov/bankfind/detail.html?bank="+ str(exosID)
	if num == 2:
		return "https://brokercheck.finra.org/firm/summary/"+ str(exosID)
	if num == 3:
		return "https://www.gmeiutility.org/actions/RecordDetails/viewRecordDetails/"+ str(exosID)
	if num == 4:
		return "https://www.ffiec.gov/nicpubweb/nicweb/InstitutionProfile.aspx?parID_Rssd=" + str(exosID)
	if num == 5:
		return "https://www.adviserinfo.sec.gov/Firm/"+ str(exosID)
	


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ INSPECTING SCRAPER_LOG FOR CHANGES  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def getListOfClients():
	db = pymysql.connect(unix_socket='/cloudsql/' + "kyc-scraping:us-central1:kyc-scraping-db",
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

	'''
def findData(search):
	clientList = getListOfClients()
	log = []
	db = pymysql.connect(unix_socket='/cloudsql/' + "kyc-scraping:us-central1:kyc-scraping-db",
                             user='maddie',
                             password='exostfp',
                             db='KYC_Scraping_DB')
	c = db.cursor()
	cmd = 'SELECT * FROM Scraper_Log WHERE tStamp = %s ORDER BY logID DESC;' 
	sel = c.execute(cmd, str(client))
	results = c.fetchall()
	logs = []
	for record in results:
	for client in clientList:
		if clientList == []:
			break
		
			logs.append(record)
		recordY = logs[1]
		record = logs[0]
		if recordY[0] != record[0]:
				if recordY[3] != record[3]: 
					# print "No Changes"
					# print ""
					# print "~~~~~~~~~~"
				# else:
					nameFinder = json.loads(recordY[3])
					name = ""
					listOfRegs = ['EDGAR', 'FDIC', 'FINRA', 'GMEI', 'NIC', 'SEC']
					for regulator in listOfRegs:
						try: 
							name =  nameFinder[regulator]['Legal Name'] 
						except KeyError:
							pass
					log.append(searchForProblem(record, recordY, name))
						# print ""
						# print "~~~~~~~~~~"
				db.commit()
				db.close()
	
'''




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
# scrapeAll()
# scrapeAll()
# printLog()
# clearAlertLog()
# clearPendingAlerts()
# clearCompletedAlerts()

# addToAlertLog((1, 1, 'Banana Inc', '2018-07-25 20:26:06', 'FDIC found a Name Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Pear Co.", "Old Legal Name": "Banana Inc"}}}', 'n/a', 0, 'n/a', 0))
# addToAlertLog((2, 2, 'Orange Co', '2018-07-24 20:26:06', 'FDIC found a Legal Address Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Pear Co.", "Old Legal Name": "Banana Inc"}}}', 'n/a', 0, 'n/a', 0))
# addToAlertLog((3, 3, 'Strawberry Inc', '2018-07-23 20:26:06', 'FDIC found a Name Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Pear Co.", "Old Legal Name": "Banana Inc"}}}', 'n/a', 0, 'n/a', 0))
# addToAlertLog((4, 1, 'Banana Inc', '2018-07-22 20:26:06', 'FDIC found a Name Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Pear Co.", "Old Legal Name": "Banana Inc"}}}', 'maddie.ostergaard@exosfinancial.com', 1, 'oren.mor@exosfinancial.com', 1))
# addToAlertLog((5, 1, 'Banana Inc', '2018-07-22 20:26:06', 'FDIC found a Name Change. ', '{"FDIC": {"Legal Name": {"New Legal Name": "Pear Co.", "Old Legal Name": "Banana Inc"}}}', 'maddie.ostergaard@exosfinancial.com', 1, 'n/a', 0))
# changes2()

# printPendingAlerts()
# printAlertLog()

# changePendingAlert(['mads', 1, 'jill', 1, 1])
# changePendingAlert(['jill', 1, 'mads', 0, 2])
# updateAlertStatus()
# printCompletedAlerts()
# printPendingAlerts()
# printAlertLog()

 #print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^"


