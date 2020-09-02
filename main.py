#
#Webpage Scraper
#By: Steve Tran
#A tool used to collect all entries of a site to an excel file for ease of sorting and comparison
#
#Currently tailored to the structure of NewEgg.ca
#_________________________________________________________________________________________

import bs4  #Packages for HTML parsing
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import time
import re   #For extracting elements from a string

#Inputs down below
search_list_url = 'https://www.newegg.ca/p/pl?d=Graphics&page=1'  #The base URL to be scraped
filename = "GraphicsCardSearch.csv"    #The name of the excel file
headers = "Product, Price, Shipping, stock, link\n"    #The name of the column headers separated by commas

#Excel file and column headers created in advance
f = open(filename, "w")
f.write(headers)

#Calling Beautiful Soup to contain the target URL
MasterClient = urlopen(search_list_url)
search_page_html = MasterClient.read()
MasterClient.close()
master_page_soup = soup(search_page_html, "html.parser")

#Selects all master entries in the search list and finds the link to the dedicated page
#This might need to be optimized in the future to improve speed
entry_containers = master_page_soup.findAll("div", {"class": "item-container"})
#print(entry_containers)

#Loop through each container on the search page which was stored in entry_containers
for container in entry_containers:
    time.sleep(3)        #Time delay to prevent block
 
    #Extracts the container with the link
    entry_url_container = container.find("a", {"class": "item-img"})
    entry_link = entry_url_container.get('href')
    print('Parsing', entry_link)    #Notify console of the current entry

    #Parse the dedicated page for information
    ChildClient = urlopen(entry_link)
    child_page_html = ChildClient.read()
    ChildClient.close()
    child_page_soup = soup(child_page_html, "html.parser")

    #Returns a list of strings with the title script
    search_list = child_page_soup.findAll("script")

    #Looks in search_list for key words to find important information. PERIODIC UPDATE REQUIRED IF THE WEBSITE IS UPDATED.
    find_this_text = 'sale'
    for searched_text in search_list:
        searched_text = searched_text.decode()
        if find_this_text in searched_text:
            info_container = searched_text
            break

    #Extract desired information from string
    try:
        product_name = re.search('product_title:(.+?)]', info_container).group(1)
        product_name = product_name.replace(',', '|')
    except AttributeError:
        print("Could not find a title")
    try:
        sale_price = re.search('product_sale_price:(.+?)]', info_container).group(1)
    except AttributeError:
        print("Could not find a sale price")
    try:
        shipping_cost = re.search('product_default_shipping_cost:(.+?)]', info_container).group(1)
    except AttributeError:
        print("Could not find a shipping cost")
    try:
        stock = re.search('product_instock:(.+?)]', info_container).group(1)
    except AttributeError:
        print("Could not find a shipping stock")

    #Simutaneously write the information extracted to the excel file
    f.write(product_name + "," + sale_price + "," +  shipping_cost  + "," + stock + "," + entry_link +"\n")

#Close the excel file so that it can be accessed
print("Success: Script run successfully")
f.close()
