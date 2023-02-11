import codecs
import requests 
import pandas as pd
import os
import time

save_html = True
html_file_name  = 'table.html'
excel_file_name = 'table.xlsx'
url = 'https://www.alta.ru/tnved/forbidden_codes/'
period_update = 2  #day
products = ['73040000', '73040001', '73040002'] # list of products

if period_update <= (time.time()-os.path.getmtime('now_time.txt'))/(60*60*24):
	print("Going to download table from " + url)
	r = requests.get(url)
	if save_html:
		print("Saving html page...")
		with codecs.open(html_file_name,'w', 'utf-8') as out:
			out.write(r.text)


tables = pd.read_html(html_file_name) # Returns list of all tables on page
#deleting spaces


def product_is_forbidden(product, mask):
	for i in range(len(mask)):
		if mask[i] != product[i]:
			return False
	return True

df = tables[-1] #returns our table 
forbidden_list = [] 

df_products = pd.read_excel("list.xlsx")
products = df_products["codes"]

for product in products:
    product = str(product).replace(' ','')
    for mask in df['Код']:
        if product_is_forbidden(product, str(mask).replace(' ', '')):
            forbidden_list.append('product ' + product + ' is forbidden by mask ' + mask)
            break

df_stop = pd.DataFrame(forbidden_list)

# my_file = open("now_time.txt", "w+") #insert date and time in file
# my_file.write(str(datetime.now()))
# my_file.close()
print("Exporting to excel...")
dft = df_stop.T
dft.to_excel('stop.xlsx')#save forbidden file

tables[-1].to_excel(excel_file_name)
print("Done!")
