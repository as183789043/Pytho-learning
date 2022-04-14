
import requests
import json
url='https://www.googleapis.com/books/v1/volumes?maxResults=20&q=Python&projection=lite'
jsonfile='book.json'
r=requests.get(url)
r.encoding='utf-8'
json_data=json.loads(r.text) #loads 將json字串轉換成字典
with open(jsonfile,'w+',encoding='utf8') as fp:
    json.dump(json_data,fp,ensure_ascii=False, indent=2)   #dump 將字典轉換成json字串,裝進指定檔案   #ensure_ascii 輸出中文字(預設為True)     #indent 分行
    
