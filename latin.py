from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate
import sys

chrome_opt = Options()
chrome_opt.add_argument('--headless')
driver = webdriver.Chrome("./chromedriver", options=chrome_opt)

def analyze (words):
    ws = words.split()
    sentence = []
    for w in ws:
        driver.get('http://archives.nd.edu/cgi-bin/wordz.pl?keyword=' + w)
        pre = driver.find_element_by_xpath('//pre')
        sentence = sentence + [[w] + [ pre.text.replace('.', '') ]]
    print(tabulate(sentence, headers=["Word", "Dictionary"]))

analyze(sys.argv[1])

driver.close()
