#!C:\Program Files\Python36\python.exe
# -*- coding: iso-8859-15 -*-

#imports
import json
import subprocess
import threading

#Headererror umgehen - cgi Problem?
print('''
''')

#Multithreading Ping Klasse
class mtPing(threading.Thread):
    """Ping Class for Multithreading"""

    pingtime = False
    host = False
    server = False

    def __init__(self, server, host, packagesize=4, countofpings=4, timelimit=4000):
        self.cmd = "ping " + str(host) +" -n " + str(countofpings) + " -l " + str(packagesize) + " -w " + str(timelimit)
        self.host = host
        self.server = server

    def run(self):
        self.ping()

    def ping(self):
        subprocessObj = subprocess.Popen(self.cmd,stdout=subprocess.PIPE,shell=True)
        (out, err) = subprocessObj.communicate()
        self.fetchPing(out)

    def fetchPing(self, unfetchedPing):

        def fetchPingOut(bytes_bitfetched):
            str_ping = ""
            str_bitfetched = bytes_bitfetched.decode("utf-8")
            for i in str_bitfetched:
                if i.isdigit():
                    str_ping = str_ping + str(i)
            return int(str_ping)

        searchstr = "Mittelwert = " #lenght
        lensearchstr = len(searchstr)
        offline = False
        onepingFailed = False

        first = unfetchedPing.find(bytes(searchstr, 'UTF-8'))
        if first == -1:
            offline = True
            self.pingtime = "offline"
            return "offline"

        bitfetched = unfetchedPing[first+lensearchstr:first+(lensearchstr+6)]
        ping1st = fetchPingOut(bitfetched)


        second = unfetchedPing[first+13:].find(bytes(searchstr, 'UTF-8'))
        if second == -1:
            onepingFailed = True

        if onepingFailed == False:
            bitfetched = unfetchedPing[second+lensearchstr:second+lensearchstr+6]
            ping2nd = fetchPingOut(bitfetched)
        else:
            ping2nd = ping1st

        #pingaverage
        pingaverage = (ping1st + ping2nd)/2
        self.pingtime = pingaverage

def jsonBuilder(pingThreadsList, dataJSON):
    #pingtime, host, server

    pattern = '''
        "musterservername": {
            "ip": "musterip",
            "pingtime": "musterpingtime",
            "hmlvalue": "musterhmlvalue"
        }'''

    jsonstr = '{'
    maxcount = len(pingThreadsList)-1

    for count, mtPingObj in enumerate(pingThreadsList):
        jsonstr += pattern #eq s = s + j

        if count < maxcount:
            jsonstr = jsonstr + ","

        high = dataJSON[str(mtPingObj.server)]["high"]
        medium = dataJSON[str(mtPingObj.server)]["medium"]
        low = dataJSON[str(mtPingObj.server)]["low"]

        if mtPingObj.pingtime != "offline":
            if int(low) >= mtPingObj.pingtime:
                hmlvalue = "LOW"
            elif int(medium) >= mtPingObj.pingtime:
                hmlvalue = "MEDIUM"
            else:
                hmlvalue = "HIGH"
        else:
            hmlvalue = "OFFLINE"

        jsonstr = jsonstr.replace("musterservername", str(mtPingObj.server))
        jsonstr = jsonstr.replace("musterip", str(mtPingObj.host))
        jsonstr = jsonstr.replace("musterpingtime", str(mtPingObj.pingtime))
        jsonstr = jsonstr.replace("musterhmlvalue", str(hmlvalue))

    jsonstr += "\n }"

    return jsonstr

def main():
    data = json.load(open('servers.json'))

    pingThreads = []

    for x in data:
        pingThread = mtPing(server=x, host=data[x]["ip"], packagesize=4, countofpings=2, timelimit=2000)
        pingThread.run()
        pingThreads.append(pingThread)

    #Erst Aufrufen wenn Pings abgeschlossen sind
    returnjson = jsonBuilder(pingThreadsList=pingThreads, dataJSON=data)

    print(returnjson)

#--------------------------------------------------------------------------------#
main()
