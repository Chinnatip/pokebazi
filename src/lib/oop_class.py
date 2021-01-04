import pandas as pd
from datetime import datetime
from src.lib.dict import hevenly_stem_dict, branch_dict, reverse_branch_dict, reverse_branch_hour_dict, reverse_month_branch_dict
from src.lib.method import bazi_calculate, string_digit, return_branch_of_year
import urllib.request
import json


class Decoder:
    def __init__(self, heavenly_id, earthly_id, df):
        self.heavenly_id = heavenly_id
        self.earthly_id = earthly_id
        self.df = df

    def response(self):
        # Find pokemon
        df = self.df
        heavenly_id = self.heavenly_id
        earthly_id = self.earthly_id
        pokemon = df.loc[(df.earthly_branch == branch_dict[earthly_id]) &
                         (df.hevenly_stem == hevenly_stem_dict[heavenly_id])].iloc[0]
        return {
            # animals[self.earthly_id],
            "earthly_branch": branch_dict[earthly_id],
            "hevenly_stem":   hevenly_stem_dict[heavenly_id],
            "monster_code": str(pokemon['pokemon_code']),
            "monster_name": pokemon['pokemon_name'],
            "monster_image": f"https://koh-assets.s3-ap-southeast-1.amazonaws.com/superai/pokebazi/{pokemon['pokemon_code']}.png"
        }


# Class interface

class Bazi:
    def __init__(self, time):
        self.time = time

    def log(self): return self.time.strftime("%d/%m/%Y %H:%M")

    def parse(self): return {
        "day": int(self.time.strftime("%-d")),
        "month": int(self.time.strftime("%-m")),
        "year": int(self.time.strftime("%Y")),
        "hour": self.time.strftime("%-I%p"),
    }

    def predict(self):
        time = self.parse()
        [
            year_branch,
            day_branch,
            month_branch,
            hour_branch,
            year_stem,
            month_stem,
            day_stem,
            hour_stem
        ] = bazi_calculate(time['hour'], time['day'], time['month'], time['year'])

        df = pd.read_csv(
            'https://koh-assets.s3-ap-southeast-1.amazonaws.com/superai/pokebazi/bazi_list.csv')

        return {
            "year": Decoder(heavenly_id=year_stem, earthly_id=year_branch, df=df).response(),
            "month": Decoder(heavenly_id=month_stem, earthly_id=month_branch, df=df).response(),
            "day": Decoder(heavenly_id=day_stem, earthly_id=day_branch, df=df).response(),
            "time": Decoder(heavenly_id=hour_stem, earthly_id=hour_branch, df=df).response()
        }

    def body(self):
        return {
            "date": self.log(),
            "prediction": self.predict()
        }


class ParcelData:
    def __init__(self, date, time):
        self.date = date
        self.time = time

    def day(self): return string_digit(self.date.split('-')[2])
    def month(self): return string_digit(self.date.split('-')[1])
    def year(self): return self.date.split('-')[0]
    def hour(self): return string_digit(self.time.split(":")[0])
    def min(self): return string_digit(self.time.split(":")[1])

    def strp_format(self):
        dt_string = f"{self.year()}/{self.month()}/{self.day()} {self.hour()}:00"
        return datetime.strptime(dt_string, "%Y/%m/%d %H:00")


class ParcelBazi:
    def __init__(self, hour, day, month, year):
        self.hour = hour
        self.day = day
        self.month = month
        self.year = year

    def year_branch(self): return return_branch_of_year(
        reverse_branch_dict[self.year])

    def hour_branch(self): return reverse_branch_hour_dict[self.hour]

    def month_branch(
        self): return reverse_month_branch_dict[reverse_branch_dict[self.month]]

    def day_branch_dict(self):
        with urllib.request.urlopen("https://koh-assets.s3-ap-southeast-1.amazonaws.com/superai/pokebazi/day_branch.json") as url:
            day_branch_dict = json.loads(url.read().decode())
            return day_branch_dict

    def translate(self):
        response = []
        day_dict = self.day_branch_dict()
        year_list = self.year_branch()
        month = self.month_branch()
        hour_list = self.hour_branch()
        day_branch_key = reverse_branch_dict[self.day]

        for year in year_list:
            day_list = day_dict[str(year)][str(month)][str(day_branch_key)]
            for day in day_list:
                for hour in hour_list:
                    response.append(f"{hour} {day}/{month}/{year}")

        return response
