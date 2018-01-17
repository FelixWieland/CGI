#!C:\Program Files\Python36\python.exe
# -*- coding: iso-8859-15 -*-

# Autor: Felix Wieland
# Datum: 05.01.2018

#imports
import json
import subprocess
import threading
import cgi
import requests
from bs4 import BeautifulSoup

#Headererror umgehen - cgi Problem?
print('''
''')

def getHTMLPROXER(id):

  url = "proxer.me/info/" + id
  param = dict()
  doc = requests.get(url, param).text
  soup = BeautifulSoup(doc, 'html.parser')
  data = {}

  tds = soup.find_all('td')
  return tds

  add = false
  name = false
  for td in tds:
    if add == true:
      data[name] = td
      add = false
      name = false

    if "Orginal Titel" in td:
      add = true
      name = "OrgTitel"

    if "Englischer Titel" in td:
      add = true
      name = "EngTitel"

    if "Genre" in td:
      add = true
      name = "Genre"

  return data

def main():
  dataPOST = cgi.FieldStorage()
  id = dataPOST.getlist("id")
  page = dataPOST.getlist("page")
  if page[0] == "PROXER":
    print(getHTMLPROXER(id[0]))

###############
main()
