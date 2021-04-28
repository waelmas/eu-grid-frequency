#!/usr/bin/env python
# -*- coding: utf-8 -*-


# export PSQLPASSWORD="PASSWORD"


from selenium import webdriver
from datetime import datetime
# from google.cloud import storage

# we need to know where the chrome driver is on the machine (not like Firefox)
# /home/waela/Desktop/selenium/scraping/

import os
import time

import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# fix for MacOs security
# xattr -d com.apple.quarantine chromedriver


from collections import defaultdict

from selenium.common.exceptions import NoSuchElementException

# import beepy #to trigger alarms when scraper fails or crashes
import csv
import os.path



chrome_path = r"[FULL_PATH_TO_CHROMEDRIVER]"




chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("window-size=1024,768")
chrome_options.add_argument("--no-sandbox")

# driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
driver = webdriver.Chrome(chrome_path, options=chrome_options)

outfile = 'datanetz/data_.csv'
file_count = 0
file_check = True

#  Using this to create a new file if older versions exist and keep linking of sequence
while file_check:
    file_count += 1
    file_name = outfile.split("_")
    outfile = file_name[0] + "_" + str(file_count) + ".csv"
    file_check = os.path.isfile(outfile)


print("Writing to: {} \n".format(outfile))

csvfile = open(outfile, 'w')
writer = csv.writer(csvfile)
writer.writerow(["Timestamp", "Frequency"])
csvfile.close()





time.sleep(2)



url = "https://www.netzfrequenzmessung.de/index.htm"


driver.get(url)

time.sleep(3)

last_timestamp_val = " "


try:

    while(1):
        csvfile = open(outfile, 'a')
        writer = csv.writer(csvfile)
        freq_path = '/html/body/div[5]/div/table/tbody/tr/td/span[1]'


        freq_el = driver.find_element_by_xpath(freq_path)


        freq_text = freq_el.get_attribute('innerHTML')
        freq_val = float(freq_text.replace('<font style="vertical-align: inherit;">', '').replace('</font>', ''))

        timestamp_path = '/html/body/div[5]/div/table/tbody/tr/td/span[3]'

        timestamp_el = driver.find_element_by_xpath(timestamp_path)

        timestamp_val = timestamp_el.get_attribute('innerHTML')

        timestamp_val = timestamp_val.replace('<font style="vertical-align: inherit;">', '').replace('</font>', '')

        if timestamp_val == last_timestamp_val:
            continue
        else:
            last_timestamp_val = timestamp_val
        

        print("Time: {} Freq: {}\n".format(timestamp_val, freq_val))
        writer.writerow([timestamp_val, freq_val])

        csvfile.close()
        time.sleep(0.5)

except KeyboardInterrupt:
    driver.close()
    csvfile.close()
    print("\nClosing driver and csv\n")
    
finally:
    driver.close()
    csvfile.close()
    print("\nClosing driver and csv\n")


