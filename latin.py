from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tabulate import tabulate
import sys
import os

app = Flask(__name__)

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
        sentence = sentence + [[w] + [ pre.text.replace('.', '').replace("\n", "<br>") ]]

    styles = '<!DOCTYPE html><html><head><style>\
              #results {  font-family: Arial, Helvetica, sans-serif;  border-collapse: collapse;  width: 100%;}\
              #results td, #results th {  border: 1px solid #ddd;  padding: 8px; }\
              #results tr:nth-child(even){background-color: #f2f2f2;}\
              #results tr:hover {background-color: #ddd;}\
              #results th {  padding-top: 12px;  padding-bottom: 12px;  text-align: left;  background-color: #3366ff;  color: white;}\
              </style></head><body>'
    result = styles + '<table id="results"><tr><th>Word</th><th>Dictionary</th></tr>'
    for tr in sentence:
        result = result + "<tr>"
        for td in tr:
            result = result + "<td>" + td + "</td>"
        result = result + "</tr>"
    result = result + "</table>" + "</body></html>"
    return result

@app.route("/api/")
def api ():
    return analyze(request.args.get("words"))

@app.route("/")
def index ():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
