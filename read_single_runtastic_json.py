import json
from time import strftime, localtime
from math import floor, isnan
import os
from os import listdir
from os.path import isfile, join, isdir
import pandas as pd
import datetime


# Jerusalem Marathon
json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2024-03-08_05-01-39-UTC_b0ba3a9b-a1b9-4bc3-b13c-795d5a2b579e.json"
# json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2024-04-21_19-38-40-UTC_92e8cd55-89bc-4b36-8091-4521b9683d47.json"
# json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2014-11-10_02-00-52-UTC_55d975a493bc7d05fa58603b.json"
json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2022-08-25_12-48-05-UTC_3cbc3ffa-5eee-4eac-82a9-ac3144e4a84b.json"


def epoch_time_convert(_etime):
    hours = int(floor(_etime / 60000) / 60)
    minutes = (int(_etime / 60000)) % 60
    seconds = floor(((_etime / 60000) - int(_etime / 60000)) * 60)
    return hours, minutes, seconds


def read_runtastic_json(_json_file=json_file):
    with open(_json_file, 'r', encoding="utf8") as json_data:
        json_data_content = json.load(json_data)
    #
    print("\n" + "*" * 80 + "\n" + "*" * 80 + "\n" + "*" * 80 + "\n")
    print("start_time\t", json_data_content["start_time"])
    print("end_time\t", json_data_content["end_time"])
    print("duration\t", json_data_content["duration"])
    print("start_time\t", json_data_content["start_time"], "\t",
          strftime('%Y-%m-%d %H:%M:%S', localtime(json_data_content["start_time"] / 1000)))
    print("end_time\t", json_data_content["end_time"], "\t",
          strftime('%Y-%m-%d %H:%M:%S', localtime(json_data_content["end_time"] / 1000)))
    duration_h, duration_min, duration_sec = epoch_time_convert(json_data_content["duration"])
    print("duration\t", json_data_content["duration"], f"\t\t{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}")
    #
    print("calories\t", f'{json_data_content["calories"]}')
    #
    print("sport_type_id\t", json_data_content["sport_type_id"])
    #
    for dicts in json_data_content["features"]:
        if "type" in dicts and "initial_values" in dicts['type']:
            duration_h, duration_min, duration_sec = epoch_time_convert(json_data_content["duration"])
            print("duration\t\t\t", dicts["attributes"]["duration"], f"\t\t{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}")
            print("distance [Km]\t\t", f'{dicts["attributes"]["distance"] / 1000}')
            print("sport_type_id\t\t", dicts["attributes"]["sport_type"]["id"])
    for dicts in json_data_content["features"]:
        if "type" in dicts and "track_metrics" in dicts['type']:
            speed_factor = 3600 / 1000
            # average_speed
            print("average_speed raw\t", dicts["attributes"]["average_speed"])
            ave_speed = float(dicts["attributes"]["average_speed"]) * speed_factor
            print("average_speed\t\t", f"{('%.2f' % ave_speed):0>5}")
            print("average_pace raw\t", dicts["attributes"]["average_pace"])
            minutes = (float(dicts["attributes"]["average_pace"]) * (1000 / 60))
            seconds = floor((minutes - int(minutes)) * 60)
            print("average_pace\t\t", f"00:{int(minutes):0>2}:{seconds:0>2}")
            # max_speed
            print("max_speed raw\t\t", dicts["attributes"]["max_speed"])
            max_speed = float(dicts["attributes"]["max_speed"]) * speed_factor
            print("max_speed\t\t\t", f"{('%.2f' % max_speed):0>5}")

    top_1km, top_5km, top_10km, top_21_1km, top_42_2km = 0, 0, 0, 0, 0
    for dicts in json_data_content["features"]:
        if "type" in dicts and "fastest_segments" in dicts['type']:
            print("segments\t", dicts["attributes"]["segments"])
            for top_speed in dicts["attributes"]["segments"]:
                if "1km" in top_speed["distance"]:
                    print("1km raw", top_speed["duration"])
                    hours, minutes, seconds = epoch_time_convert(top_speed["duration"])
                    print("1km min", minutes)
                    print("1km sec", seconds)
                    print("1km -->", f"00:{minutes :0>2}:{seconds :0>2}")
                    top_1km = 1
                elif "5km" in top_speed["distance"]:
                    print("5km raw", top_speed["duration"])
                    hours, minutes, seconds = epoch_time_convert(top_speed["duration"])
                    print("5km min", minutes)
                    print("5km sec", seconds)
                    print("5km -->", f"00:{minutes :0>2}:{seconds :0>2}")
                    top_5km = 1
                elif "10km" in top_speed["distance"]:
                    print("10km raw", top_speed["duration"])
                    hours, minutes, seconds = epoch_time_convert(top_speed["duration"])
                    print("10km min", minutes)
                    print("10km sec", seconds)
                    print("10km -->", f"{hours :0>2}:{minutes :0>2}:{seconds :0>2}")
                    top_10km = 1
                elif "half_marathon" in top_speed["distance"]:
                    print("21_1km raw", top_speed["duration"])
                    hours, minutes, seconds = epoch_time_convert(top_speed["duration"])
                    print("21_1km hour", hours)
                    print("21_1km min", minutes)
                    print("21_1km sec", seconds)
                    print("21_1km -->", f"{hours :0>2}:{minutes :0>2}:{seconds :0>2}")
                    top_21_1km = 1
                elif top_speed["distance"] == "marathon":
                    print("42_2km raw", top_speed["duration"])
                    hours, minutes, seconds = epoch_time_convert(top_speed["duration"])
                    print("42_2km hour", hours)
                    print("42_2km min", minutes)
                    print("42_2km sec", seconds)
                    print("42_2km -->", f"{hours :0>2}:{minutes :0>2}:{seconds :0>2}")
                    top_42_2km = 1
                if "mi" not in top_speed["distance"]:
                    print('-' * 30)
            if top_1km == 0:
                print("1km -->", "00:00:00")
            if top_5km == 0:
                print("5km -->", "00:00:00")
            if top_10km == 0:
                print("10km -->", "00:00:00")
            if top_21_1km == 0:
                print("21.1km -->", "00:00:00")
            if top_42_2km == 0:
                print("42.2km -->", "00:00:00")

    heart_rate_flag = 0
    for dicts in json_data_content["features"]:
        if "type" in dicts and "heart_rate" in dicts['type']:
            print("ave_heart_rate\t", f'{dicts["attributes"]["average"]}')
            print("max_heart_rate\t", f'{dicts["attributes"]["maximum"]}')
            heart_rate_flag = 1
    if heart_rate_flag == 0:
        print("heart_rate average\t", 0)
        print("heart_rate maximum\t", 0)
    print("\n" + "*" * 80 + "\n")


if __name__ == "__main__":
    read_runtastic_json()