import json
from time import strftime, localtime
from math import floor
import os
from os import listdir
from os.path import isfile, join, isdir
import pandas as pd
import datetime

DEBUG = 0

# PATH = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script"
# PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20240426-000\Sport-sessions\\'  # _output_path
PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20241103-000\Sport-sessions\\'
OUTPUT_DIR_LOCATION = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Excel_and_CSV_new\\'  # _output_path

# Jerusalem Marathon
json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2024-03-08_05-01-39-UTC_b0ba3a9b-a1b9-4bc3-b13c-795d5a2b579e.json"


def decimal_to_time(_decimal_time):
    hours = int(floor(_decimal_time / 60000) / 60)
    minutes = floor(_decimal_time / 60000) % 60
    seconds = floor(((_decimal_time / 60000) - int(_decimal_time / 60000)) * 60) # int(_decimal_time / 60000) == _decimal_time // 60000
    return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"


class Runtastic_Data_To_Csv:
    def __init__(self, _files_path='', _output_path=''):
        self.json_files_path = _files_path
        self.files_in_dir = ""
        self.output_path = _output_path
        self.date_for_folder = ""
        self.date_for_file = ""
        self.num_of_running_files = 0
        self.sport_type_id = '0'
        self.start_time = '0'
        self.end_time = '0'
        self.duration = '0'
        self.duration_decimal = '0'
        self.duration_2 = '0'
        self.calories = '0'
        self.distance = '0'
        self.average_speed = '0'
        self.average_pace = '0'
        self.max_speed = '0'
        self.max_1km = '00:00:00'
        self.max_5km = '00:00:00'
        self.max_10km = '00:00:00'
        self.fastest_max_10km = 3000000
        self.fastest_10km_date = ''
        self.max_21_1km = '00:00:00'
        self.fastest_max_21_1km = 6000000
        self.fastest_21_1km_date = ''
        self.max_42_2km = '00:00:00'
        self.fastest_max_42_2km = 12000000
        self.fastest_42_2km_date = ''
        self.max_heart_rate = '0'
        self.ave_heart_rate = '0'
        #
        self.export_dict = {}
        self.excel_columns = ['start_time', 'end_time', 'duration_decimal', 'duration', 'distance', 'average_pace',
                              'average_speed', 'max_speed', 'max_heart_rate', 'ave_heart_rate', 'calories',
                              'max_1km', 'max_5km', 'max_10km', 'max_21_1km', 'max_42_2km']
        self.excel_columns_raw = self.excel_columns + ['sport_type_id']
        for element in self.excel_columns:
            self.export_dict[element] = []
        #
        #
        # with open(self.json_file, 'r', encoding="utf8") as json_data:
        #     self.json_data_contect = json.load(json_data)

    def create_output_folder(self):
        now = datetime.datetime.now()
        self.date_for_folder = now.strftime('%Y_%m_%d')
        if not os.path.exists(self.output_path + self.date_for_folder):
            os.makedirs(self.output_path + self.date_for_folder)

    def create_files_list(self):
        self.files_in_dir = [f for f in listdir(self.json_files_path) if isfile(join(self.json_files_path, f))]

    def reset_data(self):
        self.sport_type_id = '0'
        self.date = '0'
        self.start_time = '0'
        self.end_time = '0'
        self.duration = '0'
        self.duration_decimal = '0'
        self.duration_2 = '0'
        self.calories = '0'
        self.distance = '0'
        self.average_speed = '0'
        self.average_pace = '0'
        self.max_speed = '0'
        self.max_1km = '00:00:00'
        self.max_5km = '00:00:00'
        self.max_10km = '00:00:00'
        self.max_21_1km = '00:00:00'
        self.max_42_2km = '00:00:00'
        self.max_heart_rate = '0'
        self.ave_heart_rate = '0'

    def time_and_distance(self):
        self.date = strftime('%m-%d-%Y', localtime(self.json_data_contect["start_time"] / 1000))
        self.start_time = strftime('%Y-%m-%d %H:%M:%S', localtime(self.json_data_contect["start_time"] / 1000))
        self.end_time = strftime('%Y-%m-%d %H:%M:%S', localtime(self.json_data_contect["end_time"] / 1000))
        self.duration_decimal = '%.2f' % (self.json_data_contect["duration"] / 60000)
        duration_h = int(floor(self.json_data_contect["duration"] / 60000) / 60)
        duration_min = floor(self.json_data_contect["duration"] / 60000) % 60
        duration_sec = '%.0f' % (
                (self.json_data_contect["duration"] / 60000 - floor(self.json_data_contect["duration"] / 60000)) * 60)
        self.duration = f"{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}"
        self.calories = f'{self.json_data_contect["calories"]}'

    def distance_and_heart_rate(self):
        for dicts in self.json_data_contect["features"]:
            if "type" in dicts and "initial_values" in dicts['type']:
                duration_h = int(floor(dicts["attributes"]["duration"] / 60000) / 60)
                duration_min = floor(dicts["attributes"]["duration"] / 60000) % 60
                duration_sec = '%.0f' % (
                        (dicts["attributes"]["duration"] / 60000 - floor(dicts["attributes"]["duration"] / 60000)) * 60)
                self.duration_2 = f"{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}"
                if "distance" in dicts["attributes"]:
                    self.distance = f'{dicts["attributes"]["distance"] / 1000}'
        for dicts in self.json_data_contect["features"]:
            if "type" in dicts and "heart_rate" in dicts['type']:
                self.max_heart_rate = f'{dicts["attributes"]["maximum"]}'
                self.ave_heart_rate = f'{dicts["attributes"]["average"]}'

    def speed_and_pace(self):
        for dicts in self.json_data_contect["features"]:
            if "type" in dicts and "track_metrics" in dicts['type']:
                speed_factor = 3600 / 1000
                # average_speed
                ave_speed = float(dicts["attributes"]["average_speed"]) * speed_factor
                self.average_speed = f"{('%.2f' % ave_speed):0>5}"
                # average_pace = min_per_km
                minutes = (float(dicts["attributes"]["average_pace"]) * (1000 / 60))
                seconds = floor((minutes - int(minutes)) * 60)
                self.average_pace = f"00:{int(minutes):0>2}:{seconds:0>2}"
                # max_speed. NA for treadmill
                if "max_speed" in dicts["attributes"]:
                    max_speed = float(dicts["attributes"]["max_speed"]) * speed_factor
                    self.max_speed = f"{('%.2f' % max_speed):0>5}"

    def fastest_segments(self):
        for dicts in self.json_data_contect["features"]:
            if "type" in dicts and "fastest_segments" in dicts['type']:
                for top_speed in dicts["attributes"]["segments"]:
                    if top_speed["distance"] == "1km":
                        self.max_1km = decimal_to_time(top_speed["duration"])
                    if "5km" in top_speed["distance"]:
                        self.max_5km = decimal_to_time(top_speed["duration"])
                    if "10km" in top_speed["distance"]: # if top_speed["distance"] == "10km":
                        if top_speed["duration"] < self.fastest_max_10km:
                            self.fastest_max_10km = top_speed["duration"]
                            self.fastest_10km_date = self.date
                        self.max_10km = decimal_to_time(top_speed["duration"])
                    if "half_marathon" in top_speed["distance"]:
                        if top_speed["duration"] < self.fastest_max_21_1km:
                            self.fastest_max_21_1km = top_speed["duration"]
                            self.fastest_21_1km_date = self.date
                        self.max_21_1km = decimal_to_time(top_speed["duration"])
                    if top_speed["distance"] == "marathon":
                        self.max_42_2km = decimal_to_time(top_speed["duration"])
                        if top_speed["duration"] < self.fastest_max_42_2km:
                                self.fastest_max_42_2km = top_speed["duration"]
                                self.fastest_42_2km_date = self.date


    def append_data_to_dict(self):
        if self.distance != "0":
            self.export_dict['start_time'].append(self.start_time)
            self.export_dict['end_time'].append(self.end_time)
            self.export_dict['duration'].append(self.duration)
            self.export_dict['duration_decimal'].append(self.duration_decimal)
            self.export_dict['calories'].append(self.calories)
            self.export_dict['distance'].append(self.distance)
            self.export_dict['max_heart_rate'].append(self.max_heart_rate)
            self.export_dict['ave_heart_rate'].append(self.ave_heart_rate)
            self.export_dict['average_speed'].append(self.average_speed)
            self.export_dict['average_pace'].append(self.average_pace)
            self.export_dict['max_speed'].append(self.max_speed)
            self.export_dict['max_1km'].append(self.max_1km)
            self.export_dict['max_5km'].append(self.max_5km)
            self.export_dict['max_10km'].append(self.max_10km)
            self.export_dict['max_21_1km'].append(self.max_21_1km)
            self.export_dict['max_42_2km'].append(self.max_42_2km)
            self.num_of_running_files += 1

    def get_data(self):
        self.create_files_list()
        for file in self.files_in_dir:
            self.reset_data()
            with open(self.json_files_path + "\\" + file, 'r', encoding="utf8") as json_data:
                self.json_data_contect = json.load(json_data)
            self.sport_type_id = f'{self.json_data_contect["sport_type_id"]}'
            if self.sport_type_id == "1":
                self.time_and_distance()
                self.distance_and_heart_rate()
                self.speed_and_pace()
                self.fastest_segments()
                self.append_data_to_dict()
                #
                if DEBUG == 2:
                    print("*" * 30 + f"{file: ^73}" + 30 * "*")
                if DEBUG > 1:
                    print(self.print_data())
        if DEBUG == 1:
            distance_float = [float(x) for x in self.export_dict['distance']]
            duration_decimal = [float(y) for y in self.export_dict['duration_decimal']]
            print(f"Total distance: \t\t{'%.2f' % (sum(distance_float)):>5}")
            total_duration = sum(distance_float)
            hours = int(floor(total_duration) / 60)
            minutes = floor(total_duration) % 60
            seconds = floor((total_duration - int(total_duration)) * 60)
            print(f"Total duration: \t\t{hours:0>2}:{minutes:0>2}:{seconds:0>2}")
            print(f"Total average pace: \t{'%.2f' % (60*(sum(distance_float)/sum(duration_decimal))):>5}")
            # print(f"Total average speed:\t{'%.2f' % (sum(duration_decimal)/sum(distance_float)):>5}")
            ave_speed_dec = (sum(duration_decimal)/sum(distance_float))
            minutes = int(ave_speed_dec)
            seconds = '%2.0f' % ((ave_speed_dec % minutes) * 60)
            print(f"Total average speed:\t{minutes :>2}:{seconds :0>2}")
            fastest_max_10km_time = decimal_to_time(self.fastest_max_10km)
            print(f"Fastest 10Km:\t\t\t{fastest_max_10km_time} @ {self.fastest_10km_date}")
            fastest_max_21_1km_time = decimal_to_time(self.fastest_max_21_1km)
            print(f"Fastest 21.1Km:\t\t\t{fastest_max_21_1km_time} @ {self.fastest_21_1km_date}")
            fastest_max_42_2km_time = decimal_to_time(self.fastest_max_42_2km)
            print(f"Fastest 42.2Km:\t\t\t{fastest_max_42_2km_time} @ {self.fastest_42_2km_date}")

        if DEBUG > 2:
            for key, data in self.export_dict.items():
                print(key, data, len(data))
        df = pd.DataFrame(self.export_dict, columns=self.excel_columns)
        if DEBUG > 3:
            print(df)

    def print_data(self):
        if self.sport_type_id == "1":
            return "start_time\t\t" + self.start_time \
                   + "\nend_time\t\t" + self.end_time \
                   + "\nduration\t\t" + self.duration \
                   + "\ncalories\t\t" + self.calories \
                   + "\ndistance [Km]\t" + self.distance \
                   + "\nave_heart_rate\t" + self.ave_heart_rate \
                   + "\nmax_heart_rate\t" + self.max_heart_rate \
                   + "\naverage_speed\t" + self.average_speed \
                   + "\naverage_pace\t" + self.average_pace \
                   + "\nmax_speed\t\t" + self.max_speed \
                   + "\n1km     -->\t\t" + self.max_1km \
                   + "\n5km     -->\t\t" + self.max_5km \
                   + "\n10km    -->\t\t" + self.max_10km \
                   + "\n21_1km  -->\t\t" + self.max_21_1km \
                   + "\n42_2km  -->\t\t" + self.max_42_2km
        else:
            return "Not a running activity"

    def export_to_csv(self):
        now = datetime.datetime.now()
        self.date_for_file = now.strftime('%Y-%m-%d_T_%H_%M_%S')
        df = pd.DataFrame(self.export_dict, columns=self.excel_columns)
        df.to_csv(self.output_path + self.date_for_folder + r'/' + self.date_for_file + '_Runtastic_Boaz.csv', index=False, header=True)
        # print("=====", self.output_path + self.date_for_folder + r'/' + self.date_for_file + '_Runtastic_Boaz.csv')
        print("Number of 'running' files =", f'{self.num_of_running_files:^18}')
        print("Generated Runtastic CSV path:\t", self.output_path[:-1] + self.date_for_folder +
              '\nCSV File Name:\t\t\t\t\t', self.date_for_file + '_Runtastic_Boaz.csv')
        print(120 * '-')

    def start_time_message(self):
        now = datetime.datetime.now()
        print(120 * '-')
        print(now.strftime('%Y-%m-%d_@_%H:%M:%S'), 'Start processing')
        print(120 * '-')

    def end_time_message(self):
        now = datetime.datetime.now()
        print(now.strftime('%Y-%m-%d_@_%H:%M:%S'), 'CSV is ready')
        print(120 * '-')

    def execute(self):
        self.start_time_message()
        self.create_output_folder()
        self.get_data()
        self.export_to_csv()
        self.end_time_message()

    def __str__(self):
        if self.sport_type_id == "1":
            distance_float = [float(x) for x in self.export_dict['distance']]
            duration_decimal = [float(y) for y in self.export_dict['duration_decimal']]
            # print(f"Total distance: \t\t{'%.2f' % (sum(distance_float)):>5}")
            total_duration_dec = sum(duration_decimal)
            hours = int(floor(total_duration_dec) / 60)
            minutes = floor(total_duration_dec) % 60
            seconds = floor((total_duration_dec - int(total_duration_dec)) * 60)
            total_duration_time = f"{int(hours/24)} days and {(hours % 24):0>2}:{minutes:0>2}:{seconds:0>2} --> " + \
                                  f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"
            # total_duration_time = f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"
            # print(f"Total duration: \t\t{total_duration_time}")
            average_pace = f"{'%.2f' % (60 * (sum(distance_float) / sum(duration_decimal))):>5}"
            # print(f"Total average pace: \t{average_pace}")
            # print(f"Total average speed:\t{'%.2f' % (sum(duration_decimal)/sum(distance_float)):>5}")
            ave_speed_dec = (sum(duration_decimal) / sum(distance_float))
            minutes = int(ave_speed_dec)
            seconds = '%2.0f' % ((ave_speed_dec % minutes) * 60)
            average_speed = f"{minutes :>2}:{seconds :0>2}"
            # print(f"Total average speed:\t{average_speed}")
            fastest_max_10km_time = decimal_to_time(self.fastest_max_10km)
            # print(f"Fastest 10Km:\t\t\t{fastest_max_10km_time} @ {self.fastest_10km_date}")
            fastest_max_21_1km_time = decimal_to_time(self.fastest_max_21_1km)
            # print(f"Fastest 21.1Km:\t\t\t{fastest_max_21_1km_time} @ {self.fastest_21_1km_date}")
            fastest_max_42_2km_time = decimal_to_time(self.fastest_max_42_2km)
            # print(f"Fastest 42.2Km:\t\t\t{fastest_max_42_2km_time} @ {self.fastest_42_2km_date}")


            return f"Total distance: \t\t{'%.2f' % (sum(distance_float)):>5} Km\n" \
                   + f"Total duration: \t\t{total_duration_time}\n"\
                   + f"Total average pace: \t{average_pace} Km/h\n"\
                   + f"Total average speed:\t{average_speed} min/Km\n"\
                   + f"{'  Fastest runs:  ':*^45}\n"\
                   + f"Fastest 10Km:\t\t\t{fastest_max_10km_time} @ {self.fastest_10km_date}\n"\
                   + f"Fastest 21.1Km:\t\t\t{fastest_max_21_1km_time} @ {self.fastest_21_1km_date}\n"\
                   + f"Fastest 42.2Km:\t\t\t{fastest_max_42_2km_time} @ {self.fastest_42_2km_date}\n" \
                   + f"{45 * '*'}"
        else:
            return "Error"


def read_runtastic_json():
    with open(json_file, 'r', encoding="utf8") as json_data:
        json_data_contect = json.load(json_data)

    # type(json_data_contect) = <class 'dict'>
    # print(json_data_contect)

    # json_formated = json.dumps(json_data_contect, indent=4)
    # type(json_formated) = <class 'str'>
    # print(json_formated)

    print("\n" + "*" * 80 + "\n" + "*" * 80 + "\n" + "*" * 80 + "\n")
    print("start_time\t", json_data_contect["start_time"])
    print("end_time\t", json_data_contect["end_time"])
    print("duration\t", json_data_contect["duration"])

    print("start_time\t", json_data_contect["start_time"], "\t",
          strftime('%Y-%m-%d %H:%M:%S', localtime(json_data_contect["start_time"] / 1000)))
    print("end_time\t", json_data_contect["end_time"], "\t",
          strftime('%Y-%m-%d %H:%M:%S', localtime(json_data_contect["end_time"] / 1000)))
    duration_h = int(floor(json_data_contect["duration"] / 60000) / 60)
    duration_min = floor(json_data_contect["duration"] / 60000) % 60
    duration_sec = '%.0f' % (
                (json_data_contect["duration"] / 60000 - floor(json_data_contect["duration"] / 60000)) * 60)
    print("duration\t", json_data_contect["duration"], "\t\t",
          f"{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}")

    # print("created_at\t", json_data_contect["created_at"], "\t", strftime('%Y-%m-%d %H:%M:%S',
    #                                                                       localtime(json_data_contect["created_at"]/1000)))
    #
    # print("updated_at\t", json_data_contect["updated_at"], "\t", strftime('%Y-%m-%d %H:%M:%S',
    #                                                                       localtime(json_data_contect["updated_at"]/1000)))
    print("calories\t", f'{json_data_contect["calories"]}')
    #
    print("sport_type_id\t", json_data_contect["sport_type_id"])

    # print(json_data_contect["features"][-1])

    for dicts in json_data_contect["features"]:
        if "type" in dicts and "initial_values" in dicts['type']:
            duration_h = int(floor(dicts["attributes"]["duration"] / 60000) / 60)
            duration_min = floor(dicts["attributes"]["duration"] / 60000) % 60
            duration_sec = '%.0f' % (
                    (dicts["attributes"]["duration"] / 60000 - floor(dicts["attributes"]["duration"] / 60000)) * 60)
            print("duration\t\t", dicts["attributes"]["duration"], "\t\t",
                  f"{duration_h:0>2}:{duration_min:0>2}:{duration_sec:0>2}")
            print("distance [Km]\t\t", f'{dicts["attributes"]["distance"] / 1000}')
            print("sport_type_id\t", dicts["attributes"]["sport_type"]["id"])

    for dicts in json_data_contect["features"]:
        if "type" in dicts and "track_metrics" in dicts['type']:
            speed_factor = 3600 / 1000
            # average_speed
            print("average_speed raw\t", dicts["attributes"]["average_speed"])
            ave_speed = float(dicts["attributes"]["average_speed"]) * speed_factor
            print("average_speed\t\t", f"{('%.2f' % ave_speed):0>5}")
            # average_pace = min_per_km
            print("average_pace raw\t", dicts["attributes"]["average_pace"])
            minutes = (float(dicts["attributes"]["average_pace"]) * (1000 / 60))
            seconds = floor((minutes - int(minutes)) * 60)
            print("average_pace\t\t", f"00:{int(minutes):0>2}:{seconds:0>2}")
            # max_speed
            print("max_speed raw\t\t", dicts["attributes"]["max_speed"])
            max_speed = float(dicts["attributes"]["max_speed"]) * speed_factor
            print("max_speed\t\t\t", f"{('%.2f' % max_speed):0>5}")

    top_1km, top_5km, top_10km, top_21_1km, top_42_2km = 0, 0, 0, 0, 0
    for dicts in json_data_contect["features"]:
        if "type" in dicts and "fastest_segments" in dicts['type']:
            print("segments\t", dicts["attributes"]["segments"])
            for top_speed in dicts["attributes"]["segments"]:
                if "1km" in top_speed["distance"]:
                    print("1km raw", top_speed["duration"])
                    print("1km sec_dec",
                          '%.2f' % (((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60))
                    minutes = (int(top_speed["duration"] / 60000))
                    print("1km min", minutes)
                    seconds = floor(((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60)
                    print("1km sec", seconds)
                    print("1km -->", f"00:{minutes :0>2}:{seconds :0>2}")
                    top_1km = 1
                if "5km" in top_speed["distance"]:
                    print("5km raw", top_speed["duration"])
                    print("5km sec_dec",
                          '%.2f' % (((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60))
                    minutes = (int(top_speed["duration"] / 60000))
                    print("5km min", minutes)
                    seconds = floor(((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60)
                    print("5km sec", seconds)
                    print("5km -->", f"00:{minutes :0>2}:{seconds :0>2}")
                    top_5km = 1
                if "10km" in top_speed["distance"]:
                    print("10km raw", top_speed["duration"])
                    print("10km sec_dec",
                          '%.2f' % (((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60))
                    minutes = (int(top_speed["duration"] / 60000))
                    print("10km min", minutes)
                    seconds = floor(((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60)
                    print("10km sec", seconds)
                    print("10km -->", f"00:{minutes :0>2}:{seconds :0>2}")
                    top_10km = 1
                if "half_marathon" in top_speed["distance"]:
                    print("21_1km raw", top_speed["duration"])
                    print("21_1km sec_dec",
                          '%.2f' % (((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60))
                    hours = int(floor(top_speed["duration"] / 60000) / 60)
                    print("21_1km hour", hours)
                    minutes = floor(top_speed["duration"] / 60000) % 60
                    # minutes = (int(top_speed["duration"]/60000))
                    print("21_1km min", minutes)
                    seconds = floor(((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60)
                    print("21_1km sec", seconds)
                    print("21_1km -->", f"{hours :0>2}:{minutes :0>2}:{seconds :0>2}")
                    top_21_1km = 1
                if "marathon" in top_speed["distance"]:
                    print("42_2km raw", top_speed["duration"])
                    print("42_2km sec_dec",
                          '%.2f' % (((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60))
                    hours = int(floor(top_speed["duration"] / 60000) / 60)
                    print("42_2km hour", hours)
                    minutes = floor(top_speed["duration"] / 60000) % 60
                    # minutes = (int(top_speed["duration"]/60000))
                    print("42_2km min", minutes)
                    seconds = floor(((top_speed["duration"] / 60000) - int(top_speed["duration"] / 60000)) * 60)
                    print("42_2km sec", seconds)
                    print("42_2km -->", f"{hours :0>2}:{minutes :0>2}:{seconds :0>2}")
                    top_42_2km = 1
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
    for dicts in json_data_contect["features"]:
        if "type" in dicts and "heart_rate" in dicts['type']:
            print("ave_heart_rate\t", f'{dicts["attributes"]["average"]}')
            print("max_heart_rate\t", f'{dicts["attributes"]["maximum"]}')
            heart_rate_flag = 1
    if heart_rate_flag == 0:
        print("heart_rate average\t", 0)
        print("heart_rate maximum\t", 0)
    print("\n" + "*" * 80 + "\n" + "*" * 80 + "\n" + "*" * 80 + "\n")


analyze_data = Runtastic_Data_To_Csv(_files_path=PATH, _output_path=OUTPUT_DIR_LOCATION)
analyze_data.execute()

print(analyze_data)

# read_runtastic_json()
