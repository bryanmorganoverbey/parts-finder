'''This module is responsible for sending the email alerts to the users'''
import boto3
import pandas as pd


def publish_to_sns(dataframe, location):
    '''Publishes the list of items to the SNS topic'''
    topic_arn = "arn:aws:sns:us-east-2:678837614953:Parts-finder"
    sns = boto3.client("sns", region_name="us-east-2")
    sns.publish(
        TopicArn=topic_arn,
        Message=formatted_list(dataframe),
        Subject=f"Your daily parts alert! {location}",
    )


def formatted_list(combined_df: pd.DataFrame):
    '''Formats the list of items to be sent in the email alert'''
    formatted_message = ""
    for i, row in combined_df.iterrows():
        item_name = combined_df.at[i, "title"]
        available_date = combined_df.at[i, "available_date"]
        average_price = combined_df.at[i, "average_price"]
        median_price = combined_df.at[i, "median_price"]
        url = combined_df.at[i, "url"]
        photo_path = combined_df.at[i, "photo_path"]
        vin = combined_df.at[i, "vin"]
        location_in_yard = combined_df.at[i, "location_in_yard"]
        formatted_message += f"""
    -----------------------------------
    Item            : {item_name}
    Available Date  : {available_date}
    Average Price   : {average_price}
    Median Price    : {median_price}
    URL             : {url}
    LKQ Photo       : {photo_path}
    VIN             : {vin}
    Location in Yard: {location_in_yard}
    \n
    """
    print(formatted_message)
    return formatted_message
