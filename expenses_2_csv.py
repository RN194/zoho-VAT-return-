import sys
import csv
import requests
import json
import logins
import os.path

refresh_link = "https://accounts.zoho.eu/oauth/v2/token?refresh_token=[ADD REFRESH TOKEN HERE]&client_id=[ADD CLIENT ID HERE]&client_secret=[ADD CLIENT SECRET HERE]&redirect_uri=http://localhost&grant_type=refresh_token"

id_list = []


def get_expenses(start, end, auth): 
    token = "Zoho-oauthtoken " + auth

    getter = requests.get("https://books.zoho.eu/api/v3/expenses", headers={'Authorization': token})

    j_data = json.loads(getter.content)['expenses']


    for inv in j_data:
        exp_month = inv['date'].split("-")[1]
        exp_year = inv['date'].split("-")[0]
        if start <= exp_month <= end and exp_year == "2021":
            exp_id = inv['expense_id']
            id_list.append(exp_id)


def get_individual_expense(start, end, auth):
    token = "Zoho-oauthtoken " + auth
    for e_id in id_list:
        url = "https://books.zoho.eu/api/v3/expenses/" + str(e_id)
        sender = requests.get(url, headers={'Authorization': token})
        data_from =  json.loads(sender.content)
        data_extraction(start, end, data_from)


def data_extraction(start, end, data):
    j_data = data['expense']
    vendor_name = j_data['vendor_name']
    acc_name = j_data['line_items'][0]['account_name']
    tax_percentage = j_data['line_items'][0]['tax_percentage']
    tax_amount = j_data['line_items'][0]['tax_amount']
    subtotal = j_data['line_items'][0]['item_total']
    total = tax_amount + subtotal

    header = ["vendor name", "account name", "tax rate", "subtotal", "tax amount", "total"]
    row_details = [vendor_name, acc_name, tax_percentage, subtotal, tax_amount, total]
    fname = start + "-" + end +"_expenses_"+ logins.company_name +"_VAT.csv"
    g_expenses_filename = fname
    if not os.path.exists(fname):
        with open(fname, "a+") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(header)
            out_file.close()

    with open(fname, "a+") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(row_details)
        out_file.close()


def caller(start, end, auth_token):
    get_expenses(start, end, auth_token)
    get_individual_expense(start, end, auth_token)



