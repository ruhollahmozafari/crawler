import urllib
import requests
from urllib.request import Request,urlopen# to send request and get html
import csv # to save the resutl into a csv file
import scrapy  
from bs4 import BeautifulSoup 
import re # to find a specific substring
import pandas as pd # to insert the data to csv file 


def requester(url):# gets a URL and send request and returnt the html as string
    resp=urlopen(url)
    print(resp.code)# check if the request has gone fine (200 is ok code)
    html= resp.read().decode("UTF-8")#from now on the html type is a string
    with open('requester result.txt','w',encoding='utf-8') as file:
        file.write(html)
    return html


def keyword_finder(html,substring):
    lent=len(substring)
    lst=[]
    for counter in range(0, len(html)):
        if html[counter:counter+lent] == substring:
            lst.append(counter)
    df = pd.DataFrame(lst, columns=["indexs"])  # saving data into csv file using pandas 
    df.to_csv('keyword result.csv', index=False)
    return lst



def link_finder(url):# find all the link from given URL
    req = Request(url)
    html= urlopen(req)
    soup = BeautifulSoup(html, "lxml")#converting the data into a BeautifulSoup to parse
    links = []
    for link in soup.findAll('a'):# finding all the links 
        links.append(link.get('href'))  
    df = pd.DataFrame(links, columns=["colummn"])  # saving data into csv file using pandas 
    df.to_csv('links result.csv', index=False)
    return links


def tag_finder(html): # using the html(which is a string in fact) to extract all the tags
    result_tags={}
    tagger = 1 # to search for all the tags
    Atag=True
    while Atag : 
        Atag=f'<h{tagger}'
        Btag=f'/h{tagger}>'
        startp=html.index(Atag)
        stopp=html.index(Btag)+4
        temp= html[startp:stopp]
        result_tags.update({Atag:temp})
        tagger+=1
        Atag=f'<h{tagger}'
        Btag=f'/h{tagger}>'
        if html.find(Atag)!= -1:
            pass
        else:                              
            Atag = False 
    with open('result tags.csv', 'w',) as file : # saving all the data into csv 
        
        csv_writer=csv.DictWriter(file,result_tags.keys(),delimiter='\n')
        csv_writer.writeheader()
        csv_writer.writerow(result_tags)
    return result_tags 

def image_saver(url):
    response=requests.get(url)
    soup=BeautifulSoup(response.content,"html.parser")
    images= soup.find_all("img",attrs={"alt":"Post image"})
    number = 0 
    for image in images:
        image_src=image["src"]
        print(image_src)
        urllib.request.urlretrieve(image_src, str(number))
        number+=1
        return image_src


karademy=requester('https://karademy.ir/')
# word_finder=keyword_finder(karademy,'python')
test_keyword_finder=keyword_finder(karademy,'python')
print(test_keyword_finder)
# f=tag_finder(karademy)
# lnks=link_finder("https://douryaad.ir/")
# pic= image_saver(url="https://www.reddit.com/r/cats")
# print(pic)
