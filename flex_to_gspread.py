from datetime import datetime
from os import environ

import gspread
from gspread.worksheet import ValueInputOption

import flex_report as fr

token = environ['FLEX_TOKEN']
query_id = environ['FLEX_QUERY_ID']

# Reference code is generated upon successful request
reference_code = fr.fetch_reference_code(token, query_id)
trades_df = fr.fetch_data(token, reference_code)

# Exclude entries where subcategory is empty
trades_df = trades_df[trades_df['@subCategory'] != '']

if trades_df is not None:
    print(trades_df)
else:
    print('Failed to retrieve data from the API.')

# Connect to Google Sheets
sa = gspread.service_account(filename='credentials.json')

# Locate the spreadsheet and worksheet
sheet = sa.open('Portfolio Performance')
current_year = datetime.now().year
worksheet = sheet.worksheet(str(current_year))

# Write the whole df to the worksheet starting A1 replacing existing values
title_row = [trades_df.columns.values.tolist()]
other_rows = trades_df.values.tolist()
worksheet.update(title_row + other_rows,
                 value_input_option=ValueInputOption.user_entered)
