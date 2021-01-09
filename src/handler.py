import json
import pandas as pd
from datetime import datetime, timedelta
from src.lib.oop_class import Bazi, ParcelData, ParcelBazi
from src.lib.method import return_branch_of_year


def hello(event, context):
    response = []
    response.append({
        "world": "yes"
    })
    response = {
        "statusCode": 200,
        "body": json.dumps(response)
    }
    return response


def show_all_pokemon(event, context):
    response = []
    df = pd.read_csv(
        'https://koh-assets.s3-ap-southeast-1.amazonaws.com/superai/bazi_list.csv')
    for index, row in df.iterrows():
        response.append({
            "name": row['pokemon_name'],
            "code": row['pokemon_code'],
            "earthly_branch": row["earthly_branch"],
            "heavenly_stem": row["hevenly_stem"],
            "monster_image": f"https://koh-assets.s3-ap-southeast-1.amazonaws.com/superai/pokebazi/{row['pokemon_code']}.png"
        })
    response = {
        "statusCode": 200,
        "body": json.dumps(response)
    }
    return response


def current_bazi(event, context):
    now = datetime.now()
    hours = 7
    hours_added = timedelta(hours=hours)
    future_date_and_time = now + hours_added
    bazi = Bazi(future_date_and_time)
    response = {
        "statusCode": 200,
        "body": json.dumps(bazi.body())
    }
    return response


def predict_bazi(event, context):
    parcel = json.loads(event['body'])
    bodify = ParcelData(parcel['date'], parcel['time'])
    bazi = Bazi(bodify.strp_format())
    response = {
        "statusCode": 200,
        "body": json.dumps(bazi.body())
    }
    return response


def translate_bazi(event, context):
    parcel = json.loads(event['body'])
    bodify = ParcelBazi(parcel['hour'], parcel['day'],
                        parcel['month'], parcel['year'])
    body = {
        "response": bodify.translate()
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response
