#實作案例:majortests.com的單字清單
import time
import csv
import requests
from pyparsing import Word
from bs4 import BeautifulSoup

#步驟一 識別目標的url網址1500單字 共九頁
url='http://www.majortests.com/word-lists/word-list-0{0}.html'
def generate_urls(url,start_page,end_page):
    urls=[]
    for page in range(start_page,end_page):
        urls.append(url.format(page))
    return urls
#步驟二 送出http請求取得網路資源
def get_resource(url):
    headers={
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
}
    return requests.get(url,headers=headers)
#步驟三 分析html網頁找出爬蟲的目的標籤
#F12

#步驟四 使用爬蟲工具剖析html網頁
def parse_html(html_str):
    return BeautifulSoup(html_str,'lxml')

#步驟五 取出所需資料
#py函數 web_scraping_bot
def web_scraping_bot(urls):
    eng_words=[]

    for url in urls:
        file=url.split('/')[-1]
        print('抓取:'+file+'網路資料中...')
        r=get_resource(url)
        if r.status_code==requests.codes.ok:
            soup=parse_html(r.text)
            words=get_words(soup,file)
            eng_words=eng_words+words
            print('等待三秒鐘')
            time.sleep(3)
        else:
            print('http請求錯誤'+url)
    return eng_words
#py函數:get_words()

def get_words(soup,file):
    words=[]
    count=0
    for wordlist_table in soup.find_all(class_='wordlist'):
        count+=1
        for word_entry in wordlist_table.find_all('tr'):
            new_word=[]
            new_word.append(file)
            new_word.append(str(count))
            new_word.append(word_entry.th.text)
            new_word.append(word_entry.td.text)
            words.append(new_word)
    return words
#步驟六 儲存取出的資料
def save_to_csv(words,file):
    with open(file,'w+',newline='',encoding='utf-8') as fp:
        writer=csv.writer(fp)
        for word in words:
            writer.writerow(word)
#步驟七 建立主程式執行網頁爬蟲
if __name__=='__main__':
    urls=generate_urls(url,1,9)
    #print(urls)
    eng_words=web_scraping_bot(urls)
    for item in eng_words:
        print(item)
    save_to_csv(eng_words,"word.csv")

