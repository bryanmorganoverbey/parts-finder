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


def parse(soup: BeautifulSoup) -> list[pd.DataFrame]:
    '''Parse the LKQ Nashville inventory and return a list of DataFrames. Each DataFrame contains the info of one car.'''
    result = pd.DataFrame(columns=["title", "available_date", "photo_path"])
    items = soup.select(".pypvi_resultRow")
    for item in items:
        title = item.select_one(".pypvi_ymm").getText().replace(
            '\n', '').replace('\r', '').strip().replace("&", "and")
        date = item.find("time").getText().replace(
            '\n', '').replace('\r', '').strip()
        # get text from second div with class name "pypvi_detailItem"
        detail_items = item.select(".pypvi_detailItem")
        # get the value of the second div
        vin = detail_items[1].getText().replace(
            '\n', '').replace('\r', '').strip()
        loc_in_yard = detail_items[2].getText().replace(
            '\n', '').replace('\r', '').strip()
        # location_in_yard=
        if len(item.select_one(".pypvi_image")) > 0:
            photo_path = item.select_one(".pypvi_image")['href']
        result = pd.concat([result, pd.DataFrame([[title, date, photo_path, vin, loc_in_yard]], columns=[
            "title", "available_date", "photo_path", "vin", "location_in_yard"])])
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
                # add the parsed array to the DataFrame
                cars_df = pd.concat([cars_df, parsed_array])

            return cars_df
        except requests.exceptions.RequestException as e:
            print("Error in creating LKQ list: ", e)
