# LKQ.py
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup


def make_soup(url: str) -> BeautifulSoup:
    '''Make a BeautifulSoup object from the LKQ Nashville inventory page.'''
    r = requests.get(url,
                     headers={
                         "Referer": "https://www.lkqpickyourpart.com/inventory/nashville-1218/"},
                     timeout=5)
    if r.status_code != 200:
        print('Failed to get LKQ data: ', r.status_code)
        sys.exit(1)
    return BeautifulSoup(r.text, 'html.parser')


def parse(soup: BeautifulSoup) -> list[list[str]]:
    '''Parse the LKQ Nashville inventory and return a list of DataFrames. Each DataFrame contains the info of one car.'''
    result = []
    items = soup.select(".pypvi_resultRow")
    for item in items:
        title = item.select_one(".pypvi_ymm").getText().replace(
            '\n', '').replace('\r', '').strip().replace("&", "and")
        date = item.find("time").getText().replace(
            '\n', '').replace('\r', '').strip()
        if len(item.select_one(".pypvi_image")) > 0:
            photo_path = item.select_one(".pypvi_image")['href']
        result.append(pd.DataFrame([[title, date, photo_path]], columns=[
                      "title", "available_date", "photo_path"]))
    return result


class Nashville:
    '''Class to scrape LKQ Nashville inventory and return a DataFrame with car info.'''

    def __init__(self):
        # Constructor code goes here
        pass

    def create_lkq_nashville_df(self) -> pd.DataFrame:
        '''Scrape LKQ Nashville inventory and return a DataFrame with car info.'''
        cars_df = pd.DataFrame(columns=["title", "release_date"])
        try:
            for i in range(5):
                url = f"https://www.lkqpickyourpart.com/DesktopModules/pyp_vehicleInventory/getVehicleInventory.aspx?page={i+1}&filter=&store=1218&pageSize=15"
                parsed_array = parse(make_soup(url))
                print(parsed_array)
                cars_df = pd.concat(parsed_array, ignore_index=True)
            return cars_df
        except requests.exceptions.RequestException as e:
            print("Error in creating LKQ list: ", e)
