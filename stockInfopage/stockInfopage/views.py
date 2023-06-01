from unicodedata import category
from django.core import paginator
from django.core.paginator import Paginator
from django.db.models.expressions import OuterRef
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

#crawling
from urllib.request import urlopen
from urllib.parse import quote_plus
import urllib.request
from bs4 import BeautifulSoup
import requests
import json
from django.conf import settings
import urllib.request as req
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import datetime
from dateutil.relativedelta import relativedelta
from django.utils.dateformat import DateFormat



def home(request):
    # 네이버 경제 메인 페이지 크롤링
    url = f'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
    # 네이버 글로벌 경제 페이지 크롤링
    finance_news_url = f'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=262'

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # 네이버 경제 메인
    my_news = soup.select('#main_content > div > div._persist > div.section_headline > ul > li > div.sh_text > a')
    my_news_link = soup.select('#main_content > div > div._persist > div.section_headline > ul > li > div.sh_text > a')
    my_news_content = soup.select('#main_content > div > div._persist > div.section_headline > ul > li > div.sh_text > div.sh_text_lede')
    my_news_writing = soup.select('#main_content > div > div._persist > div.section_headline > ul > li > div.sh_text > div.sh_text_info > div')
    my_news_image = soup.select('#main_content > div > div._persist > div.section_headline > ul > li > div.sh_thumb > div > a > img')


    newslist = list()
    nnews = list()
    nlink = list()

    for news in my_news:
        nnews.append(news.text.strip())

    for link in my_news_link:
        nlink.append(link.get('href'))
        
    for i in range(len(nnews)):
        newslist.append([nnews[i],nlink[i]])
        title = my_news[i].text.strip()
        link = my_news[i].get('href')
        content = my_news_content[i].text.strip()
        writing = my_news_writing[i].text.strip()

        try: #이거 빠지면 오류남
            image_s = my_news_image[i].get('src')
            image = my_news_image[i].get('src').replace('nf132_90','w647')
        except:
            image_s="NO IMAGE"
            image = "NO IMAGE"

        item_obj = {
            'title': title,
            'link': link,
            'content': content,
            'writing': writing,
            'image': image,
            'image_s': image_s,
        }

        newslist.append(item_obj)
   
    data = newslist




    # 글로벌 뉴스
    res = requests.get(finance_news_url, headers=headers)
    soup2 = BeautifulSoup(res.text, 'html.parser')

    finance_news = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2)')
    finance_link = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a')
    finance_content = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.lede')
    finance_writing = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.writing')
    finance_image = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt.photo > a > img')

    financenewslist = []

        
    for n in range(len(finance_news)):
   
        fnews_title = finance_news[n].text.strip()
        fnews_link = finance_link[n].get('href')
        fnews_content = finance_content[n].text.strip()
        fnews_writing = finance_writing[n].text.strip()
        fnews_image = finance_image[n].get('src').replace('type=nf106_72','type=w647')

        item_obj = {
            'ftitle': fnews_title,
            'flink': fnews_link,
            'fcontent': fnews_content,
            'fwriting': fnews_writing,
            'fimage': fnews_image,
        }

        financenewslist.append(item_obj)
    
    fnews_data = financenewslist





    #top종목
    urls = 'https://finance.naver.com/'
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    res = requests.get(urls,headers=headers)
    soups = BeautifulSoup(res.text,'html.parser')

    top = soups.select("#container > div.aside > div.group_aside > div.aside_area.aside_popular > table > tbody > tr > th")

    toplist = list()
    top2 = list()

    for tops in top:
        toplist.append(tops.text.strip())

    for i in range(len(toplist)):
        comp = top[i].text.strip()

        item_objs={
            'comp':comp,
        }
        top2.append(item_objs)
    comps = top2
    


    
    #상한가 테스트
    url = "http://finance.naver.com/sise/"         
    res = req.urlopen(url).read().decode('cp949')   
    soup = BeautifulSoup(res, "html.parser")
 
    top101 = soup.select("#popularItemList > li > a")
    top102 = soup.select("#popularItemList > li")
    
    top10list1 = list()
    top10list2 = list()

    top101list = list()
    top102list = list()
    
    for top11 in top101:
        top10list1.append(top11.text.strip())

    for top22 in top102:
        top10list2.append(top22.text.strip())

    for i in range(len(top10list1)):
        toptext1 = top101[i].text.strip()

        item_objs={
            'toptext1':toptext1,
        }
        top101list.append(item_objs)
    data1 = top101list

    for i in range(len(top10list2)):
        toptext2 = top102[i].text.strip()

        item_objs={
            'toptext2':toptext2,
        }
        top102list.append(item_objs)
    data2 = top102list
    
    # 거래량 상위 업종 top3
    urls = 'https://finance.naver.com/main/main.nhn'
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    res = requests.get(urls,headers=headers)
    soup = BeautifulSoup(res.text,'html.parser')

    sise1 = list()
    sise2 = list()

    sise_title = soup.select('#content > div.article > div.section2 > div.section_top.section_top_first > ul > li > p.item > a > strong')
    sise_diff = soup.select('#content > div.article > div.section2 > div.section_top.section_top_first > ul > li > p.item > em')

    for s1 in sise_title:
        sise1.append(s1.text.strip())
    
    for i in range(len(sise1)):
        title = sise_title[i].text.strip()
        diff = sise_diff[i].text.strip()
        
        sise_obj={
            'title':title,
            'diff': diff,
        }
        sise2.append(sise_obj)
    sise_data = sise2

    #기관 순매수
    url = 'https://finance.naver.com/sise/sise_deal_rank.nhn'       
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')

    organ_name = soup.find_all('a', class_ = 'company')
    organ_price = soup.find_all('td',class_ = 'number')

    organ1 = list()
    total_organ = list()

    for o in organ_name[0:7]:
        organ1.append(o.text.strip())

    for o2 in range(len(organ1)):
        title = organ_name[o2].text.strip()
        price = organ_price[o2].text.strip()

        organ_obj={
            'title': title,
            'price': price,
        }
        total_organ.append(organ_obj)
    organ_data=total_organ

    context = {'data':data,'comps':comps,'data1':data1,'data2':data2,'fnews_data': fnews_data, 'sise_data':sise_data,'organ_data':organ_data,}
    return render(request, 'stockInfopage/home.html',context)



#날짜 관련
def detail(request,code):
    comp_lists = Company.objects.get(code=code)
    
    comp_list = Daily.objects.all()

    comp_list3 = Detaildaily.objects.get(date= datetime.now(),code=code)
    datenow = datetime.now()
    datemonth1 = datenow - relativedelta(month=1)
    date=datetime.now()
    datenow1 = datetime.datetime.today() -datetime.timedelta(days=1)
    datenow2 = datetime.datetime.today() -datetime.timedelta(days=2)
    datenow3 = datetime.datetime.today() -datetime.timedelta(days=3)
    datenow4 = datetime.datetime.today() -datetime.timedelta(days=4)
    
    
    comp_list3 = Daily.objects.get(date= datenow ,code=code)
    comp_list4 = Daily.objects.get(date= datenow1,code=code)
    comp_list5 = Daily.objects.get(date= datenow2,code=code)
    comp_list6 = Daily.objects.get(date= datenow3,code=code)
    comp_list7 = Daily.objects.get(date= datenow4,code=code)

