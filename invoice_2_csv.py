import requests
import csv
import json
import expenses_2_csv
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import logins

refresh_link = "https://accounts.zoho.eu/oauth/v2/token?refresh_token=" + logins.r_token + "&client_id=" + logins.c_id + "&client_secret=" + logins.c_secret + "&redirect_uri=http://localhost&grant_type=refresh_token"

# Dict to save invoice ids and numbers
id_map = {}

# variable for names of files created
g_invoice_name = ""
filename = ""
g_expenses_name = ""
exp_filename = ""


def send_email():
    from_add = logins.from_email
    to_add = logins.to_email

    msg = MIMEMultipart()
    msg['From'] = from_add
    msg['To'] = to_add
    msg['Subject'] = logins.company_name + " VAT Returns" + filename
    body_p = MIMEText("Attached are the accounts for the previous 2 months", 'plain')
    msg.attach(body_p)

    with open(g_invoice_name, 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=filename))

    with open(g_expenses_name, 'rb') as file:
        # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=filename))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(logins.email_uname, logins.email_passwd)
    s.sendmail(msg['From'], msg['To'], msg.as_string())


def get_mappings(start, end, auth):
    token = "Zoho-oauthtoken " + auth
    getter = requests.get("https://books.zoho.eu/api/v3/invoices", headers={'Authorization': token})

    j_data = json.loads(getter.content)['invoices']

    for inv in j_data:
        invoice_month = inv['date'].split("-")[1]
        invoice_year = inv['date'].split("-")[0]
        if start <= invoice_month <= end and invoice_year == "2021":
            invoice_id = inv['invoice_id']
            invoice_num = inv['invoice_number']
            id_map[invoice_num] = invoice_id


def get_by_id(start, end, auth):
    token = "Zoho-oauthtoken " + auth
    for key, value in id_map.items():
        url = "https://books.zoho.eu/api/v3/invoices/" + str(value)
        sender = requests.get(url, headers={'Authorization': token})
        data_from = json.loads(sender.content)
        data_extraction(start, end, data_from)

 main() 
def data_extraction(start, end, json_data):
    j_data = json_data['invoice']
    invoice_number = j_data['invoice_number']
    date = j_data['date']
    name = j_data['customer_name']
    status = j_data['status']
    description = j_data['line_items'][0]['name']
    quantity = j_data['line_items'][0]['quantity']
    ppu = j_data['line_items'][0]['rate']
    vat = j_data['line_items'][0]['tax_percentage']
    subtotal = j_data['sub_total']
    tax_total = j_data['tax_total']
    total = j_data['total']

    # list to write to csv
    row_details = [invoice_number, date, name, status, description, quantity, ppu, subtotal, vat, tax_total, total]
    fname = start + "-" + end + "invoices" + logins.company_name + "_VAT.csv"
    with open(fname, "a+") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(row_details)
        out_file.close()


def main():
    start = input("Please enter the start month in form 07: ")
    end = input("Please enter the end month in integer form 07: ")
    full_token = requests.post(refresh_link)
    j_auth = json.loads(full_token.text)
    auth_token = j_auth['access_token']

    get_mappings(start, end, auth_token)
    get_by_id(start, end, auth_token)

    exp = input("Finally, would you like to run the expenses report as well? y or n")
    if exp == "y":
        expenses_2_csv.caller(start, end, auth_token)
    else:
        print("Thank You.")
        return


main()

