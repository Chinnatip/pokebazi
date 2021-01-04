import math
from datetime import date
from src.lib.dict import febuary_stem_dict, hour_dict, rat_hour_stem_dict, month_branch_id, hour_branch_id, reverse_branch_dict


def string_digit(string_num):
    number = int(string_num)
    if(number <= 9):
        return f"0{number}"
    else:
        return number


def find_year_branch(year):
    print(year)
    mod_year = (year - 3) % 12
    print(mod_year)
    return 12 if mod_year == 0 else mod_year


def return_branch_of_year(year_id, base_year=2020):
    year_branch_collect = []
    for add in range(5):
        year_branch_collect.append(base_year + (add * 12) + (year_id - 1))
    return year_branch_collect


def find_month_stem(year_stem, month):
    month_stem = (febuary_stem_dict[year_stem] + month - 2) % 10
    return 10 if month_stem == 0 else month_stem


def find_year_stem(year):
    return (year-3)-(math.floor((year - 3)/10)*10)


def find_day_stem(year, month, day, leap):
    # Prepare day
    a = date(year, month, day)
    b = date(year, 1, 1)

    # Calculation
    mod_day = year % 1900 if year < 2000 else year % 2000
    diff_day = (a-b).days
    balancer = (-1 * (5 + leap)) if year >= 2000 else 10 + (1 * leap)
    day_mod = ((5 * mod_day) + math.ceil((mod_day / 4)) +
               diff_day + balancer + (1 * leap)) % 60

    # Find Day stem and branch
    day_stem = 10 if day_mod % 10 == 0 else day_mod % 10
    day_branch = 12 if day_mod % 12 == 0 else day_mod % 12

    return [day_stem, day_branch]


def find_hour_stem(day_stem, hour):
    hour_stem_filter = rat_hour_stem_dict[day_stem]
    hour_diff = math.ceil(hour_dict[hour] / 2)
    mod_hour = (hour_stem_filter + hour_diff) % 10
    return 10 if mod_hour == 0 else mod_hour


def bazi_calculate(hour, day, month, year, leap=False):
    year_branch = find_year_branch(year)
    year_stem = find_year_stem(year)
    month_stem = find_month_stem(year_stem, month)
    [day_stem, day_branch] = find_day_stem(year, month, day, leap)
    hour_stem = find_hour_stem(day_stem, hour)
    return [
        year_branch, day_branch, month_branch_id[month], hour_branch_id[hour],
        year_stem, month_stem, day_stem, hour_stem
    ]
