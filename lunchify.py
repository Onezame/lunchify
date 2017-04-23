#!/usr/bin/python
# -*- coding: UTF-8 -*-
#author Samu Kumpulainen, 23.4.2017
#Checks lounaat.info's today's lunch menus for given searchterm 
from lxml import html
import requests
import sys
import re

location = 'jyvaskyla'
searchterm = sys.argv[1]
url = 'https://www.lounaat.info/' + location
page = requests.get(url)
tree = html.fromstring(page.content)

menus = tree.xpath("/html/body/div[5]/div[2]/div[2]/*")
info = []
i = 1
for e in menus:
    rafla = []
    namepath = 'div/h3/a/text()'
    dishpath = 'div/ul/li/p/text()'

    name = e.xpath(namepath)
    dishes = e.xpath(dishpath)

    if not (len(name) == 0):
        rafla.append(name[0])
    for dish in dishes:
        rafla.append(dish)
    info.append(rafla)

r = re.compile(".*%s.*" % searchterm)
places_with_food = []

for restaurant in info:
    foods = restaurant[1:]
    if len((filter(r.search, foods))) > 0:
        places_with_food.append(restaurant[0])

if not len(places_with_food) > 0:
    print "Ei löydy tänään lounaspaikkaa, jossa olisi", searchterm
else:
    print "Ravintolat, joista löytyy tänään ", searchterm, ":"
    for place in places_with_food:
        print place


def check_for_food(foods):
  #  searchObj = re.search(r'(.*)%d(.*)' % searchterm, re.I)
  #  return searchObj
    return true
