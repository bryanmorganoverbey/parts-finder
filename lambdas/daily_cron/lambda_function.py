import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import LKQ
# from Pick_A_Part import PickAPart
from sns_email_alerts import publish_to_sns


def main(event=None, lambda_context=None) -> None:
    try:
        LKQ_Nashville()
        # Pick_A_Part_Nashville()
        print("Done!")
    except (ValueError, TypeError) as e:
        # Code to handle any exception
        print("An exception occurred:", e)


def LKQ_Nashville() -> None:
    lkq = LKQ.Nashville()
    lkq_cars_df = lkq.create_lkq_nashville_df()
    # Create an empty list to store DataFrames
    parts_and_averages = []
    for i in range(len(lkq_cars_df)):
        lkq_car_info = lkq_cars_df.iloc[i]
        for part in ["Body+control+module",  "amplifier",  "ECU", "Headlight+Ballast", "fuse box", "radio"]:
            item = ('+'.join(lkq_car_info["title"].split()) + "+" + part)
            print(item)
            url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={item}&_sacat=0&_osacat=0&_sop=16&LH_Complete=1&LH_Sold=1&LH_ItemCondition=3000"
            parsed_ebay_items_list = parse(make_soup(url))
            if len(parsed_ebay_items_list) == 0:
                print("No items found on eBay!")
                continue
            ebay_df = pd.DataFrame(parsed_ebay_items_list, columns=[
                'title', 'price', 'link'])

            # get_average_part_price returns a dataframe with part query and average price
            parts_and_averages.append(get_median_part_price(
                item, lkq_car_info["available_date"], ebay_df, url, lkq_car_info["photo_path"], lkq_car_info["vin"], lkq_car_info["location_in_yard"]))
    # Concatenate all DataFrames in the list into one DataFrame
    combined_df = pd.concat(parts_and_averages, ignore_index=True)
    # Return only the top 10 earning products and their ebay URLs
    combined_df = combined_df.nlargest(20, 'median_price')
    publish_to_sns(combined_df, "LKQ Nashville")


def Pick_A_Part_Nashville() -> None:
    pick_a_part = PickAPart()
    pick_a_part_cars_df = pick_a_part.create_pick_a_part_nashville_df()
    # Create an empty list to store DataFrames
    parts_and_averages = []
    print("Number of cars found: ", len(pick_a_part_cars_df))
    for i in range(len(pick_a_part_cars_df)):
        pick_a_part_car_info = pick_a_part_cars_df.iloc[i]
        for part in ["Body+control+module",  "amplifier",  "ECU", "Headlight+Ballast", "fuse box", "radio"]:
            item = (
                '+'.join(pick_a_part_car_info["title"].split()) + "+" + part)
            print(item)
            url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={item}&_sacat=0&_osacat=0&_sop=16&LH_Complete=1&LH_Sold=1&LH_ItemCondition=3000"
            parsed_ebay_items_list = parse(make_soup(url))
            if len(parsed_ebay_items_list) == 0:
                print("No items found on eBay!")
                continue
            ebay_df = pd.DataFrame(parsed_ebay_items_list, columns=[
                'title', 'price', 'link'])

            # get_average_part_price returns a dataframe with part query and average price
            parts_and_averages.append(get_median_part_price(
                item, pick_a_part_car_info["available_date"], ebay_df, url, pick_a_part_car_info["photo_path"], "no vin", pick_a_part_car_info["location_in_yard"]))
    # Concatenate all DataFrames in the list into one DataFrame
    combined_df = pd.concat(parts_and_averages, ignore_index=True)
    # Return only the top 10 earning products and their ebay URLs
    combined_df = combined_df.nlargest(20, 'median_price')
    publish_to_sns(combined_df, "Pick A Part Nashville")


def make_soup(url: str) -> BeautifulSoup:
    '''Make a BeautifulSoup object from the LKQ Nashville inventory page.'''
    r = requests.get(url, timeout=5)
    if r.status_code != 200:
        print('Failed to get data: ', r.status_code)
        sys.exit(1)
    return BeautifulSoup(r.text, 'html.parser')


def parse(soup: BeautifulSoup) -> list[list[str]]:
    '''Parse the LKQ Nashville inventory and return a list of DataFrames. Each DataFrame contains the info of one car.'''
    result = []
    items = []
    # Check if the warning "No exact matches found" appears and skip if it does
    null_warning = soup.select_one(".srp-save-null-search")
    if null_warning:
        print("No exact matches found!")
    else:
        print("Found matches!")
    if null_warning is None:
        # Find the span tag containing the text "Results matching fewer words"
        stop_span = soup.find('span', string="Results matching fewer words")
        # Get all items before this span tag

        if stop_span:
            print("Stop span found!")
            # Get all preceding siblings that are elements
            previous_elements = stop_span.find_all_previous(
                "li", class_="s-item")
            print("Number of previous siblings: ", len(previous_elements))
            for sibling in previous_elements:
                items.append(sibling)
            items.reverse()  # Reverse to maintain the original order
        else:
            print("Stop span not found!")
            items = soup.find_all("li", class_="s-item")
        print("Number of items found: ", len(items))
        for item in items:
            try:
                title = item.select_one(".s-item__title").getText(strip=True)
                price = item.select_one(".s-item__price").getText(strip=True)
                print("Item price: ", price)
                link = item.select_one(".s-item__link")['href']
                result.append([title, price, link])
            except (ValueError, TypeError) as e:
                print("An exception occurred:", e)
                title = "invalid!"
                price = 0
                link = "no link!"
                result.append([title, price, link])
    return result


def get_median_part_price(query: str, available_date: str, df: pd.DataFrame, url: str, photo_path: str, vin: str, location_in_yard: str) -> pd.DataFrame:
    '''Compute the median price of a part from the eBay search results. Return a DataFrame with the part query, available date, median price, and eBay URL.'''
    # Clean the 'price' column by removing dollar signs and converting to numeric type
    # Function to strip leading $ and extract only the leading number
    median_price = 0.0
    average_price = 0.0
    try:
        # clean the price column by removing dollar signs and converting to numeric type
        df['price'] = df['price'].replace(
            '[^0-9.]', '', regex=True).astype(float)

        # Compute the average price
        average_price = df['price'].mean()
        median_price = df['price'].median()
        print("Average price after cleaning data:", average_price)
    except (ValueError, TypeError) as e:
        print("An error occurred:", e)
        average_price = 0.0
        median_price = 0.0
    finally:
        data = [[query, available_date, average_price,
                median_price,  url, photo_path, vin, location_in_yard]]
        dataframe = pd.DataFrame(data, columns=[
            'title', 'available_date', 'average_price', 'median_price', 'url', "photo_path", "vin", "location_in_yard"])
        print(dataframe)
    return dataframe


if __name__ == '__main__':
    main()
