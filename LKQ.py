# LKQ.py
import os
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup


def make_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, headers={
                     "Referer": "https://www.lkqpickyourpart.com/inventory/nashville-1218/"})
    if r.status_code != 200:
        print('Failed to get LKQ data: ', r.status_code)
        sys.exit(1)
    return BeautifulSoup(r.text, 'html.parser')


def parse(soup: BeautifulSoup) -> list[list[str]]:
    result = []
    items = soup.select(".pypvi_resultRow")
    for item in items:
        title = item.select_one(".pypvi_ymm").getText()
        # price = item.select_one(".s-item__price").getText(strip=True)
        # link = item.select_one(".s-item__link")['href']
        result.append(title)
    return result


class Nashville:
    """
    Documentation for MyClass.
    """

    def __init__(self):
        # Constructor code goes here
        pass

    def create_lkq_nashville_csv(self):
        """
        Documentation for my_method.
        """
        # delete old file
        try:
          os.remove("LKQ_car_list.csv")
        except:
            pass
        f = open("LKQ_car_list.csv", "a")
        # Method code goes here
        for i in range(1):
          url = f"https://www.lkqpickyourpart.com/DesktopModules/pyp_vehicleInventory/getVehicleInventory.aspx?page={i+1}&filter=&store=1218&pageSize=15"
          titleArray = parse(make_soup(url))
          for t in titleArray:
            t = t.lstrip()  # This will strip leading spaces and tabs
            t = t.rstrip()
            f.write(t + "\n")
  # Additional functions, classes, or variables can be defined here
