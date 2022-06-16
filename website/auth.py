from email.policy import strict
import re
from unittest import result
from flask import Flask, jsonify, json,request
from flask import Blueprint,render_template, request,flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from .models import *
from .models import db
from requests import  get

import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


db.init_app(app)

app.config['SECRET_KEY'] = "groupe5"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:groupe5@localhost/scrapy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
auth = Blueprint('auth', __name__)


@auth.route("/")
def main():
    flipkart = Flipkart.query.order_by(Flipkart.prix.desc()).limit(32).all()
    ebay = Ebay.query.order_by(Ebay.prix.desc())[33:59]
    data3 = Olx.query.order_by(Olx.prix.desc()).limit(31).all()
    return render_template('home.html', data = flipkart, data2 = ebay, materiel = data3)






name = "iphone"
#name = input("Entrer le nom du produit\t")
#url du site flipkart
def get_url():
    fname = name
    fname = fname.replace(' ','%20')
    url = 'https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
    url = url.format(fname)
    url += "&page{}" 
    
    return url
#scraping avec beautifulsoup
def get_soup(url):
    url = get_url()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup
#les paginations
def get_pages():
    pages = []
    route = get_url()
    souper = get_soup(route)
    nav = souper.find_all('nav', class_="yFHi8N")
    links = nav[0].find_all('a', class_="ge-49M")
    for link in links:
        lien = 'https://www.flipkart.com' + link['href']
        pages.append(lien)
    return pages

#collections des donnees

def get_details():
    data = []
    pages = get_pages()
    for page in pages:
        soup = get_soup(page)
        items = soup.find_all('div', class_ = "_13oc-S")#bloc du produit
        
        for item in items:
            try:
                titre = item.find("div", class_ ="_4rR01T").text
            except AttributeError:
                titre =" pas de titre "
            try:
                prixx = item.find("div", class_ ="_30jeq3 _1_WHN1").text 
                prix = float(prixx.replace("₹","").replace(",",""))*0.012
            except AttributeError:
                prix = "prix non disponible"
                
           
                
            lien = (titre, prix)
            data.append(lien)
            flipkart = Flipkart(prix = prix,
                                titre = titre    
                                   )
            db.session.add(flipkart)
        db.session.commit()
        


name = "iphone"
#name = input("Entrer le nom du produit\t")
#url du site ebay
def get_url():
    fname = name
    fname = fname.replace(' ','%20')
    url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={}&_sacat=0&LH_TitleDesc=0&_odkw=samsung&_osacat=0'
    url = url.format(fname)
    url += "&page{}" 
    
    return url
#scraping avec beautifulsoup
def get_soup(url):
    url = get_url()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
    }
    
    req = requests.get(url, headers = headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    return soup
#les paginations
def get_pages():
    pages = []
    temp = get_url()

    for i in range(1):

        if i == 0:
            pages.append(temp)
        else:
            ss = get_soup(temp)
            nextBtn = ss.find_all('li')

            next_link = nextBtn[0].a.get('href')
            next_url = get_url().format(next_link)
            temp = next_url
            pages.append(temp)

    return pages


#collections des donnees

def get_details():
    data = []
    pages = get_pages()
    for page in pages:
        soup = get_soup(page)
        items = soup.find_all('li', class_ = "s-item s-item__pl-on-bottom s-item--watch-at-corner")#bloc du produit
        
        for item in items:
            try:
                titre = item.find("h3", class_ ="s-item__title").text
            except AttributeError:
                titre =" pas de titre "
            try:
                prixs = item.find("span", class_ ="s-item__price").text 
                prix = prixs.replace("$","€")
            except AttributeError:
                prix = "prix non disponible"
            
            lien = (titre, prix)
            data.append(lien)
            ebay = Ebay(prix = prix,
                                titre = titre    
                                   )
            db.session.add(ebay)
        db.session.commit()
            
       


    
    

