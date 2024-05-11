import gspread
from google.oauth2.service_account import Credentials

import os
from dotenv import load_dotenv

load_dotenv()

token= os.getenv('SHEED_ID')

scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("cred.json", scopes=scopes)

client = gspread.authorize(creds)

sheed_id = token
workbook = client.open_by_key(sheed_id)

def add_spend(type_spend,summ, category, time_spend, worksheet="May"):
    sheets = workbook.worksheet(worksheet)
    i = 13
    while sheets.cell(i,3).value != None:
        i += 1
    sheets.update_cell(i,1, type_spend) 
    sheets.update_cell(i,2, time_spend) 
    sheets.update_cell(i,3, summ) 
    sheets.update_cell(i,4, category) 

def add_income(type_income,summ, category, time_spend, worksheet="May"):
    sheets = workbook.worksheet(worksheet)
    i = 13
    while sheets.cell(i,8).value != None:
        i += 1
    sheets.update_cell(i,6, type_income) 
    sheets.update_cell(i,7, time_spend) 
    sheets.update_cell(i,8, summ) 
    sheets.update_cell(i,9, category) 
