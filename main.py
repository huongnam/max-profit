import os
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta
import time


def compute_max_profit(lst):
    return max(lst)[1]


def parse_text(url, file):
    with open(file, 'w') as f:
        f.write('date,rate\n')
    driver = webdriver.Chrome(
        r'D:\courses\ds101\ds101ex02template\chromedriver_win32\chromedriver.exe')
    driver.get(url)
    start_date = date(2020, 6, 1)
    end_date = date(2020, 7, 31)
    delta = timedelta(days=1)
    while start_date <= end_date:
        date_string = start_date.strftime("%d/%m/%Y")
        textbox = driver.find_element_by_id('txttungay')
        textbox.clear()
        textbox.send_keys(date_string)
        textbox.send_keys(Keys.TAB)
        time.sleep(1)
        table = driver.find_element_by_id('ctl00_Content_ExrateView')
        list_rows = table.find_elements_by_tag_name('tr')
        for row in list_rows:
            list_tds = row.find_elements_by_tag_name('td')
            if len(list_tds) >= 5:
                if list_tds[1].text.strip() == 'AUD':
                    rate = list_tds[4].text.replace(',', '')
                    with open('data/exchange_rate.aud.06_2020.07_2020.csv', 'a') as f:
                        f.write(",". join((date_string, str(rate)+"\n")))
        start_date += delta


if __name__ == "__main__":

    parse_text('https://portal.vietcombank.com.vn/Personal/TG/Pages/ty-gia.aspx',
               'data/exchange_rate.aud.06_2020.07_2020.csv')
    # load your data frame from data/exchange_rate.aud.06_2020.07_2020.csv
    df = pd.read_csv('data/exchange_rate.aud.06_2020.07_2020.csv')

    # convert to list
    list_exchange_rates = df.values.tolist()

    # compute max profit we can achieve
    max_profit = compute_max_profit(list_exchange_rates)

    print('After many complicate calculations ...')
    print('Max profit we can get is', max_profit)
