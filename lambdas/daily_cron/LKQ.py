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
        title = item.select_one(".pypvi_ymm").getText().replace('\n', '').replace('\r', '').strip()
        # Find the element containing the text "Available:"
        date = item.find("time").getText().replace('\n', '').replace('\r', '').strip()
        # Navigate to the next sibling element to get the date
        # price = item.select_one(".s-item__price").getText(strip=True)
        # link = item.select_one(".s-item__link")['href']
        result.append(pd.DataFrame([[title, date]], columns=["title", "available_date"]))
    return result
class Nashville:
    def __init__(self):
        # Constructor code goes here
        pass

    def create_lkq_nashville_df(self) -> pd.DataFrame:
        cars_df = pd.DataFrame(columns=["title", "release_date"])
        try:
          for i in range(1):
            url = f"https://www.lkqpickyourpart.com/DesktopModules/pyp_vehicleInventory/getVehicleInventory.aspx?page={i+1}&filter=&store=1218&pageSize=15"
            parsedArray = parse(make_soup(url))
            print(parsedArray)
            cars_df = pd.concat(parsedArray , ignore_index=True)
          return cars_df
        except Exception as e:
          print("Error in creating LKQ list: ", e)
