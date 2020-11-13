""" Program to Scrape Mobiles Details from FlipKart.com and Saves in Local """

# pylint: disable = C0301, W0702, R0914
# C0301: Line too long (108/100) (line-too-long)
# W0702: No exception type(s) specified (bare-except)
# R0914: Too many local variables (25/15) (too-many-locals)

import re
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from progressbar import ProgressBar, Bar, Percentage

def scrape_from_flipkart(low, high):
    """ Scrapes the Mobile Phone Details from FlipKart.com """
    session_object = requests.Session()
    page_url = f"https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.price_range.from%3D{low}&sort=price_asc&p%5B%5D=facets.price_range.to%3D{high}"
    no_of_pages = int(BeautifulSoup(session_object.get(page_url).content, "html.parser").find("div", {"class": "_2zg3yZ"}).find("span").text.rsplit(" ", 1)[-1])

    ram_pattern = re.compile(r"[0-9]+ [A-Za-z]{2} RAM")
    rom_pattern = re.compile(r"[0-9]+ [A-Za-z]{2} ROM")
    battery_pattern = re.compile(r"[0-9]+ mAh [-A-Za-z ]*Battery")
    camera_pattern = re.compile(r"[.0-9]+MP[ A-Za-z]*(Camera)*")

    progress_bar = ProgressBar(maxval=no_of_pages + 1, widgets=[Bar('=', '[', ']'), ' ', Percentage()])
    progress_bar.start()

    collection = [['Model Name', 'Price', 'RAM', 'ROM', 'Battery Capacity', 'Camera', 'URL', 'Features']]

    flag = True
    for i in range(1, no_of_pages+1):
        progress_bar.update(i)
        if flag:
            page = requests.get(page_url + f"&page={i}").content
            parsed = BeautifulSoup(page, "html.parser")
            containers = parsed.findAll('div', {'class': '_1UoZlX'})
            if len(containers) == 0:
                flag = False
            for con in containers:
                ram, rom, battery, camera = 'NaN', 'NaN', 'NaN', 'NaN'

                model_name = con.find('div', {'class': '_3wU53n'}).text.replace(',', ' ')
                price = int(con.find('div', {'class': '_1vC4OE _2rQ-NK'}).text[1:].replace(',', ''))
                url = "https://www.flipkart.com" + con.find('a', {'class': '_31qSD5'}).get("href")

                ul_tag = con.find('ul', {'class': 'vFw0gD'})
                features = '\n'.join([li_tag.text.replace(',', ' ') for li_tag in ul_tag.findAll('li', {'class': 'tVe95H'})])

                try:
                    ram = ram_pattern.search(features).group()
                except:
                    pass

                try:
                    rom = rom_pattern.search(features).group()
                except:
                    pass

                try:
                    battery = battery_pattern.search(features).group()
                except:
                    pass

                try:
                    iters = list(camera_pattern.finditer(features))
                    camera = '; '.join([item.group(0).strip() for item in iters])
                except:
                    pass

                collection.append([model_name, price, ram, rom, battery, camera, url, features])

    progress_bar.finish()

    return collection

def write_csv(filename, data):
    """ Writes 2D array to CSV file """
    with open(filename, 'w') as file:
        for index, row in enumerate(data):
            if not index:
                index = "Sno."
            line = ",".join([str(cell).replace(',', ';').replace('\n', ' ') for cell in [index]+row]) + '\n'
            file.write(line)

if __name__ == "__main__":
    minimum, maximum = "Min", "Max"
    if len(sys.argv) > 2:
        minimum = sys.argv[1]
        maximum = sys.argv[2]
    elif len(sys.argv) == 2:
        minimum = sys.argv[1]

    mobile_details = scrape_from_flipkart(low=minimum, high=maximum)

    name = ("Mobiles-List-of-Price-" + minimum  + "-to-" + maximum + " "
            + datetime.now().strftime("%d-%b-%Y %H%M hrs") + ".csv")

    write_csv(name, mobile_details)
