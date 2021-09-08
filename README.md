# zoho-VAT-return-
This is a program that allows the user to use Zoho's REST API to scrape their invoice and purchase data for VAT return filing.

##USAGE
irst, you need to create a file named 'logins.py' in the same folder as the other files.
This file must contain the following:
	r_token = ""
	c_id = ""
	c_secret = ""
	from_email = ""
	to_email = ""
	email_uname = ""
	email_passwd = ""
	company_name = ""

Insert your refresh token between the "" for r_token, your client id between "" for c_id and finally your client secret between "" for c_secret.
If you change any of the names above, they will also need to be changed in the invoice_2_csv and expenses_2_csv files also.

Run invoice_2_csv.py with the command python3 invoice_2_csv.py, and answer the questions.
If all runs correctly, you should have the corresponding csv files in your folder.

