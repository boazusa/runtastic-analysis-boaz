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
        self.create_dataframe_form_list()
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

        now = datetime.datetime.now().strftime('%Y')
        # start_year = "2014"
        out = []
        dist_list = []
        year_list = []
        while int(start_year) <= int(now):
            yearly_dist = float('%.2f' % self.per_year_distance(start_year))
            year = int(start_year)
            out.append([year, float(yearly_dist)])
            dist_list.append(yearly_dist)
            year_list.append(year)
            start_year = int(start_year) + 1
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
        ax = dist_df.plot(x='year', y='Distance', alpha=0.9,  kind='bar', color='skyblue')
        # labels and title
        plt.xlabel('Year')
        plt.ylabel('Distance')
        plt.title('Distance per Year')
        for i, value in enumerate(dist_df['Distance']):
            ax.text(i, value + 0.2, str(value), ha='center', va='bottom')
        # Show the plot
        # plt.show() # block=False)
        if not os.path.exists('plots'):
            os.makedirs('plots')
        plot_date = datetime.datetime.now().strftime('%Y-%m-%d_T_%H_%M_%S')
        plt.savefig(f'plots/histogram_plot_{plot_date}.{plot_save_format}')
        plt.close()
        return f"plot 'histogram_plot_{plot_date}.{plot_save_format}' was saved to {os.getcwd()}\plots"

    def per_year_duration(self, _year):
        """
        :param _year: STR, Ex. '2024'
        :return: str, total days, hours, min, sec of running activities in a year; Ex. 187:14:01 --> 7 days and 19:14:01
        """
        year_duration = self.df[self.df["start_time"].str.contains(str(_year))][["duration_decimal"]].astype(float)
        # yearly_running_duration = decimal_to_time(year_duration['duration_decimal'].sum() * 60000)
        total_duration_dec = year_duration['duration_decimal'].sum()
        return decimal_duration_to_time(total_duration_dec)

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
        :param _num_of_runs:        int
        :param running_distance:    type of running: "max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"
        :return: running list of    [str: (hh:)mm:ss, str: yyyy-mm-dd]
        """

        year_best_runs = self.df[(self.df["start_time"].str.contains(str(_year))) &
                                 (self.df[running_distance] != 0)]  # can select different distances here
        year_best_runs = year_best_runs.copy()
        year_best_runs = year_best_runs[[running_distance, "start_time", 'calories']]
        year_best_runs = year_best_runs.nsmallest(_num_of_runs, running_distance)
        year_best_runs_list = year_best_runs.values.tolist()
        temp = len(year_best_runs_list)
        for i in range(_num_of_runs - temp):
            year_best_runs_list.append([0, 0])
        for i in range(len(year_best_runs_list)):
            if year_best_runs_list[i][0] == 0:
                year_best_runs_list[i][0] = 'N/A'
                year_best_runs_list[i][1] = 'N/A'
            else:
                year_best_running = decimal_to_time(year_best_runs_list[i][0])
                if year_best_running[1] != "0":
                    year_best_runs_list[i][0] = year_best_running[1:]
                else:
                    year_best_runs_list[i][0] = year_best_running[3:]
                year_best_runs_list[i][1] = year_best_runs_list[i][1][:10]
        return year_best_runs_list

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
        print(f"{i + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}")
    print("*" * 50)

    X = test.per_year_longest_running("2022", 5)
    for i, item in enumerate(X):
        print(f"{i + 1:0>2}) Distance: {item[0]:<7} @ {item[1]:^12}")
    print("*" * 50)

    print(test.per_every_year_distance())
    print(test.plot_per_every_year_distance())

