#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# author Samu Kumpulainen, 22.5.2017
# Checks lounaat.info's today's lunch menus for given searchterm

import click
from lxml import html
import requests
import sys
import re
import random

LOCATION = 'jyvaskyla'

def search(searchterm, number):

    if not searchterm:
        print("Anna yksi hakutermi!")
        sys.exit()

    r = re.compile("(?i).*%s.*" % searchterm)
    places_with_food = []

    info = get_restaurant_info()
    for restaurant in info:
        foods = restaurant[1:]
        lista = [elem for elem in foods if r.search(elem)]
        if  len (lista)  > 0:
            places_with_food.append(restaurant[0] + ": " + ''.join(lista) + '\n')

    if not len(places_with_food) > 0:
        print("Ei löydy tänään lounaspaikkaa, jossa olisi", searchterm)
    else:
        print("Ravintolat, joista löytyy tänään ", searchterm, ":")
        print("----------------------------------")
        for place in places_with_food[:number]:
            print(place)
        print("----------------------------------")


def get_restaurant_info():
    
    url = 'https://www.lounaat.info/' + LOCATION
    page = requests.get(url)
    tree = html.fromstring(page.content)

    menus = tree.xpath("/html/body/div[5]/div[2]/div[1]/*")
    info = []
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
    
    return info



def suggest(number):
    
    restaurant_info = list(filter(None, get_restaurant_info()))
    random.shuffle(restaurant_info)
    suggestions = restaurant_info[:number]
    
    print("Tässä olisi hyviä vaihtoehtoja:")
    for restaurant in suggestions:
        print("===================================")
        print(f"{restaurant[0]}:")
        print("===================================")
        for food in restaurant[1:]:
            print(f"- {food}")
           
        


@click.command()
@click.option("--random", "-r", "mode", help="Restaurants are suggested randomly", flag_value="random", default=True)
@click.option("--search", "-s", "mode", help="Searches for given food on restaurants", flag_value="search")
@click.argument("searchterm", required=False)
@click.option("--number", "-n", default = 10, help="How many restaurants are shown")
def main(mode, number, searchterm = "*"):
    if (mode == "random"):
        suggest(min(3,number))
    else:
        search(searchterm, number)


if __name__ == "__main__":
    main()