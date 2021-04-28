#!/usr/bin/env python
# -*- coding: utf-8 -*-


from selenium import webdriver
from datetime import datetime


import os
import time

import psycopg2

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


from collections import defaultdict

from selenium.common.exceptions import NoSuchElementException


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



outfile = 'data/data_.csv'
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



url = "https://www.swissgrid.ch/en/home/operation/grid-data/current-data.html#frequency"


driver.get(url)

time.sleep(3)

try:

    while(1):
        csvfile = open(outfile, 'a')
        writer = csv.writer(csvfile)
        freq_path = '/html/body/div[2]/div[1]/div[3]/div[10]/div/swg-data-widget/div/div/div[2]/swg-data-widget-marker[9]'

        freq_el = driver.find_element_by_xpath(freq_path)

        in_freq_el = freq_el.find_element_by_class_name("swg-data-widget-marker__value-1")
        freq_text = in_freq_el.get_attribute('innerHTML')

        freq_vals = freq_text.split("<br>")

        freq_val = float(freq_vals[1].replace("&nbsp;Hz", ""))


        timestamp_path = '/html/body/div[2]/div[1]/div[3]/div[10]/div/swg-data-widget/div/table/tbody/tr[7]/td[2]'
        timestamp_el = driver.find_element_by_xpath(timestamp_path)
        timestamp_val = timestamp_el.text

        print("Time: {} Freq: {}\n".format(timestamp_val, freq_val))
        writer.writerow([timestamp_val, freq_val])

        csvfile.close()
        time.sleep(10)

except KeyboardInterrupt:
    driver.close()
    csvfile.close()
    print("\nClosing driver and csv\n")
    
finally:
    driver.close()
    csvfile.close()
    print("\nClosing driver and csv\n")



driver.close()







