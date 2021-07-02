
from unicodedata import category
from django.core import paginator
from django.core.paginator import Paginator
from django.db.models.expressions import OuterRef
from django.shortcuts import get_object_or_404, render
from .models import Company, Detaildaily
from .models import Daily
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


def company(request):
    comp = Company.objects.all()
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw','') # 검색어
    #조회
    company_list = comp.order_by('code')
    if kw:
        company_list = company_list.filter(
            Q(code__icontains=kw) |
            Q(company__icontains=kw)
        ).distinct()

    #페이징처리
    paginator = Paginator(company_list, 20)
    page_obj = paginator.get_page(page)
    context = {'comp':page_obj, 'page':page, 'kw' : kw}
    return render(request, 'stockInfoPage/company.html', context)



    


def daily_price(request):
    info = Daily.objects.all()
    page = request.GET.get('page', '1')  # 페이지
    kw2 = request.GET.get('kw2', '')  # 검색어
    #조회
    daily_price= info.order_by('code')
    if kw2:
        daily_price = daily_price.filter(
            Q(code__icontains=kw2) |  # 제목검색
            Q(company__icontains=kw2)    # 내용검색
        ).distinct()

    paginator = Paginator(daily_price, 20)
    page_obj = paginator.get_page(page)
    context = {'info':page_obj, 'page':page, 'kw2':kw2}
    return render(request, 'stockInfopage/daily_price.html',context)

def home(request):
    #네이버 경제 메인 페이지 크롤링
    url = f'https://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
    #네이버 글로벌 경제 페이지 크롤링
    finance_news_url = f'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=101&sid2=262'

    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    #네이버 글로벌 경제 금융
    res = requests.get(finance_news_url,headers=headers)
    soup2 = BeautifulSoup(res.text,'html.parser')

    #네이버 경제 메인
    my_news = soup.select('#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > a')
    #my_news_link = soup.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a')
    my_news_content = soup.select('#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_lede')
    my_news_writing = soup.select('#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_text > div.cluster_text_info > div')
    my_news_image = soup.select('#main_content > div > div._persist > div:nth-child(1) > div.cluster_group._cluster_content > div.cluster_body > ul > li:nth-child(1) > div.cluster_thumb > div.cluster_thumb_inner > a > img')
    
    newslist = list()
    nnews = list()
    # nlink = list()

    for news in my_news:
        nnews.append(news.text.strip())

    # for link in my_news_link:
    #     nlink.append(link.get('href'))
        
    for i in range(len(nnews)):
        #newslist.append([nnews[i],nlink[i]])
        title = my_news[i].text.strip()
        link = my_news[i].get('href')
        content = my_news_content[i].text.strip()
        writing = my_news_writing[i].text.strip()
        #image = my_news_image[i].get('src').replace('nf132_90','w647')
        try: #list index out of range 방지를 위한 예외처리
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

    # 네이버 뉴스 글로벌 경제_금융
    finance_news = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2)')
    finance_link = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt:nth-child(2) > a')
    finance_content = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.lede')
    finance_writing = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dd > span.writing')
    finance_image = soup2.select('#main_content > div.list_body.newsflash_body > ul.type06_headline > li > dl > dt.photo > a > img')
    
    financenewslist = list()
    financennews = list()
    # nlink = list()

    for fnews in finance_news:
        financennews.append(fnews.text.strip())

    # for link in my_news_link:
    #     nlink.append(link.get('href'))
        
    for n in range(len(financennews)):
        #newslist.append([nnews[i],nlink[i]])
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
    # 네이버 경제 금융 마지막.

    ####top종목
    urls = 'https://finance.naver.com/'
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    res = requests.get(urls,headers=headers)
    #res = req.urlopen(urls).read().decode('cp949')
    #soups = BeautifulSoup(res,'html.parser')
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
    ####
    
    # 윤재락 만드는중 - home > 상한가 테스트
    url = "http://finance.naver.com/sise/"          #네이버 금융 url 주소
    res = req.urlopen(url).read().decode('cp949')   #utf-8 : 한글 깨짐, unicode_escape : 한글 깨짐, cp949로 변환해야한다.
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
    url = 'https://finance.naver.com/sise/sise_deal_rank.nhn'         #네이버 금융 url 주소
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')

    organ_name = soup.find_all('a', class_ = 'company')
    organ_price = soup.find_all('td',class_ = 'number')

    organ1 = list()
    total_organ = list()

    for o in organ_name:
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


def dashboard(request):
    comp_list = Daily.objects.all()
    page = request.GET.get('page', '1')
    kw3 = request.GET.get('kw3','')
    #조회
    comp_list2=comp_list.order_by('code')
    if kw3:
        comp_list2 = comp_list2.filter(
            Q(code__icontains=kw3) |  # 제목검색
            Q(company__icontains=kw3)    # 내용검색
        ).distinct()
    
    paginator = Paginator(comp_list2, 20)
    page_obj = paginator.get_page(page)
    context = {'comp_list':page_obj,'page':page, 'kw3':kw3}
    return render(request, 'stockInfopage/dashboard.html',context)

    

#네이버 뉴스 검색
def search(request):
    if request.method == 'GET':
        
        config_secret_debug = json.loads(open(settings.SECRET_DEBUG_FILE).read())
        client_id = config_secret_debug['NAVER']['CLIENT_ID']
        client_secret = config_secret_debug['NAVER']['CLIENT_SECRET']

        q = request.GET.get('q')
        encText = urllib.parse.quote("주가".format(q))
        url = "https://openapi.naver.com/v1/search/news?query=" + encText  # json 결과
        news_api_request = urllib.request.Request(url)
        news_api_request.add_header("X-Naver-Client-Id",client_id)
        news_api_request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(news_api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')

            context = {
                'items': items
            }
            return render(request, 'stockInfopage/search.html', context=context)

# 페이징, 클릭시 이동 url 테스트
# edit. daily_price 카피
# def lists(request):
#     info = Daily.objects.all()
#     page = request.GET.get('page', '1')  # 페이지
#     kw2 = request.GET.get('kw2', '')  # 검색어
#     #조회
#     daily_price= info.order_by('code')
#     if kw2:
#         daily_price = daily_price.filter(
#             Q(code__icontains=kw2) |  # 제목검색
#             Q(company__icontains=kw2)    # 내용검색
#         ).distinct()

#     paginator = Paginator(daily_price, 20)
#     page_obj = paginator.get_page(page)
#     context = {'lists':page_obj, 'page':page, 'kw2':kw2}
#     return render(request, 'stockInfopage/lists.html',context)

#edit. dashboard 카피. 티커명 클릭 시 세부 페이지로 넘어가도록하는 코드
def detail(request,code):
    comp_lists = Company.objects.get(code=code)
    
    comp_list = Daily.objects.all()

    # comp_list3 = Detaildaily.objects.get(date= datetime.now(),code=code)
    #datenow = datetime.now()
    #datemonth1 = datenow - relativedelta(month=1) //실시간 실행시 주석 제거
    # date=datetime.now()
    datenow1 = datetime.datetime.today() -datetime.timedelta(days=2)
    datenow2 = datetime.datetime.today() -datetime.timedelta(days=9)
    datenow3 = datetime.datetime.today() -datetime.timedelta(days=16)
    datenow4 = datetime.datetime.today() -datetime.timedelta(days=23)
   # datenow5 = datetime.datetime.today() -datetime.timedelta(days=19)
    #datenow6 = datetime.datetime.today() -datetime.timedelta(days=20)
    #datenow7 = datetime.datetime.today() -datetime.timedelta(days=21)
    #datenow8 = datetime.datetime.today() -datetime.timedelta(days=24)
    #datenow9 = datetime.datetime.today() -datetime.timedelta(days=24)

    
    
    # comp_list3 = Daily.objects.get(date= datenow ,code=code)
    comp_list4 = Daily.objects.get(date= datenow1,code=code)
    comp_list5 = Daily.objects.get(date= datenow2,code=code)
    comp_list6 = Daily.objects.get(date= datenow3,code=code)
    comp_list7 = Daily.objects.get(date= datenow4,code=code)
   # comp_list8 = Daily.objects.get(date= datenow5,code=code)
    #comp_list9 = Daily.objects.get(date= datenow6,code=code)
    #comp_list10 = Daily.objects.get(date= datenow7,code=code)
    #comp_list11 = Daily.objects.get(date= datenow8,code=code)
    #comp_list12 = Daily.objects.get(date= datenow9,code=code)


    
    page = request.GET.get('page', '1')
    kw3 = request.GET.get('kw3','')
    #조회
    comp_list2=comp_list.order_by('code')
    if kw3:
        comp_list2 = comp_list2.filter(
            Q(code__icontains=kw3) |  # 제목검색
            Q(company__icontains=kw3)    # 내용검색
        ).distinct()
    
    paginator = Paginator(comp_list2, 20)
    page_obj = paginator.get_page(page)

    context = {'comp_list':page_obj,'page':page, 'kw3':kw3,'comp_lists':comp_lists,'comp_list4':comp_list4,'comp_list5':comp_list5,'comp_list6':comp_list6,'comp_list7':comp_list7}
    return render(request, 'stockInfopage/detail.html', context)#다른곳 이동