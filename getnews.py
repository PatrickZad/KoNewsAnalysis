import requests
from pyquery import PyQuery as pq
import os
urls=[]
newspath=r"./news/"
with open(r'./newsurl.txt','r',encoding='utf-8') as urlfile:
    url=urlfile.readline()
    while len(url) > 0:
        urls.append(url.strip())
        url=urlfile.readline()
count=0
for url in urls:
    try:
        page=requests.get(url)
        pqdoc=pq(page.text)
        headlineObj=pqdoc('.tit-article')
        #filePath=os.path.join(newspath,headlineObj.text()+'.txt')
        filePath=newspath+str(count)+".txt"
        contents=pqdoc('.article').children('p').items()
        with open(filePath,'w',encoding='utf-8') as newsFile:
            newsFile.write(headlineObj.text()+'\n')
            newsStrlist=[]
            for content in contents:
                newsStrlist.append(content.text())
            for paragraph in newsStrlist[:-2]:
                newsFile.write(paragraph+'\n')
        count+=1
        print(str(count)+' '+url+' done !')
    except BaseException as e:
        print('error:',e)
        print('failed:'+url)
    
