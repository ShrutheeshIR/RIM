from flask import Flask, request, render_template,url_for
import datetime
import pyowm
import bs4
import sys
import imaplib
import getpass
import email
import datetime
import time
from email.header import Header, decode_header, make_header
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import dateutil.parser as parser
import os
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
app = Flask(__name__)
today = datetime.date.today()
def fun():
    owm = pyowm.OWM('f52800c11084928f857687ec9ef44b4f')
    observation = owm.weather_at_place("Bangalore,IN")
    w = observation.get_weather()
    wind = w.get_wind()
    temperature = w.get_temperature('celsius')
    dic={}
    dic['temp']=temperature
    dic['wind']=wind
    dic['humidity']=w.get_humidity()
    dic['rain']=w.get_rain()
    dic['clouds']=w.get_clouds()
    dic['icon']= "http://openweathermap.org/img/w/" + w.get_weather_icon_name() + ".png"
    return dic



def newsfunc():
    news_url="https://news.google.com/news/rss"
    Client=urlopen(news_url)
    xml_page=Client.read()
    Client.close()
    dic = []
    soup_page=soup(xml_page,"xml")
    news_list=soup_page.findAll("item")
    # Print news title, url and publish date
    for i,news in enumerate(news_list):
        if i>4:
            break
        dic1 = {}
        print(i)
        dic1['title'] = news.title.text
        dic1['link'] = news.link.text
        dic1['text'] = news.pubDate.text
        dic.append(dic1)

    return dic

@app.route("/")
def hello():
    print(datetime.datetime.now())
    now=datetime.datetime.now()
    returndict = {}
    returndict['date'] = str(today.strftime("%a %d %b"))
    ts = time.time()
    hours=now.hour

    returndict['time']  = str(datetime.datetime.fromtimestamp(ts).strftime('%I:%M %p'))
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    dic={}
    dic4=[]
    results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=5).execute()
    mssg_list = results['messages']
    for mssg in mssg_list:
        temp_dict = { }
        m_id = mssg['id'] # get id of individual message
        message = service.users().messages().get(userId='me', id=m_id).execute() # fetch the message using API
        payld = message['payload'] # get payload of the message
        headr = payld['headers'] # get header of the payload
        for one in headr: # getting the Subject
            if one['name'] == 'Subject':
                msg_subject = one['value']
                temp_dict['Subject'] = msg_subject
                dic['subject']=temp_dict['Subject']
            if one['name'] == 'From':
                msg_from = one['value']
                temp_dict['Sender'] = msg_from
                dic['sender']=temp_dict['Sender']
            else:
                pass
        dic4.append(temp_dict)



    weather=fun()
    print(dic4)
    newsdic=newsfunc()



    return render_template('mainpage.html', dict = returndict, dic2=weather, dic3= newsdic,dic6=dic4)




if __name__ == '__main__':
    app.run(debug=True)