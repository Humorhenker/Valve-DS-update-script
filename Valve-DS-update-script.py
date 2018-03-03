#!/usr/bin/python
from urllib2 import Request, urlopen, URLError
from subprocess import call
import os
# insert your paths here
csgopath = "somewehere"
gmodpath = "somewhere"
csgo_steamcmdpath = "somewhere/steamcmd.sh"
gmod_steamcmdpath = "somewhere/steamcmd.sh"

valid = False
while not valid:
        antwort = raw_input("Which server do you want to check? (csgo,gmod) ")
        if antwort == 'csgo' or antwort == 'gmod':
                valid = True
if antwort == 'csgo':
        appid = 730
        file = open(csgopath + "/csgo/steam.inf","r")
elif antwort == 'gmod':
        appid = 4000
        file = open(gmodpath + "/garrysmod/steam.inf","r")
steaminf = file.read()
front = steaminf.find('PatchVersion=')
back = steaminf.find('\nProductName=')
version = steaminf[front+13:back]
version = version.replace(".", "")
url = "http://api.steampowered.com/ISteamApps/UpToDateCheck/v0001?appid=" + str(appid) + "&version=" + version
request = Request(url)

try:
        response = urlopen(request)
        ergebnis = response.read()
except URLError, e:
        print 'Webrequest error:', e
front = ergebnis.find("up_to_date")
back = ergebnis.find("version_is_listable")
uptodate = ergebnis[front+13:back-5]
if uptodate == 'true':
        print "Server (for " + str(appid) + ") is uptodate"
else:
        print "Server (for " + str(appid) + ") is NOT uptodate"
        valid = False
        while not valid:
                antwort = raw_input("Update now? (y,n) ")
                if antwort == 'y' or antwort == 'n':
                        valid = True
        if antwort == 'y':
                if appid == 730:
                        os.system("sudo " + csgo_steamcmdpath + " +login anonymous +force_install_dir " + csgopath + " +app_update 740 validate +quit")
                elif appid == 4000:
                        os.system("sudo " + gmod_steamcmdpath + " +login anonymous +force_install_dir " + gmodpath + " +app_update 4020 validate +quit")
