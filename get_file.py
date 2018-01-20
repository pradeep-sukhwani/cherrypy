# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import mechanize
import os.path
import zipfile

def get_zip_file():
    parent_url = "http://www.bseindia.com/markets/equity/EQReports/BhavCopyDebt.aspx?expandable=3&utm_campaign=website&utm_source=sendgrid.com&utm_medium=email"
    child_url = "http://www.bseindia.com/markets/equity/EQReports/Equitydebcopy.aspx"
    soup = BeautifulSoup(urllib2.urlopen(child_url).read())
    file_url = soup.find('form', {"id": "form1"}).find("table").find("tr").find("td").find("table").find_all("tr")[1].find("td").find("table").find("tr").find("td").find("ul").find("li").find("a")["href"]
    br = mechanize.Browser()
    return br.retrieve(str(file_url), "stock_file.zip")[0]

def load_zip_data_in_redis():
    get_zip_file()
    if os.path.isfile("stock_file.zip"):
        zip_ref = zipfile.ZipFile("stock_file.zip", 'r')
        zip_ref.extractall("/home/pradeep/Desktop")
        os.remove("stock_file.zip")
        print "Retrieved the file with name: {0}".format(zip_ref.namelist()[0])
        return None

load_zip_data_in_redis()
