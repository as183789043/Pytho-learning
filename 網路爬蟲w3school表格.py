import requests
import csv
from bs4 import BeautifulSoup

url='https://www.w3schools.com/html/html_media.asp'
csvfile='video_format.csv'
headers={
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}
r=requests.get(url,headers=headers)
r.encoding='utf8'
soup=BeautifulSoup(r.text,'lxml')
tag_table=soup.find(class_='ws-table-all')
rows=tag_table.findAll('tr')

with open(csvfile,'w+',newline='',encoding='utf-8') as fp:
    writer=csv.writer(fp)
    for row in rows:
        rowlist=[]
        for cell in row.findAll(['td','th']):
            rowlist.append(cell.get_text().replace('\n','').replace('\r',''))
        writer.writerow(rowlist)