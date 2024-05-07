import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import LKQ


def main(query: str) -> None:
    print(sys.argv[1])
    lkq = LKQ.Nashville()
    lkq.create_lkq_nashville_csv()
    # Create an empty DataFrame
# Create an empty list to store DataFrames
    dfs = []
    try:
      title_file = open("LKQ_car_list.csv")
      for line in title_file:
        url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={line}&_sacat=0&_osacat=0&_sop=16&LH_Complete=1&LH_Sold=1"
        print(url, file=sys.stderr)

        df = pd.DataFrame(parse(make_soup(url)), columns=[
                          'title', 'price', 'link'])
        # Append the current DataFrame to the list
        dfs.append(df)
    finally:
      # Concatenate all DataFrames in the list into one DataFrame
      combined_df = pd.concat(dfs, ignore_index=True)
      combined_df.to_csv("output.csv", sep="\t", index=False)
      print("Done!")


def make_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    if r.status_code != 200:
        print('Failed to get data: ', r.status_code)
        sys.exit(1)
    return BeautifulSoup(r.text, 'html.parser')


def parse(soup: BeautifulSoup) -> list[list[str]]:
    result = []
    items = soup.select(".s-item")
    for item in items:
        title = item.select_one(".s-item__title").getText(strip=True)
        price = item.select_one(".s-item__price").getText(strip=True)
        link = item.select_one(".s-item__link")['href']
        result.append([title, price, link])
    return result


if __name__ == '__main__':
    main(sys.argv[1])
