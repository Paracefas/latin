from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate
import sys
import os

chrome_opt = Options()
chrome_opt.binary_location = g_chrome_bin = os.environ.get("GOOGLE_CHROME_BIN")
chrome_opt.add_argument('--headless')
chrome_opt.add_argument('--no-sandbox')
chrome_opt.add_argument('--disable-dev-sh--usage')

selenium_driver_path = os.environ.get("CHROMEDRIVER_PATH")
driver = webdriver.Chrome(executable_path= selenium_driver_path if selenium_driver_path else "./chromedriver", options=chrome_opt)

def analyze (words):
    ws = words.split()
    sentence = []
    for w in ws:
        driver.get('http://archives.nd.edu/cgi-bin/wordz.pl?keyword=' + w)
        pre = driver.find_element_by_xpath('//pre')
        sentence = sentence + [[w] + [ pre.text.replace('.', '') ]]
    print(tabulate(sentence, headers=["Word", "Dictionary"]))

analyze("pater noster qui est in celis")

driver.close()
