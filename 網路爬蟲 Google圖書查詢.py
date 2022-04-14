
import requests
import json
url='https://www.googleapis.com/books/v1/volumes?maxResults=20&q=Python&projection=lite'
jsonfile='book.json'
r=requests.get(url)
r.encoding='utf-8'
json_data=json.loads(r.text)
with open(jsonfile,'w+',encoding='utf8') as fp:
    json.dump(json_data,fp,ensure_ascii=False, indent=2)