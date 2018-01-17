#!C:\Program Files\Python36\python.exe
# -*- coding: iso-8859-15 -*-

#imports
import json
import cgi

#Headererror umgehen - cgi Problem?
print('''
''')

def show():
    dataJSON = json.load(open('servers.json'))
    print(json.dumps(dataJSON))

def add(servername, ip, low, medium, high):

    def addBetweenPos1andPos2(string, added, pos1, pos2):
        return string[:pos1] + added + string[pos2:]



    dataJSON = json.load(open('servers.json'))
    data = json.dumps(dataJSON)

    pattern = '''
    "musterservername": {
        "ip": "musterip",
        "low": "musterlow",
        "medium": "mustermedium",
        "high": "musterhigh"
    },'''

    added = pattern
    added = added.replace("musterservername", servername)
    added = added.replace("musterip", ip)
    added = added.replace("musterlow", low)
    added = added.replace("mustermedium", medium)
    added = added.replace("musterhigh", high)

    onetime = True
    for pos, char in enumerate(data):
        if char == "{" and onetime == True:
            onetime = False
            data = addBetweenPos1andPos2(data, added, pos+1, pos+1)
            break;

    with open('servers.json', 'w') as file:
        file.write(data)
        print("successful")

def delete(servername):
    data = json.load(open('servers.json'))

    jsonstr = json.dumps(data);

    deleted = " "
    delfrom = jsonstr.find('"' + servername[0] + '"')

    startdel = False
    enddel = 0
    if delfrom != -1:
        for count, char in enumerate(jsonstr):
            if enddel == 1 or enddel == 2:
                if char == ",":
                    enddel += 1
                    continue
                elif char == '"' or char == "}":
                    enddel += 1
                    deleted += char
                    continue

            if startdel == True:
                if char == "}":
                    if enddel < 2:
                        enddel += 1
                    startdel = False
                    continue
                else:
                    continue
            if count == delfrom:
                startdel = True
            else:
                deleted += char
    else:
        print("Error")
        print(delfrom)
        return

    for i, c in enumerate(reversed(deleted)):
        if list(deleted)[-i-2] == '"':
            break;
        if c  == ",":
            deleted = list(deleted)
            deleted.pop(-i-1)
            deletedstr = ''.join(str(e) for e in deleted)
            deleted = deletedstr
            break

    print(list(deleted)[-2])

    #Save json
    print("successful")
    with open('servers.json', 'w') as file:
        file.write(deleted)

def main():
    serversJSON = json.load(open('servers.json'))
    dataPOST = cgi.FieldStorage()

    controller = dataPOST.getlist("choose")
    if "show" in controller:
        show()

    elif "delete" in controller:
        servername = dataPOST.getlist("servername")
        delete(servername)
        print("servername")

    elif "add" in controller:
        servername = dataPOST.getlist("servername")
        ip = dataPOST.getlist("ip")
        low = dataPOST.getlist("low")
        medium = dataPOST.getlist("medium")
        high = dataPOST.getlist("high")
        add(servername[0], ip[0], low[0], medium[0], high[0])

#------------------------------------------------------
main()
