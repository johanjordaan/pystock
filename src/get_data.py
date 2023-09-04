import os.path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import config as cfg
from datetime import datetime, timedelta

file_template = '%Y%m%d'
query_template = '%d%m%Y'

def login():
    login_url = 'https://www2.commsec.com.au/secure/login'
    data_url = 'https://www2.commsec.com.au/Private/Charts/EndOfDayPrices.aspx'

    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory":cfg.destination}
    options.add_experimental_option("prefs", prefs)

    browser = webdriver.Chrome(options=options)
    browser.get(login_url)
    username_input = browser.find_element(By.ID, "username")
    username_input.send_keys(cfg.username)
    password_input = browser.find_element(By.ID, "password")
    password_input.send_keys(cfg.password)

    login_btn = browser.find_element(By.ID, "login")
    login_btn.click()
    time.sleep(3)

    browser.get(data_url)
    time.sleep(3)
    return browser

def download(browser, date):
    type_select = Select(browser.find_element(By.ID, "ctl00_BodyPlaceHolder_EndOfDayPricesView1_ddlAllSecurityType_field"))
    type_select.select_by_visible_text("ASX Equities")
    format_select = Select(browser.find_element(By.ID, "ctl00_BodyPlaceHolder_EndOfDayPricesView1_ddlAllFormat_field"))
    format_select.select_by_visible_text("Stock Easy")
    date_input = browser.find_element(By.ID, "ctl00_BodyPlaceHolder_EndOfDayPricesView1_txtAllDate_field")
    date_input.clear()
    date_input.send_keys(date.strftime(query_template))
    download_btn = browser.find_element(By.ID, "ctl00_BodyPlaceHolder_EndOfDayPricesView1_btnAllDownload_implementation_field")
    download_btn.click()
    time.sleep(.5)


def make_file_name(path, date):
    return f"{path}\\ASXEQUITIESStockEasy-{date.strftime(file_template)}.txt"


def file_exists(path, date):
    #print(make_file_name(path, date))
    return os.path.exists(make_file_name(path, date))

browser = login()
current_date = datetime.now()
end_date = datetime.fromisoformat('2022-06-03')

finished = False
while not finished:
    if current_date <= end_date:
        finished = True
    else:
        #print(current_date,current_date.strftime(file_template))
        if not file_exists(cfg.destination, current_date):
            if current_date.weekday() < 5:
                print(f"Downloading - {current_date.strftime(file_template)}")
                download(browser, current_date)
            else:
                pass
                #print("Skipped Weekend")
        else:
            pass
            #print("Skipped Already Exists")
        current_date = current_date - timedelta(days=1)

#
#download('error')
#download('02022023')
#download('05022023')
#download('03022023')


browser.quit()

