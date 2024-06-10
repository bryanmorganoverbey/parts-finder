import sys
import pandas as pd
import requests

# [
#     {
#         "locationID": 6,
#         "exact": [
#             {
#                 "vinID": 136906,
#                 "ticketID": 1919871,
#                 "lineID": 1,
#                 "locID": 6,
#                 "locName": "Nashville",
#                 "makeID": 15,
#                 "makeName": "CADILLAC",
#                 "modelID": 126,
#                 "modelName": "SEVILLE",
#                 "modelYear": 1996,
#                 "row": 134,
#                 "vin": "1G6KS52Y6TU836883",
#                 "dateYardOn": "2024-06-03T14:56:51.16",
#                 "vinDecodedId": 57637,
#                 "extendedInfo": null
#             },
#     }
# ]


def fetch_api_json() -> list[pd.DataFrame]:
    '''Fetch the Pick A Part Nashville inventory API and return a list of DataFrames. Each DataFrame contains the info of one car.'''
    url = "https://inventoryservice.pullapart.com/Vehicle/NewOnYard"
    body = {"DaysOnYard": 7, "Locations": [6]}
    r = requests.post(url, json=body)
    if r.status_code != 200:
        print('Failed to get Pick A Part data: ', r.status_code)
        sys.exit(1)
    # response from requests.post is a JSON object
    api_result = r.json()
    # get the item called "exact" from the JSON object
    api_result = api_result[0]["exact"]
    print(api_result)
    result = pd.DataFrame(columns=["title", "available_date", "photo_path"])

    for item in api_result:
        title = f"{item['modelYear']} {item['makeName']} {item['modelName']}"
        date = item['dateYardOn']
        vin = item['vin']
        loc_in_yard = f"{item['row']}"
        result = pd.concat([result, pd.DataFrame([[title, date, "no photo available!", vin, loc_in_yard]], columns=[
            "title", "available_date", "photo_path", "vin", "location_in_yard"])])
    return result


class PickAPart:
    def __init__(self):
        pass

    def create_pick_a_part_nashville_df(self) -> pd.DataFrame:
        try:
            # add the parsed array to the DataFrame
            cars_df = pd.concat([fetch_api_json()], ignore_index=True)
            print(cars_df)
            return cars_df
        except Exception as e:
            print("Error in creating Pick A Part list: ", e)
