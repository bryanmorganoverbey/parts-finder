import boto3
import pandas as pd

def publish_to_sns(dataframe):
    topic_arn = "arn:aws:sns:us-east-2:678837614953:Parts-finder"
    sns = boto3.client("sns")
    response = sns.publish(
        TopicArn=topic_arn,
        Message=formatted_list(dataframe),
        Subject="Your daily parts alert!",

    )

def formatted_list(combined_df: pd.DataFrame):
    formatted_message = ""
    for i, row in combined_df.iterrows():
        formatted_message += '''
        -----------------------------------
        Item            : {item_name}
        Available Date  : {available_date}
        Average Price   : {average_price}
        Median Price    : {median_price}
        URL             : {url}
        \n
        '''.format(item_name=combined_df.at[i,"title"], available_date=combined_df.at[i,"available_date"], average_price=combined_df.at[i,"average_price"], median_price=combined_df.at[i,"median_price"], url=combined_df.at[i,"url"])
    print(formatted_message)
    return formatted_message
