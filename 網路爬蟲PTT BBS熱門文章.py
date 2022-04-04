#實作案例 PTT BBS 熱門文章

import requests
import time
import json
from bs4 import BeautifulSoup


#步驟一 是別出目標的url網址
URL='https://www.ptt.cc'
MAX_PUSH=50
#Topic='Gossiping'
Topic='NBA'

url=URL+'/bbs/'+Topic+'index.html'

#步驟二 送出HTTP請求取得網路資源
def get_resource(url):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36 Edg/100.0.1185.29'
    }
    return requests.get(url,headers=headers,cookies={'over18':"1"})

#步驟三 分析HTML網頁找出爬蟲的目標標籤
#F12網頁結構

#步驟四 使用爬蟲剖析HTML網頁
def parse_html(r):
    if r.status_code==requests.codes.ok:
        r.encoding='utf-8'
        soup=BeautifulSoup(r.text,'lxml')
    else:
        print('連線失敗'+url)
        soup=None
    return soup
#步驟五 提取所需資料
#py 函數 web_scraping_bot()
def web_scraping_bot(url):
    articles=[]
    print('網路資料抓取中...')
    soup=parse_html(get_resource(url))
    if soup:
        #取得今天日期，去掉開頭"0"符合ptt日期形式
        today=time.strftime('%m/%d').lstrip('0')
        #取得目前頁面的今日文章清單
        current_articles,prev_url=get_articles(soup,today)
        while current_articles:
            articles+=current_articles
            print('等待2秒鐘....')
            time.sleep(2)
            #剖析上一頁繼續尋找是否有今日文章
            soup=parse_html(get_resource(URL+prev_url))
            current_articles,prev_url=get_articles(soup,today)
    return articles

#py函數 get_articles()
def get_articles(soup,date):
    articles=[]
    #取得上一頁連結
    paging_div=soup.find('div',class_='btn-group btn-group-paging')
    paging_a=paging_div.find_all('a',class_='btn')
    prev_url=paging_a[1]['href']
    tag_div=soup.find_all('div',class_='r-ent')
    #判斷文章日期
    for tag in tag_div:
        if tag.find('div',class_='date').text.strip()==date:
            push_count=0 #取得推文數
            push_str=tag.find('div',class_='nrec').text
            if push_str:
                try:
                    push_count=int(push_str) #轉換成數字
                except ValueError:#轉換失敗可能是爆或x1,x2
                    if push_str=="爆":
                        push_count=99
                    elif push_str.startswich('X'):
                        push_count=-10
                        #取得文字的超連結和標題文字
            if tag.find('a'):
                href=tag.find('a')['href']
                title=tag.find('a').text
                author=tag.find('div',class_='author').string
                articles.append({
                    'title':title,
                    'href':href,
                    'push_count':push_count,
                    'author':author
                })
    return articles,prev_url

#步驟六 儲存取出的資料
def save_to_json(articles,file):
    print('今天總共有:',str(len(articles))+'篇文章')
    threshold=MAX_PUSH
    print('熱門文章(> %d推):'%(threshold))
    for item in articles: #顯示熱門文章清單
        if int(item['push_count'])>threshold:
            print(item['title'],item['href'],item['author'])
    with open(file,'w+',encoding='utf8') as fp: #寫入json檔案
        json.dump(articles,fp,indent=2,sort_keys=True,ensure_ascii=False)

#步驟七 建立主程式執行網頁爬蟲
if __name__=='__main__':
    url=URL+'/bbs/'+Topic+'/index.html'
    print(url)
    articles=web_scraping_bot(url)
    for item in articles:
        print(item)
    save_to_json(articles,'article.json')










