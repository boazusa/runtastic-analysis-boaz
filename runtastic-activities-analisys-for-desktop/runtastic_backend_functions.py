import datetime
import os
import pandas as pd

import read_runtastic_json
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

print("Current script directory:", os.path.dirname(os.path.abspath(__file__)))
print("Current working directory:", os.getcwd())
decimal_to_time = read_runtastic_json.decimal_to_time
PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20241103-000\Sport-sessions\\'
OUTPUT_DIR_LOCATION = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Excel_and_CSV_new\\'  # _output_path
PDF_SAVE = 1  #


def decimal_duration_to_time(duration):
    hours = int(int(duration) / 60)
    minutes = int(duration) % 60
    seconds = int((duration - int(duration)) * 60)
    return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2} --> " + \
           f"{int(hours / 24)} days and {(hours % 24):0>2}:{minutes:0>2}:{seconds:0>2}"


def decimal_duration_to_time_hh_mm_ss(duration):
    hours = int(int(duration) / 60)
    minutes = int(duration) % 60
    seconds = int((duration - int(duration)) * 60)
    return f"{hours:0>2}:{minutes:0>2}:{seconds:0>2}"


def plot_date():
    return datetime.datetime.now().strftime('%Y-%m-%d_T_%H_%M_%S')

def save_plot(_pdf_p=None, _plt_p=plt, _file_name='', _pdf_msg=''):
    if not os.path.exists('plots'):
        os.makedirs('plots')
    #
    if _pdf_p is not None:
        _pdf_p.savefig(bbox_inches='tight', dpi=300, pad_inches=0.3)  # Save the current plot to the PDF
        _plt_p.close()
        return f"{_pdf_msg:<35}" + " was added to pdf"
    else:
        _plt_p.savefig(f'plots/' + _file_name, bbox_inches='tight', dpi=300, pad_inches=0.3)
        _plt_p.close()
        _file_name += "'"
        return f"plot '{_file_name:<60} was saved to {os.getcwd()}\\plots"


class runtastic_data_filter(read_runtastic_json.Runtastic_Data_To_Csv):
    # def __init__(self, pdf=0):
    #     self.pdf = pdf
    #     super().__init__(_files_path=PATH, _output_path=OUTPUT_DIR_LOCATION)
    #     pass

    def create_main_dataframe(self):
        self.start_time_message()

        # process the activities files into dictionary
        self.get_data()
        # create Pandas dataframe from the activities files into dictionary
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

    def total_distance(self):
        """
        :return: str total running distance logged.
        """
        float_distance = self.df[["distance"]].astype(float)
        total_running_km = float_distance['distance'].sum()
        return '%.2f' % total_running_km  # f"{total_running_km:.2f}"

    def per_year_calories(self, _year):
        """
        :param _year: STR, Ex. '2024'
        :return: int, total calories burned in a year
        """
        year_calories = self.df[self.df["start_time"].str.contains(str(_year))][["calories"]].astype(int)
        total_calories = year_calories['calories'].sum()
        return total_calories

    def total_calories(self):
        """
        :return: str total running burned calories logged.
        """
        int_calories = self.df[["calories"]].astype(int)
        total_calories = int_calories['calories'].sum()
        return total_calories

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
        return float(average_speed_km_h)

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

    def per_every_year_attribute(self, start_year="2014", _attribute='Distance'):
        """
        :param start_year: str of starting year; defaulted to '2014'
        :param _attribute: str - Options: 'Distance / calories / Speed'
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
        elif _attribute == 'Calories':
            per_year_attr = self.per_year_calories
        elif _attribute == 'Speed':
            per_year_attr = self.per_year_speed
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

    def per_every_year_duration(self, _start_year=2014):
        curr_year = int(_start_year)
        now = int(datetime.datetime.now().strftime('%Y'))
        yearly_duration = []
        while curr_year <= now:
            year_duration = self.df[self.df["start_time"].str.contains(str(curr_year))][["duration_decimal"]].astype(
                float)
            # yearly_running_duration = decimal_to_time(year_duration['duration_decimal'].sum() * 60000)
            total_duration = year_duration['duration_decimal'].sum()
            total_duration_dec = float('%.2f' % year_duration['duration_decimal'].sum())
            yearly_duration.append([decimal_duration_to_time_hh_mm_ss(total_duration), total_duration_dec, curr_year])
            curr_year += 1
        return yearly_duration

    def total_duration(self):
        """
        :return: str total running duration logged.
        """
        total_duration = self.df[["duration_decimal"]].astype(float)['duration_decimal'].sum()
        return decimal_duration_to_time(total_duration)

    def per_year_fastest_10k_list(self, _year, _num_of_runs):
        year_fastest_10ks = self.df[(self.df["start_time"].str.contains(str(_year))) &
                                    (self.df["distance"].astype(float) > 10)]
        year_fastest_10ks = year_fastest_10ks[["duration_decimal"]].astype(float)["duration_decimal"]
        year_fastest_10ks = year_fastest_10ks.nsmallest(_num_of_runs)
        year_fastest_10ks_list = list(year_fastest_10ks.reset_index()['duration_decimal'])
        temp = len(year_fastest_10ks_list)
        for i in range(_num_of_runs - temp):
            year_fastest_10ks_list.append(0)
        for i in range(len(year_fastest_10ks_list)):
            year_fastest_10k = decimal_to_time(year_fastest_10ks_list[i] * 60000)
            if year_fastest_10k[1] != "0":
                year_fastest_10ks_list[i] = year_fastest_10k[1:]
            else:
                year_fastest_10ks_list[i] = year_fastest_10k[3:]
        return year_fastest_10ks_list

    def per_year_fastest_running(self, _year, _num_of_runs, running_distance="max_10km_dec"):
        """
        :param _year:               str, Ex. '2024'
        :param _num_of_runs:        int, # of fastest running results.
        :param running_distance:    type of running: "max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"
        :return: running list of    [str: (hh:)mm:ss, str: yyyy-mm-dd, calories burned: int, start_time_dec: int]
        """
        year_fastest_runs = self.df[(self.df["start_time"].str.contains(str(_year))) &
                                    (self.df[running_distance] != 0)]  # can select different distances here
        year_fastest_runs = year_fastest_runs.copy()
        year_fastest_runs = year_fastest_runs[[running_distance, "start_time", 'calories', 'start_time_dec']]
        year_fastest_runs = year_fastest_runs.nsmallest(_num_of_runs, running_distance)
        year_fastest_runs[running_distance + '_raw'] = year_fastest_runs[running_distance]
        year_fastest_runs_list = year_fastest_runs.values.tolist()
        temp = len(year_fastest_runs_list)
        for i in range(_num_of_runs - temp):
            year_fastest_runs_list.append(['N/A', 'N/A', 'N/A', 'N/A', 'N/A'])
        for i in range(len(year_fastest_runs_list)):
            if year_fastest_runs_list[i][0] != 'N/A':
                year_fastest_running = decimal_to_time(year_fastest_runs_list[i][0])
                if year_fastest_running[1] != "0":
                    year_fastest_runs_list[i][0] = year_fastest_running[1:]
                else:
                    year_fastest_runs_list[i][0] = year_fastest_running[3:]
                year_fastest_runs_list[i][1] = year_fastest_runs_list[i][1][:10]
        return year_fastest_runs_list

    def per_every_year_fastest_running(self, _start_year="2014", _num_of_runs=3, running_distance="max_10km_dec"):
        """
        :param _start_year:         default to '2014'
        :param _num_of_runs:        int, # of fastest running results.
        :param running_distance:    type of running: "max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"
        :return: running list of    list of fastest running scores of each year
        """
        curr_year = int(_start_year)
        now = int(datetime.datetime.now().strftime('%Y'))
        every_year_fastest_runs_list = []
        while curr_year <= now:
            every_year_fastest_runs_list += self.per_year_fastest_running(_year=curr_year, _num_of_runs=_num_of_runs,
                                                                          running_distance=running_distance)
            curr_year += 1
        # print(every_year_fastest_runs_list)
        return every_year_fastest_runs_list

    def per_year_longest_running(self, _year, _num_of_runs):
        """
        :param _year:               str, Ex. '2024'
        :param _num_of_runs:        int
        :return: running list of    [str: kk:mm, str: yyyy-mm-dd]
        """
        year_longest_runs = self.df[(self.df["start_time"].str.contains(str(_year)))]
        year_longest_runs = year_longest_runs.copy()
        year_longest_runs["distance"] = year_longest_runs["distance"].astype(float)
        year_longest_runs = year_longest_runs[["distance", "start_time", 'start_time_dec']]
        year_longest_runs = year_longest_runs.nlargest(_num_of_runs, "distance")
        year_longest_runs_list = year_longest_runs.values.tolist()
        year_longest_runs_list.sort(key=lambda x: x[2])
        return year_longest_runs_list

    def per_every_year_longest_running(self, _start_year="2014", _num_of_runs=3):
        curr_year = int(_start_year)
        now = int(datetime.datetime.now().strftime('%Y'))
        every_year_longest_runs_list = []
        while curr_year <= now:
            every_year_longest_runs_list += self.per_year_longest_running(_year=curr_year, _num_of_runs=_num_of_runs)
            curr_year += 1
        return every_year_longest_runs_list

    def plot_per_every_year_attribute(self, plot_save_format='jpg', _attribute='Distance', pdf_p=None):
        """
        :param plot_save_format: plot file type: png, pdf, jpg, svg
        :param _attribute: str - Options: 'Distance / calories / Speed'
        :return: plot file name and current directory
        :param pdf_p:   pdf pointer: to be passed from the 'def save_plot_to_pdf(self)' function, or 'None' if .jpg
        :return: string of file name and path, 'added to pdf', or error if attribute is not in dataframe
        """
        _attribute = _attribute.capitalize()
        attr_df = self.per_every_year_attribute(_attribute=_attribute)
        if _attribute == 'Calories':
            att_ylabel, att_title, att_color = 'Calories [Cal]', 'Calories burned per Year', 'skyblue'
            attr_df[_attribute] = attr_df[_attribute].astype(int)
        elif _attribute == 'Speed':
            att_ylabel, att_title, att_color = 'Speed [km/h]', 'Running Speed per Year', '#fc9100'
        else:
            att_ylabel, att_title, att_color = 'Distance [km]', 'Running Distance per Year', '#25d0e8'

        # data plot
        ax = attr_df.plot(x='year', y=_attribute, alpha=0.9, kind='bar', color=att_color, label=att_ylabel.capitalize())

        # labels and title
        plt.xlabel('Year')
        plt.ylim(0, max(attr_df[_attribute]) * 1.225)
        plt.ylabel(att_ylabel)
        plt.title(att_title)

        # add attribute average line
        if _attribute == 'Speed':
            speed_mean = attr_df[_attribute][attr_df[_attribute] > 0].mean()
            speed_str = '%.2f' % speed_mean
            plt.ylim(0, 16.5)
            plt.axhline(y=speed_mean, color='#ffcb77', label=f'Ave {_attribute}: {speed_str}', linestyle='--')
        plt.legend()

        for i, value in enumerate(attr_df[_attribute]):
            ax.text(i, value + 0.2, str(attr_df[_attribute][i]), ha='center', va='bottom', rotation=25)
        # Show the plot
        # plt.show() # block=False)
        #
        pdf_msg = f"'yearly_" + _attribute.lower() + f"_histogram_plot'"
        file_name = 'yearly_' + _attribute.lower() + f'_histogram_plot_{plot_date()}.{plot_save_format}'
        return save_plot(_pdf_p=pdf_p, _plt_p=plt, _file_name=file_name, _pdf_msg=pdf_msg)

    def plot_per_every_year_duration(self, plot_save_format='jpg', pdf_p=None):
        """
        :param plot_save_format: plot file type: png, pdf, jpg, svg
        :return: plot file name and current directory
        :param pdf_p:   pdf pointer: to be passed from the 'def save_plot_to_pdf(self)' function, or 'None' if .jpg
        :return: string of file name and path, 'added to pdf', or error if attribute is not in dataframe
        """
        duration_list = self.per_every_year_duration()
        duration_df = pd.DataFrame(duration_list, columns=['duration_str', 'duration_dec', 'year'])
        # data plot
        ax = duration_df.plot(x='year', y='duration_dec', alpha=0.9, kind='bar', color='#0f0cef', label='[hhh:mm:ss]')
        # labels and title
        plt.xlabel('Year')
        plt.ylabel('Duration')
        plt.yticks([])
        plt.title('Running Duration per Year')
        for i, value in enumerate(duration_df['duration_dec']):
            ax.text(i, value + 0.2, str(duration_df['duration_str'][i]), ha='center', va='bottom', rotation=25)
        # Show the plot
        # plt.show() # block=False)
        pdf_msg = f"'yearly_duration_histogram_plot'"
        file_name = f'yearly_duration_histogram_plot_{plot_date()}.{plot_save_format}'
        return save_plot(_pdf_p=pdf_p, _plt_p=plt, _file_name=file_name, _pdf_msg=pdf_msg)

    def plot_per_year_fastest_running(self, start_year="2014", _num_of_runs=3,
                                      running_distance="max_10km_dec", plot_save_format='jpg', pdf_p=None):
        """
        :param start_year:          default to '2014'
        :param _num_of_runs:        int, # of fastest running results.
        :param running_distance:    type of running: "max_10km_dec", "max_21_1km_dec", "max_42_2km_dec"
        :param plot_save_format:    plot file type: png, pdf, jpg, svg
        :param pdf_p:   pdf pointer: to be passed from the 'def save_plot_to_pdf(self)' function, or 'None' if .jpg
        :return: string of file name and path, 'added to pdf', or error if attribute is not in dataframe
        """
        if '21' in running_distance:
            run, units, color = '21.1Km', '[hh:mm:ss]', '#0cef24'  # color codes: https://htmlcolorcodes.com/
        elif '42' in running_distance:
            run, units, color = '42.2Km', '[hh:mm:ss]', '#2ac4c4'
        else:
            run, units, color = '10Km', '[mm:ss]', '#36ffda'
        fastest_running_df = pd.DataFrame(self.per_every_year_fastest_running(_start_year=start_year,
                                                                              _num_of_runs=_num_of_runs,
                                                                              running_distance=running_distance),
                                          columns=["Duration", "Date", 'calories', 'start_time_dec', "Duration_raw"])
        fastest_running_df = fastest_running_df.replace('N/A', pd.NA).dropna(subset=["Duration"]).reset_index()
        fastest_running_df = fastest_running_df.drop('index', axis=1)
        fastest_running_df['Date'] = pd.to_datetime(fastest_running_df['Date'], format='%Y-%m-%d', errors='coerce')
        fastest_running_df['start_time'] = (fastest_running_df['start_time_dec'] / 1000) + 7200  # adjust to ISR time
        fastest_running_df['start_time'] = pd.to_datetime(fastest_running_df['start_time'], unit='s')
        fastest_running_df = fastest_running_df.sort_values(by='start_time_dec')
        fastest_running_df = fastest_running_df.dropna(subset=['Date'])
        ax = fastest_running_df.plot(x='start_time', y='Duration_raw', kind='bar',  color=color,
                                     figsize=(max((len(fastest_running_df) + 1) // 2, 4), 6), label="Duration")
        #
        plt.yticks([])
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.xlabel('Date')
        plt.ylabel(f'Duration {units}')
        plt.title(f'fastest {run} running activities per every Year')
        if running_distance == "max_10km_dec":
            n = 3
        else:
            n = 0
        for i, value in enumerate(fastest_running_df['Duration_raw']):
            ax.text(i, value - 0.2, str(decimal_to_time(value))[n:], ha='center', va='bottom', rotation=65)
        # Manually set y-limits
        plt.ylim(min(fastest_running_df['Duration_raw']) - 350000, max(fastest_running_df['Duration_raw']) + 470000)
        # plt.show()
        pdf_msg = f"'fastest_{run}_histogram_plot'"
        file_name = f'fastest_{run}_histogram_plot_{plot_date()}.{plot_save_format}'
        return save_plot(_pdf_p=pdf_p, _plt_p=plt, _file_name=file_name, _pdf_msg=pdf_msg)

    def plot_per_every_year_longest_running(self, _start_year="2014", _num_of_runs=3,
                                            plot_save_format='jpg', pdf_p=None):
        """
        description: plots the '_num_of_runs' of running activities of a selected distance.
        If there are not enough activities of a type, it will plot only these available of that year.
        :param _start_year:         str, Ex. '2024'
        :param _num_of_runs:        int
        :param plot_save_format:    plot file type: png, pdf, jpg, svg
        :param pdf_p:        pdf pointer: to be passed from the 'def save_plot_to_pdf(self)' function, or 'None' if .jpg
        :return:             string of file name and path, 'added to pdf', or error if attribute is not in dataframe
        """
        longest_runs_list = self.per_every_year_longest_running(_start_year=_start_year, _num_of_runs=_num_of_runs)
        longest_runs_df = pd.DataFrame(longest_runs_list, columns=["Distance", "start_time", 'start_time_dec'])
        longest_runs_df['Distance'] = longest_runs_df['Distance'].astype(float).round(2)
        longest_runs_df['start_time'] = (longest_runs_df['start_time_dec'] / 1000) + 7200  # adjust to ISR time
        longest_runs_df['start_time'] = pd.to_datetime(longest_runs_df['start_time'], unit='s')
        longest_runs_df = longest_runs_df.sort_values(by='start_time_dec')
        ax = longest_runs_df.plot(x='start_time', y='Distance', alpha=0.9, kind='bar', color='#ba03bd',
                                  figsize=(max((len(longest_runs_df) + 1) // 2, 4), 6), label='Distance [Km]')
        plt.xlabel('Date')
        plt.ylabel('Distance')
        plt.title(f'Longest {_num_of_runs} running activities per every Year')
        for i, value in enumerate(longest_runs_df['Distance']):
            ax.text(i, value + 0.2, str(value), ha='center', va='bottom', rotation=25)
        # plt.show()
        pdf_msg = f"'longest_running_histogram_plot'"
        file_name = f'longest_running_histogram_plot_{plot_date()}.{plot_save_format}'
        return save_plot(_pdf_p=pdf_p, _plt_p=plt, _file_name=file_name, _pdf_msg=pdf_msg)

    def save_plot_to_pdf(self):
        """
        Generated pdf document with all available plots
        :return: success/fail message
        """
        pdf_date = datetime.datetime.now().strftime('%Y-%m-%d_T_%H_%M_%S')
        if PDF_SAVE:
            with PdfPages(f'plots/analysis_plots_{pdf_date}.pdf') as pdf:
                print('***', self.plot_per_every_year_attribute(_attribute='Distance', pdf_p=pdf), '***')
                print('***', self.plot_per_every_year_attribute(_attribute='Calories', pdf_p=pdf), '***')
                print('***', self.plot_per_every_year_duration(pdf_p=pdf), '***')
                print('***', self.plot_per_every_year_attribute(_attribute='Speed', pdf_p=pdf), '***')
                print('***', self.plot_per_every_year_longest_running(pdf_p=pdf), '***')
                print('***', self.plot_per_year_fastest_running(running_distance="max_10km_dec", pdf_p=pdf), '***')
                print('***', self.plot_per_year_fastest_running(running_distance="max_21_1km_dec", pdf_p=pdf), '***')
                print('***', self.plot_per_year_fastest_running(running_distance="max_42_2km_dec", pdf_p=pdf), '***')
            return f"Document 'analysis_plots_{pdf_date}.pdf' was saved to {os.getcwd()}\\plots"
        else:
            return f"Saving plots to pdf is disabled"


if __name__ == "__main__":
    test = runtastic_data_filter(_files_path=PATH, _output_path=OUTPUT_DIR_LOCATION)
    test.create_main_dataframe()
    print(f"Distance: {test.per_year_distance('2024')} Km")
    print(f"Duration: {test.per_year_duration('2024')}")
    print(f"Pace:     {test.per_year_pace('2022')} mm:ss")
    print(f"Speed:    {test.per_year_speed('2022')} Km/h")
    print(f"Calories: {test.per_year_calories('2022')} Cal")
    print("*" * 60)
    print(f"Total Distance: {test.total_distance()} Km")
    print(f"Total Duration: {test.total_duration()} hh:mm:ss")
    print(f"Total Calories: {test.total_calories()} kCal")
    print("*" * 60)

    X = test.per_year_fastest_running("2024", 5)
    for ind, item in enumerate(X):
        print(f"{ind + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}")
    print("*" * 60)

    X = test.per_year_fastest_running("2023", 3, "max_21_1km_dec")
    for ind, item in enumerate(X):
        print(f"{ind + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}")
    print("*" * 60)

    X = test.per_year_fastest_running("2024", 3, "max_42_2km_dec")
    for ind, item in enumerate(X):
        print(f"{ind + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}, Calories burned: {item[2]:^6}")
    print("*" * 60)

    X = test.per_every_year_fastest_running()
    for ind, item in enumerate(X):
        print(f"{ind + 1:0>2}) duration: {item[0]:^7} @ {item[1]:^12}, Calories burned: {item[2]:^6}")
    print("*" * 60)

    X = test.per_year_longest_running("2024", 5)
    for ind, item in enumerate(X):
        print(f"{ind + 1:0>2}) Distance: {item[0]:<7} @ {item[1]:^12}")
    print("*" * 60)
    # print(test.per_every_year_longest_running())
    # print("*" * 60)
    # print(test.per_every_year_attribute(_attribute='calories'))
    # print("*" * 60)
    # print(test.per_every_year_attribute(_attribute='Distance'))
    # print("*" * 60)
    # print(test.per_every_year_attribute(_attribute='Speed'))
    # print("*" * 60)

    # plots
    print(test.plot_per_every_year_attribute(_attribute='Distance'))
    print(test.plot_per_every_year_attribute(_attribute='calories'))
    print(test.plot_per_every_year_duration())
    print(test.plot_per_every_year_attribute(_attribute='Speed'))
    print(test.plot_per_year_fastest_running(running_distance="max_10km_dec"))
    print(test.plot_per_year_fastest_running(running_distance="max_21_1km_dec"))
    print(test.plot_per_year_fastest_running(running_distance="max_42_2km_dec"))
    print(test.plot_per_every_year_longest_running())
    # plots pdf
    print(test.save_plot_to_pdf())
