import datetime
import os
import pandas as pd

import read_runtastic_json
from matplotlib import pyplot as plt

decimal_to_time = read_runtastic_json.decimal_to_time
PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20241103-000\Sport-sessions\\'
OUTPUT_DIR_LOCATION = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Excel_and_CSV_new\\'  # _output_path


def decimal_duration_to_time(duration):
    hours = int(int(duration) / 60)
    minutes = int(duration) % 60
    seconds = int((duration - int(duration)) * 60)
    return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2} --> " + \
           f"{int(hours / 24)} days and {(hours % 24):0>2}:{minutes:0>2}:{seconds:0>2}"


class runtastic_data_filter(read_runtastic_json.Runtastic_Data_To_Csv):
    def create_main_dataframe(self):
        self.start_time_message()
        # self.create_output_folder()
        self.get_data()
        self.create_raw_dataframe_form_list()
        # self.end_time_data_summary_message()

    def per_year_distance(self, _year):
        """
        :param _year: STR, Ex. '2024'
        :return: float, total running Km in a year
        """
        year_distance = self.df[self.df["start_time"].str.contains(str(_year))][["distance"]].astype(float)
        total_running_km = year_distance['distance'].sum()
        return total_running_km

    def per_every_year_distance(self, start_year="2014"):
        """
        :param start_year: str of starting year; defaulted to '2014'
        :return: pandas DataFrame [pd.DataFrame] of 'year' and 'Distance (per year)' columns from 2014 to today's year
        """
        now = int(datetime.datetime.now().strftime('%Y'))
        # start_year = "2014"
        out = []
        dist_list = []
        year_list = []
        start_year = int(start_year)
        while start_year <= now:
            yearly_dist = float('%.2f' % self.per_year_distance(start_year))
            year = start_year
            out.append([year, float(yearly_dist)])
            dist_list.append(yearly_dist)
            year_list.append(year)
            start_year = start_year + 1
        data = {'year': year_list, 'Distance': dist_list}
        yearly_dist_df = pd.DataFrame(data, columns=['year', 'Distance'])
        return yearly_dist_df

    def plot_per_every_year_distance(self, plot_save_format='jpg'):
        """
        :param plot_save_format: plot file type: png, pdf, jpg, svg
        :return: plot file name and current directory
        """
        dist_df = self.per_every_year_distance()
        # data plot
        ax = dist_df.plot(x='year', y='Distance', alpha=0.9, kind='bar', color='skyblue')
        # labels and title
        plt.xlabel('Year')
        plt.ylabel('Distance [km]')
        plt.title('Running distance per Year')
        for i, value in enumerate(dist_df['Distance']):
            ax.text(i, value + 0.2, str(value), ha='center', va='bottom', rotation=25)
        # Show the plot
        # plt.show() # block=False)
        if not os.path.exists('plots'):
            os.makedirs('plots')
        plot_date = datetime.datetime.now().strftime('%Y-%m-%d_T_%H_%M_%S')
        plt.savefig(f'plots/histogram_plot_{plot_date}.{plot_save_format}')
        plt.close()
        return f"plot 'histogram_plot_{plot_date}.{plot_save_format}' was saved to {os.getcwd()}\plots"

    def per_every_year_attribute(self, start_year="2014", _attribute='Distance'):
        """
        :param start_year: str of starting year; defaulted to '2014'
        :return: pandas DataFrame [pd.DataFrame] of 'year' and 'attribute (per year)' columns from 2014 to today's year
        """
        now = int(datetime.datetime.now().strftime('%Y'))
        # start_year = "2014"
        out = []
        attr_list = []
        year_list = []
        start_year = int(start_year)
        #
        if _attribute == 'Distance':
            per_year_attr = self.per_year_distance
        elif _attribute == 'calories':
            per_year_attr = self.per_year_calories
        else:
            per_year_attr = self.per_year_distance
        #
        while start_year <= now:
            yearly_attr = float('%.2f' % per_year_attr(start_year))
            year = start_year
            out.append([year, float(yearly_attr)])
            attr_list.append(yearly_attr)
            year_list.append(year)
            start_year = start_year + 1
        data = {'year': year_list, _attribute: attr_list}
        yearly_attr_df = pd.DataFrame(data, columns=['year', _attribute])
        return yearly_attr_df

    def per_year_duration(self, _year):
        """
        :param _year: STR, Ex. '2024'
        :return: str, total days, hours, min, sec of running activities in a year; Ex. 187:14:01 --> 7 days and 19:14:01
        """
        year_duration = self.df[self.df["start_time"].str.contains(str(_year))][["duration_decimal"]].astype(float)
        # yearly_running_duration = decimal_to_time(year_duration['duration_decimal'].sum() * 60000)
        total_duration_dec = year_duration['duration_decimal'].sum()
        return decimal_duration_to_time(total_duration_dec)

    def total_duration(self):
        total_duration = self.df[["duration_decimal"]].astype(float)['duration_decimal'].sum()
        return decimal_duration_to_time(total_duration)

    def per_year_speed(self, _year):
        """
        :param _year: STR, Ex. '2024'
        :return: float, average Km/h in a year
        """
        year_distance = self.df[self.df["start_time"].str.contains(str(_year))][["distance"]].astype(float)
        year_duration = self.df[self.df["start_time"].str.contains(str(_year))][["duration_decimal"]].astype(float)
        if year_duration['duration_decimal'].sum() != 0 or year_distance['distance'].sum() != 0:
            average_speed_km_h = '%.2f' % (
                    year_distance['distance'].sum() / (year_duration['duration_decimal'].sum() / 60))
        else:
            average_speed_km_h = '00.00'
        return average_speed_km_h

    def per_year_pace(self, _year):
        """
        :param _year: STR, Ex. '2024'
        :return: str, average mm:ss per Km in a year
        """
        year_distance = self.df[self.df["start_time"].str.contains(str(_year))][["distance"]].astype(float)
        year_duration = self.df[self.df["start_time"].str.contains(str(_year))][["duration_decimal"]].astype(float)
        if year_duration['duration_decimal'].sum() != 0 or year_distance['distance'].sum() != 0:
            average_pace_min_km = decimal_to_time(
                (year_duration['duration_decimal'].sum() / year_distance['distance'].sum()) * 60000)[3:]
        else:
            average_pace_min_km = '00:00:00'[3:]
        return average_pace_min_km

    def per_year_calories(self, _year):
        """
        :param _year: STR, Ex. '2024'
        :return: int, total calories burned in a year
        """
        year_calories = self.df[self.df["start_time"].str.contains(str(_year))][["calories"]].astype(int)
        total_calories = year_calories['calories'].sum()
        return total_calories

    def per_year_best_10k_list(self, _year, _num_of_runs):
        year_best_10ks = self.df[(self.df["start_time"].str.contains(str(_year))) &
                                 (self.df["distance"].astype(float) > 10)]
        year_best_10ks = year_best_10ks[["duration_decimal"]].astype(float)["duration_decimal"]
        year_best_10ks = year_best_10ks.nsmallest(_num_of_runs)
        year_best_10ks_list = list(year_best_10ks.reset_index()['duration_decimal'])
        temp = len(year_best_10ks_list)
        for i in range(_num_of_runs - temp):
            year_best_10ks_list.append(0)
        for i in range(len(year_best_10ks_list)):
            year_best_10k = decimal_to_time(year_best_10ks_list[i] * 60000)
            if year_best_10k[1] != "0":
                year_best_10ks_list[i] = year_best_10k[1:]
            else:
                year_best_10ks_list[i] = year_best_10k[3:]
        return year_best_10ks_list

    def per_year_best_running(self, _year, _num_of_runs, running_distance="max_10km_dec"):
        """
        :param _year:               str, Ex. '2024'
        :param _num_of_runs:        int, # of best running results.
        :param running_distance:    type of running: "max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"
        :return: running list of    [str: (hh:)mm:ss, str: yyyy-mm-dd, calories burned: int, start_time_dec: int]
        """

        year_best_runs = self.df[(self.df["start_time"].str.contains(str(_year))) &
                                 (self.df[running_distance] != 0)]  # can select different distances here
        year_best_runs = year_best_runs.copy()
        year_best_runs = year_best_runs[[running_distance, "start_time", 'calories', 'start_time_dec']]
        year_best_runs = year_best_runs.nsmallest(_num_of_runs, running_distance)
        year_best_runs[running_distance + '_raw'] = year_best_runs[running_distance]
        year_best_runs_list = year_best_runs.values.tolist()
        temp = len(year_best_runs_list)
        for i in range(_num_of_runs - temp):
            year_best_runs_list.append([0, 0, 0, 0, 0])
        for i in range(len(year_best_runs_list)):
            if year_best_runs_list[i][0] == 0:
                year_best_runs_list[i][0] = 'N/A'
                year_best_runs_list[i][1] = 'N/A'
                year_best_runs_list[i][2] = 'N/A'
                year_best_runs_list[i][3] = 'N/A'
                year_best_runs_list[i][4] = 'N/A'
            else:
                year_best_running = decimal_to_time(year_best_runs_list[i][0])
                if year_best_running[1] != "0":
                    year_best_runs_list[i][0] = year_best_running[1:]
                else:
                    year_best_runs_list[i][0] = year_best_running[3:]
                year_best_runs_list[i][1] = year_best_runs_list[i][1][:10]
        # TODO
        # df = pd.DataFrame(year_best_runs_list, columns=[running_distance,
        #                                                 "start_time", 'calories', 'start_time_dec'])
        return year_best_runs_list

    def per_every_year_best_running(self, _start_year="2014", _num_of_runs=3, running_distance="max_10km_dec"):
        """
        :param _start_year:         default to '2014'
        :param _num_of_runs:        int, # of best running results.
        :param running_distance:    type of running: "max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"
        :return: running list of    list of best running scores of each year
        """
        curr_year = int(_start_year)
        now = int(datetime.datetime.now().strftime('%Y'))
        every_year_best_runs_list = []
        while curr_year <= now:
            every_year_best_runs_list += self.per_year_best_running(_year=curr_year,
                                                                    _num_of_runs=_num_of_runs,
                                                                    running_distance=running_distance)
            curr_year += 1
        # print(every_year_best_runs_list)
        return every_year_best_runs_list

    def plot_per_year_best_running(self, start_year="2014", _num_of_runs=3
                                   , running_distance="max_10km_dec", plot_save_format='jpg'):
        """
        :param start_year:          default to '2014'
        :param _num_of_runs:        int, # of best running results.
        :param running_distance:    type of running: "max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"
        :param plot_save_format:    plot file type: png, pdf, jpg, svg
        :return:
        """
        if '21' in running_distance:
            run, units, color = '21.1Km', '[hh:mm:ss]', '#0cef24'
        elif '42' in running_distance:
            run, units, color = '42.2Km', '[hh:mm:ss]', '#2ac4c4'
        else:
            run, units, color = '10Km', '[mm:ss]', 'skyblue'
        best_running_df = pd.DataFrame(self.per_every_year_best_running(_start_year=start_year,
                                                                        _num_of_runs=_num_of_runs,
                                                                        running_distance=running_distance),
                                       columns=["Duration", "Date", 'calories', 'start_time_dec', "Duration_raw"])
        best_running_df = best_running_df.replace('N/A', pd.NA).dropna(subset=["Duration"]).reset_index()
        best_running_df = best_running_df.drop('index', axis=1)
        best_running_df['Date'] = pd.to_datetime(best_running_df['Date'], format='%Y-%m-%d', errors='coerce')
        best_running_df['start_time'] = (best_running_df['start_time_dec'] / 1000) + 7200   # adjust to ISR time
        best_running_df['start_time'] = pd.to_datetime(best_running_df['start_time'], unit='s')
        print(best_running_df)
        best_running_df = best_running_df.dropna(subset=['Date'])
        ax = best_running_df.plot(x='start_time', y='Duration_raw', kind='bar',
                                  color=color, figsize=(12, 6), label="Duration")
        #
        plt.yticks([])
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.xlabel('Date')
        plt.ylabel(f'Duration {units}')
        plt.title(f'fastest {run} per every Year')
        if running_distance == "max_10km_dec":
            n = 3
        else:
            n = 0
        for i, value in enumerate(best_running_df['Duration_raw']):
            ax.text(i, value - 0.2, str(decimal_to_time(value))[n:], ha='center', va='bottom', rotation=65)
        # Manually set y-limits
        plt.ylim(min(best_running_df['Duration_raw']) - 350000, max(best_running_df['Duration_raw']) + 470000)
        # plt.show()
        if not os.path.exists('plots'):
            os.makedirs('plots')
        plot_date = datetime.datetime.now().strftime('%Y-%m-%d_T_%H_%M_%S')
        plt.savefig(f'plots/best_{run}_histogram_plot_{plot_date}.{plot_save_format}', bbox_inches='tight', dpi=300, pad_inches=0.3)
        plt.close()
        return f"plot 'best_{run}_histogram_plot_{plot_date}.{plot_save_format}' was saved to {os.getcwd()}\plots"

    def per_year_longest_running(self, _year, _num_of_runs):
        """
        :param _year:               str, Ex. '2024'
        :param _num_of_runs:        int
        :return: running list of    [str: kk:mm, str: yyyy-mm-dd]
        """
        year_longest_runs = self.df[(self.df["start_time"].str.contains(str(_year)))]
        year_longest_runs = year_longest_runs.copy()
        year_longest_runs["distance"] = year_longest_runs["distance"].astype(float)
        year_longest_runs = year_longest_runs[["distance", "start_time"]]
        year_longest_runs = year_longest_runs.nlargest(_num_of_runs, "distance")
        year_longest_runs_list = year_longest_runs.values.tolist()
        temp = len(year_longest_runs_list)
        for i in range(_num_of_runs - temp):
            year_longest_runs_list.append([0, 0])
        for i in range(len(year_longest_runs_list)):
            if year_longest_runs_list[i][0] == 0:
                year_longest_runs_list[i][0] = 'N/A'
                year_longest_runs_list[i][1] = 'N/A'
            else:
                year_best_10k = year_longest_runs_list[i][0]
                year_longest_runs_list[i][0] = year_best_10k
                year_longest_runs_list[i][1] = year_longest_runs_list[i][1][:10]
        return year_longest_runs_list


if __name__ == "__main__":
    test = runtastic_data_filter(_files_path=PATH, _output_path=OUTPUT_DIR_LOCATION)
    test.create_main_dataframe()
    print(f"Distance: {test.per_year_distance('2024')} Km")
    print(f"Duration: {test.per_year_duration('2024')}")
    print(f"Pace:     {test.per_year_pace('2022')} mm:ss")
    print(f"Speed:    {test.per_year_speed('2022')} Km/h")
    print(f"Calories: {test.per_year_calories('2022')} Cal")
    print("*" * 50)
    print(f"Total Duration: {test.total_duration()} mm:ss")
    print("*" * 50)

    X = test.per_year_best_running("2024", 5)
    for i, item in enumerate(X):
        print(f"{i + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}")
    print("*" * 50)

    X = test.per_year_best_running("2023", 3, "max_21_1km_dec")
    for i, item in enumerate(X):
        print(f"{i + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}")
    print("*" * 50)

    X = test.per_year_best_running("2024", 3, "max_42_2km_dec")
    for i, item in enumerate(X):
        print(f"{i + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}, Calories burned: {item[2]:^6}")
    print("*" * 50)

    X = test.per_every_year_best_running()
    for i, item in enumerate(X):
        print(f"{i + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}, Calories burned: {item[2]:^6}")
    print("*" * 50)

    X = test.per_year_longest_running("2022", 5)
    for i, item in enumerate(X):
        print(f"{i + 1:0>2}) Distance: {item[0]:<7} @ {item[1]:^12}")
    print("*" * 50)

    print(test.per_every_year_attribute(_attribute='calories'))
    print("*" * 50)
    print(test.per_every_year_attribute(_attribute='Distance'))
    print("*" * 50)

    # plots
    print(test.plot_per_every_year_distance())
    print(test.plot_per_year_best_running(running_distance="max_42_2km_dec"))
    print(test.plot_per_year_best_running(running_distance="max_21_1km_dec"))
    print(test.plot_per_year_best_running(running_distance="max_10km_dec"))
    # print(float('00.00'))
