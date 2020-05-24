'''
Webpage Scraper
-By: Steve Tran
A tool used to collect all entries of a site to an excel file for ease of sorting and comparison

Currently tailored to the structure of NewEgg.ca
_________________________________________________________________________________________'''
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


'''Inputs down below_____________________________________________________________________'''
parse_this_url = 'https://www.newegg.ca/Video-Cards-Video-Devices/Category/ID-38'  #The URL to be scraped
filename = "Graphic.csv"    #The name of the excel file
headers = "brand, product_name, shipping\n"    #The name of the column headers separated by commas


'''Code body below_______________________________________________________________________'''

'''Excel file and column headers created in advance'''
f = open(filename, "w")
f.write(headers)

'''Calling Beautiful Soup to contain the target URL'''
uClient = uReq(parse_this_url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html, "html.parser")

'''Selects all master entries in the search list and stores it in a list of informative entries'''
'''This might need to be optimized in the future to improve speed'''
entry_containers = page_soup.findAll("div", {"class": "item-container"})


'''Loop through each container in entry_containers'''
'''Write the information from each container to one row of the excel file at a time'''
for container in entry_containers:

    '''find Product Title'''
    product_title_container = container.find("a", {"class", "item-title"})
    product_title = product_title_container.text

    '''find Product Brand'''
    brand_title_container = container.find("a", {"class", "item-brand"})
    brand_title = brand_title_container.img["title"]

    '''Find Shipping Price'''
    shipping_title_container = container.find("li", {"class", "price-ship"})
    shipping_cost = shipping_title_container.text

    print('Product: ' + product_title)
    print('Brand: ' + brand_title)
    print('Shipping: ' + shipping_cost.strip())

    '''Simutaneously write the information extracted to the excel file'''
    f.write(brand_title + "," + product_title.replace(",", "|") + "," + shipping_cost.strip() + "\n")



'''Close the excel file so that it can be accessed'''
f.close()
