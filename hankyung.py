import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os,sys
## pdf 파싱하기 
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open
from urllib.request import urlopen

## pdf 다운로드를 위한 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

## 데이터 저장 
import pandas as pd
import numpy as np

## 크롬 경로설정 

browser = webdriver.Chrome("C:/chromedriver_win32/chromedriver.exe") 
#browser.implicitly_wait(3) 
page_num = 1 
board_index = 1 
start_date = "2017-01-05" 
end_date = "2021-01-05" 
base_url = "http://consensus.hankyung.com" 
browser.get("http://consensus.hankyung.com/apps.analysis/analysis.list?sdate="+str(start_date)+"&edate="+str(end_date)+"&now_page="+str(page_num)+"&search_value=&report_type=&pagenum=80&search_text=&business_code=") 

##pdf 파일 파싱하기
def read_pdf_file(pdfFile):
    rsrcmgr = PDFResourceManager() 
    retstr = StringIO() 
    laparams = LAParams() 
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    PDFPageInterpreter.get_pages(rsrcmgr, device, pdfFile) 
    device.close()

    content = retstr.getvalue() 
    retstr.close() 
    return content

##web pdf타입 사이트 pdf 파일을 다운받기 
def download_pdf(lnk):
    download_dir = "/Users/mjc/Desktop/stockCrawling"
    # for linux/*nix, download_dir="/usr/Public" 
    options = webdriver.ChromeOptions()
    #options.add_experimental_option('excludeSwitches', ['enable-logging'])
    #driver = webdriver.Chrome(options=options, executable_path='C:/chromedriver_win32/chromedriver.exe')

    profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer 
    "download.default_directory": download_dir, 
    "download.prompt_for_download": False, #To auto download the file 
    "plugins.always_open_pdf_externally": True, 
    "download.extensions_to_open": "applications/pdf"} 
    options.add_experimental_option('prefs', profile)
    driver = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe', chrome_options=options) # Optional argument, if not specified will search path. 
    
    driver.get(lnk) 
    time.sleep(3) 
    driver.close()

    pdf_title = board_pdf_url.split('=')[1] 
    pdf_file = open(pdf_title+".pdf", "rb")
    pdf_content = read_pdf_file(pdf_file) 
    return pdf_content

##로컬 파일 불러오기 
#pdf_file_test = open("547325.pdf", "rb") 
#contents = read_pdf_file(pdf_file_test) 
##해당 pdf 파일 다운로드 
#download_pdf("http://consensus.hankyung.com/apps.analysis/analysis.downpdf?report_idx=547354")
 
board_category = "" 
board_title = "" 
board_reference = "" 
board_pdf_href = "" 
board_pdf_content = "" 
html = browser.page_source 
soup = BeautifulSoup(html, 'html.parser') 

while board_index < 80: 
    board_date = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child("+str(board_index)+") > td.first.txt_number")[0].get_text() 
    board_title = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child("+str(board_index)+") > td.text_l > a")[0].get_text() 
    board_category = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child("+str(board_index)+") > td:nth-child(2)")[0].get_text() 
    board_reference = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child("+str(board_index)+") > td:nth-child(5)")[0].get_text() 
    board_pdf_url = soup.select("#contents > div.table_style01 > table > tbody > tr:nth-child("+str(board_index)+") > td:nth-child(6) > div > a")[0]['href'] 
    board_pdf_content = download_pdf(base_url+"/"+board_pdf_url) 
    print(str(page_num)+"페이지의"+str(board_index)+"번째까지 게시글 확인 완료") 
    board_index += 1
board_index = 1

write_wb.save(filename = 'report_data.xlsx')
## 기본 정보 파싱 완료 
browser.close()

