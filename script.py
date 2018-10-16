import MySQLdb
from googlesearch import search
import requests
import urllib2
from bs4 import BeautifulSoup
import re
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def search2(g):
	now = datetime.datetime.now()
	q=" imdb "+g
	for j in search(q, tld="com", num=1, stop=1, pause=2):
		# f=open("2.txt","r")
		page=urllib2.urlopen(j)
		# source=f.read()
		source=page.read()
		h=source.find('season=')
		g=source[h-29:h+29]
		aa=g.find('/')
		ab=g[aa:]
		ac=ab.find('"')
		ad=ab[:ac]
		nex="https://www.imdb.com"+ad
		print nex
		page1=urllib2.urlopen(nex)
		s1=page1.read()
		match=re.findall(r'\d+\s\w\w\w.\s\d\d\d\d',s1)
		# print match
		name=[]
		epi=re.findall(r'<a\shref="\/\w+\/\w+\/\?\w+\_\=\w+\_\w+"\ntitle\=".*"\s',s1)
		for i in epi:
			g=i.split(r'"')
			if g[3] not in name:
				name.append(g[3])
		print name
		st=""
		if len(match)==0:
			hhh=source.find('year=')
			ggg=source[hhh+5:hhh+9]
			st+="next season begins in year "+ggg
			return st
		else:
			m=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
			date=now.day
			month=now.month
			year=now.year
			st=""
			i=0
			for mat in match:
				tem=mat.split(" ")
				dd=int(tem[0])
				md=tem[1][:3]
				yy=int(tem[2])
				mm=0
				for kk in range(len(m)):
					if m[kk] == md:
						mm=kk+1
						break
				# print dd,mm,yy
				if year==yy:
					if mm==month:
						if dd==date:
							st+="Episode name is : "+name[i]+"\n"+"next episode airs on "+str(yy)+"-"+str(mm)+"-"+str(dd)
							return st
						elif dd>date:
							st+="Episode name is : "+name[i]+"\n"+"next episode airs on "+str(yy)+"-"+str(mm)+"-"+str(dd)
							return st
					elif mm>month:
						st+="Episode name is : "+name[i]+"\n"+"next episode airs on "+str(yy)+"-"+str(mm)+"-"+str(dd)
						return st
				elif yy>year:
					st+="Episode name is : "+name[i]+"\n"+"next episode airs on "+str(yy)+"-"+str(mm)+"-"+str(dd)
					return st
				i=i+1
			return "No data found for further release date so far we believe that the show has finished streaming all its episodes"


def main():
	db=MySQLdb.connect('localhost','root','password','script')
	cursor=db.cursor()
	numberofmail=raw_input("Number of Users need to be entered: ")
	gg=0
	for i in range(int(numberofmail)):
		a=raw_input("Email address : ")
		b=raw_input("TV Series : ")
		query="select id from details ORDER BY id DESC LIMIT 1"
		cursor.execute(query)
		r=cursor.fetchall()
		for r1 in r:
			gg=int(r1[0])
		insert="insert into details(email,tvseries) values('%s','%s')"%(a,b)
		cursor.execute(insert)
		db.commit()
	query="select email,tvseries from details where id>='%d'"%(gg)
	cursor.execute(query)
	result=cursor.fetchall()
	print result
	for series in result:
		email=series[0]
		tvseries=series[1]
		# print tvseries
		tvseries=tvseries.split(',')
		sendmail=""
		print tvseries
		for t in tvseries:
			print t
			sendmail+="\n\nTV series name : '%s'"%(t)
			send=""
			send=search2(t)
			sendmail+="\nStatus : "+send
		print sendmail
		fromaddr = 'innovacer@gmail.com'  # Sender(Your) email adddress
		toaddrs  = email  # Receiver email address
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddrs
		msg['Subject'] = "TV-series"

		body = sendmail

		msg.attach(MIMEText(body, 'plain'))

		username = 'innovacer@gmail.com'  # Sender(Your) email address
		password = 'innovacer'  # Password of your email account
		server = smtplib.SMTP('smtp.gmail.com:587')  # Give your SMTP server. Here, i'm using gmail.
		server.ehlo()
		server.starttls()
		server.ehlo()

		server.login(username, password)
		text = msg.as_string()
		server.sendmail(fromaddr, toaddrs, text)

		server.close()
		print 'Successfully sent the mail !!!'
	db.close()
# def createtable():
# 	db=MySQLdb.connect('localhost','root','password','script')
# 	cursor=db.cursor()
# 	create="""create table details(
# 			id integer AUTO_INCREMENT PRIMARY KEY,
# 			email nvarchar(100),
# 			tvseries nvarchar(200))"""
# 	cursor.execute(create)
# 	db.close()

# createtable()
main()
