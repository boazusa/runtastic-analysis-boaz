import json

# 2014 10k
json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2014-05-28_01-45-23-UTC_55d975a493bc7d05fa586022.json"
# 2022 10k
# json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2022-11-19_18-26-34-UTC_1d91dc28-ffc1-4308-9383-6f93d6c47ace.json"
# Fastest 10k
json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2023-03-24_04-03-54-UTC_52541bd5-6990-4c4e-aba3-62b676c53758.json"

# 2023 10k
# json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2023-03-25_19-30-01-UTC_4ca4691a-62d9-4222-abc4-d395fdc8d119.json"
# 2024 10k
# json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2024-04-21_19-38-40-UTC_92e8cd55-89bc-4b36-8091-4521b9683d47.json"
# Jerusalem Marathon
json_file = r"C:\Users\USER\Documents\Python\Runtastic_script_My_PC\Jsons_for_new_Script\2024-03-08_05-01-39-UTC_b0ba3a9b-a1b9-4bc3-b13c-795d5a2b579e.json"
#
FILE_W_PATH = json_file
# --------------------------------------------------------------------------------------------------------------------

JSON_PATH = r'C:\Users\USER\Documents\Python\Runtastic_script_My_PC\export-20241103-000\Sport-sessions' + '\\'
JSON_FILE = r'2024-10-30_17-57-07-UTC_e09f1bb7-6e71-440f-b4cc-aa0ac8b64904.json'

FILE_W_PATH = JSON_PATH + JSON_FILE

with open(FILE_W_PATH, 'r', encoding="utf8") as json_data:
    json_data_contect = json.load(json_data)

json_formated = json.dumps(json_data_contect, indent=4)

print(json_formated)