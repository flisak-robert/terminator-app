#!/usr/bin/python3

from flask import Flask, render_template
import deathbycaptcha
import array
from flask import Flask, render_template
import random
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import ReplyKeyboardRemove,ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator
import requests
import re
from bs4 import BeautifulSoup
import sys
from binascii import a2b_base64

app = Flask(__name__)

@app.route("/")
#def index():
#    return render_template('index.html', my_list=[0,1,2,3,4,5,6,7,8,9,100,101])
def index():
    user = {'username': 'Robert'}
    my_list = [0,1,2,3,4,5,6,7,8,9,10,100,101]
    return render_template('index.html', my_list=my_list)

@app.route("/book")
def anmelden():
    all_available_dates=[]
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintoshf  Mac OS X 10_12_6) AppeWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
    'Connection': 'keep-alive'
    }
    session = requests.Session()
    url = 'https://service.berlin.de/dienstleistung/120686/'
    data = session.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    products = soup.findAll('div', {'class': 'zmstermin-multi inner'})
    for p in products:
        link = p.find('a')['href']
        r = session.get(link)
    parseData = BeautifulSoup(r.text, 'html.parser')

    findDates = parseData.findAll('td', {'class': 'buchbar'})
    if len(findDates) == 0:
        sorry_msg = 'Sorry, no appointment dates available :('
        return render_template('sorry.html')
    else:
        #Declare a counter to distinguish between two visible calendar months and two lists to store months names and appointment urls
        counter = 0
        months = []
        appointment_urls = []
        
        #Find the two months names and store it in a list
        for m in parseData.findAll('th', {'class': 'month'}):
            month = m.text.strip()
            months.append(month)
        
        #Since there are two calendars, we need to store them both in the list
        soup = BeautifulSoup(r.content, "html.parser")
        appointment_list = soup.find_all('div', {'class': 'calendar-month-table span6'})

        #For each calendar, get the available appointment urls, the end goal is to create a key/value pair with appointment date and corresponding URL
        for buchbar in appointment_list:
            all_available = buchbar.find_all('td', {'class': 'buchbar'})
            for buchbar in all_available:
                appointment_url =  buchbar.find_all('a', href=True)
                for j in appointment_url:
                    appointment_urls.append(j['href'])
                    all_available_dates.append((buchbar.text.strip() + ' ' + months[counter], j['href']))
            counter = counter + 1
        print(all_available_dates)
        print(len(all_available_dates))
        return render_template('index.html', all_available_dates=all_available_dates)

@app.route('/<user_id>')
def custom_user_page(user_id):
    return render_template('item.html', user_id=user_id)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
