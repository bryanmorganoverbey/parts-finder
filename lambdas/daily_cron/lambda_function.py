import sys
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import LKQ
from sns_email_alerts import publish_to_sns


def main(event = None, lambda_context = None) -> None:
    lkq = LKQ.Nashville()
    cars_df = lkq.create_lkq_nashville_df()
    # Create an empty list to store DataFrames
    parts_and_averages = []
    try:
      for i in range(len(cars_df)):
        car_info = cars_df.iloc[i]
        for part in ["ABS+pump", "Body+control+module", "TCU", "ECU", "amplifier", "Headlight"]:
          item = ('+'.join(car_info["title"].split()) + "+" + part)
          print(item)
          url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={item}&_sacat=0&_osacat=0&_sop=16&LH_Complete=1&LH_Sold=1&LH_ItemCondition=3000"
          df = pd.DataFrame(parse(make_soup(url)), columns=[
                            'title', 'price', 'link'])
          # get_average_part_price returns a dataframe with part query and average price
          parts_and_averages.append(get_median_part_price(item, car_info["available_date"], df, url))
      # Concatenate all DataFrames in the list into one DataFrame
      combined_df = pd.concat(parts_and_averages, ignore_index=True)
      # Return only the top 10 earning products and their ebay URLs
      combined_df = combined_df.nlargest(20, 'median_price')
      publish_to_sns(combined_df)
      print("Done!")
    except Exception as e:
      # Code to handle any exception
      print("An exception occurred:", e)



def make_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    if r.status_code != 200:
        print('Failed to get data: ', r.status_code)
        sys.exit(1)
    return BeautifulSoup(r.text, 'html.parser')


def parse(soup: BeautifulSoup) -> list[list[str]]:
    result = []

    # Check if the warning "No exact matches found" appears and skip if it does
    null_warning = soup.select_one(".srp-save-null-search")
    if null_warning is None:
        # Find the span tag containing the text "Results matching fewer words"
        stop_span = soup.find('span', text="Results matching fewer words")

        # Get all items before this span tag
        if stop_span:
            # Get all preceding siblings that are elements
            items = []
            for sibling in stop_span.previous_elements:
                if sibling.name == "div" and "s-item" in sibling.get("class", []):
                    items.append(sibling)
                if sibling.name == "html":
                    break
            items.reverse()  # Reverse to maintain the original order
        else:
            items = soup.select(".s-item")

        for item in items:
            try:
                title = item.select_one(".s-item__title").getText(strip=True)
                price = item.select_one(".s-item__price").getText(strip=True)
                link = item.select_one(".s-item__link")['href']
                result.append([title, price, link])
            except:
                title = "invalid!"
                price = 0
                link = "no link!"
                result.append([title, price, link])

    return result

def get_median_part_price(query: str, available_date: str, df: pd.DataFrame, url: str) -> pd.DataFrame:
    # Clean the 'price' column by removing dollar signs and converting to numeric type
# Function to strip leading $ and extract only the leading number
    try:
      df['price'] = df['price'].replace('[^0-9.]', '', regex=True).astype(float)
      # Compute the average price
      average_price = df['price'].mean()
      median_price = df['price'].median()
      print("Average:", average_price)
    except:
      average_price = 0.0
      median_price = 0.0
    finally:
      data = [[query, available_date, average_price, median_price,  url]]
      dataframe = pd.DataFrame(data, columns=['title', 'available_date', 'average_price', 'median_price', 'url'] )
      print(dataframe)

    return dataframe


if __name__ == '__main__':
    main()
