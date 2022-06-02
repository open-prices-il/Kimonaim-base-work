from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

path = r'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(path)

# Open shufersal db
driver.get('http://prices.shufersal.co.il/')

# Filter to full price list (not promos or partial lists)
select = Select(driver.find_element_by_css_selector('#ddlCategory'))
select.select_by_visible_text('PricesFull')
time.sleep(3)

# Now selenium will go through the first 4 pages and get all the links. 

css_selectorList = [
    '#gridContainer > table > tbody > tr:nth-child(1) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(2) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(3) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(4) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(5) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(6) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(7) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(8) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(9) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(10) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(11) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(12) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(13) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(14) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(15) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(16) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(17) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(18) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(19) > td:nth-child(1) > a',
    '#gridContainer > table > tbody > tr:nth-child(20) > td:nth-child(1) > a',
]
'#gridContainer > table > tfoot > tr > td > a:nth-child(1)'

links = []
for selector in css_selectorList:
    conn = driver.find_element_by_css_selector(selector)
    link = conn.get_attribute('href')
    links.append(link)

driver.find_element_by_css_selector('#gridContainer > table > tfoot > tr > td > a:nth-child(1)').click()
time.sleep(4)


for selector in css_selectorList:
    conn = driver.find_element_by_css_selector(selector)
    link = conn.get_attribute('href')
    links.append(link)

driver.find_element_by_css_selector('#gridContainer > table > tfoot > tr > td > a:nth-child(3)').click()
time.sleep(4)

for selector in css_selectorList:
    conn = driver.find_element_by_css_selector(selector)
    link = conn.get_attribute('href')
    links.append(link)

driver.find_element_by_css_selector('#gridContainer > table > tfoot > tr > td > a:nth-child(5)').click()
time.sleep(4)

for selector in css_selectorList:
    conn = driver.find_element_by_css_selector(selector)
    link = conn.get_attribute('href')
    links.append(link)

print(len(links))
for l in links:
    print(l)

import os, requests, pyperclip, shutil
from datetime import date

today = date.today()

path = os.path.join(r'C:\...\shufersal', str(today))
print(path)
print(os.getcwd())

## Now download all the files and put them in the shufersal list

for gz_link in links:
    pyperclip.copy(gz_link)
    fileName = pyperclip.paste()[56:98]
    try:
        r = requests.get(pyperclip.paste(), stream=True)
        with open(fileName, 'wb') as f:
            for chunk in r.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)
        shutil.move(str(fileName), path)
    except:
        print("File " +str(fileName) + " apparently exists.")


time.sleep(5)
driver.quit()
