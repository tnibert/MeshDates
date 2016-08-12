from bs4 import BeautifulSoup
import urllib2

#def toUTC():

#class for making an ical calendar file
class Ical:
	def __init__(self, fname):
		self.f = open(fname, "w")
		self.f.write("BEGIN:VCALENDAR\nVERSION:2.0\n")
	def addEvent(self, time):
		self.f.write("BEGIN:VEVENT\n")
		self.f.write("DTSTART;VALUE=DATE:" + time + "\n")
		self.f.write("DTEND;VALUE=DATE:" + str(int(time)+1) + "\n")
		self.f.write("SUMMARY:MESH Meeting - check easthack.com\n")
		self.f.write("END:VEVENT\n")
	def close(self):
		self.f.write("END:VCALENDAR\n")
		self.f.close()


#initialize month hash table for converting to UTC
month = {}
month["January"] = "01"
month["February"] = "02"
month["March"] = "03"
month["April"] = "04"
month["May"] = "05"
month["June"] = "06"
month["July"] = "07"
month["August"] = "08"
month["September"] = "09"
month["October"] = "10"
month["November"] = "11"
month["December"] = "12"

#begin open web page
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
url = "http://easthack.com/meeting-dates/"
req = urllib2.Request(url, headers=hdr)
try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()
soup = BeautifulSoup(page, "lxml")
page.close()
#end open web page

#the following is for opening it as a local file
#if you are testing this offline with the html page, uncomment the next two lines and comment between the above begin and end lines
#with open("mesh.html", "r") as mesh:
#	soup = BeautifulSoup(mesh, "lxml")

table = soup.find("table")
tr_list = table.find_all("tr")		#divide each entry into list elements

cal = Ical("meshdates.ics")

for elem in tr_list:
	monthday = elem.find().find_next()
	year = monthday.find_next()
	monthandday = monthday.string.split()
	print monthandday[0] + " " + monthandday[1] + " " + year.string
	if len(monthandday[1]) == 1:
		monthandday[1] = "0" + monthandday[1]
	cal.addEvent(year.string + "" + month[monthandday[0]] + monthandday[1]) #year + month + day

cal.close()

#ok, so
#time has to be in UTC format for australia eastern standard time but we have to account for daylight savings time
#
