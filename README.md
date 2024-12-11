# 6 Essential Automation Tools Django

1. `dataentry/management/command`:
    - `importdata.py` - import data from the CSV files to the DB     
       Usage: `py manage.py importdata <path_to_csv_file> <model_name>`

2. `dataentry/management/command`:
    - `exportdata.py` - export data from the DB to a CSV file      
       Usage: `py manage.py exportdata <model_name>`
