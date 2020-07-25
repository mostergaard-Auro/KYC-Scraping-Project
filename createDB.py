import sqlite3
import json
###ONE TIME USE TO CREATE THE DATABASE AND TABLES


db = sqlite3.connect("data/DB.db")
c = db.cursor()

mainList = "CREATE TABLE IF NOT EXISTS KYC_Client_Main_List(exosID INTEGER, client STRING, EDGAR STRING, FDIC STRING, FINRA STRING, GMEI STRING, NIC STRING, SEC STRING, active BOOLEAN);"
c.execute(mainList)

scraperLog = "CREATE TABLE IF NOT EXISTS Scraper_Log(logID INTEGER, exosID INTEGER, tStamp TIME, data BLOB);"

alertLog = "CREATE TABLE IF NOT EXISTS Alert_Log(exosID INTEGER, tStamp TIME, alert BLOB, reviwed BOOLEAN, addressed BOOLEAN);"
c.execute(alertLog)

db.commit()
db.close()
