from flask import Flask,render_template,redirect,url_for
from flask import request
from datetime import timedelta
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.keys import Keys
import requests,os
#-----------------------以下為TechCrunch爬蟲-------------------------------------------------

def TCcrawler(search):
    url = "https://search.techcrunch.com/search;_ylc=X3IDMgRncHJpZANzQjRHM2ZJaVJ0Nktfa0U5WDJjYnhBBG5fc3VnZwMxMARwb3MDMARwcXN0cgMEcHFzdHJsAzAEcXN0cmwDMgRxdWVyeQNhaQR0X3N0bXADMTYyMjEzMTMwNQ--?p="+search+"&fr=techcrunch"
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(20)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    tag_div = soup.find_all("li",class_="ov-a mt-0 pt-26 pb-26 bt-dbdbdb")
    print("標題數:", len(tag_div))
    titles_list = []
    href_list=[]    
    for tag in tag_div:
        titles_reg = tag.find("h4", class_="pb-10").find("a").text.strip()
        href_reg=tag.find("a").get("href",None)
        titles_list.append(titles_reg)
        href_list.append(href_reg)
        #summary_reg = tag.find("p", class_="fz-14 lh-20 c-777").text.strip()

    images = soup.find_all("li",class_="ov-a mt-0 pt-26 pb-26 bt-dbdbdb")
    print("圖檔數:", len(images))
    img_list= []
    for img in images:
        imgUrl = img.find("img").get("src")
        img_list.append(imgUrl)
    class title_img():  
        def __init__(self,title,img,href):
            self.title=title
            self.img=img
            self.href=href
    TC_title_img_list=[]
    for i in range(len(titles_list)):
        TC_title_img_list.append(title_img(titles_list[i],img_list[i],href_list[i]))
    #print(titles_list)
    driver.quit()
    return TC_title_img_list
#-------------------------以下為TheVerge爬蟲---------------------------------------------
def TVcrawler(search):
    url = "https://www.theverge.com/search?q="+search
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(20)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")

    tag_div = soup.find_all("div", class_="c-compact-river__entry")
    print("標題數:", len(tag_div))
    titles_list = []
    href_list=[]    
    for tag in tag_div:
        titles_reg = tag.find("h2", class_="c-entry-box--compact__title").find("a").text.strip()
        href_reg=tag.find("a").get("href",None)
        titles_list.append(titles_reg)
        href_list.append(href_reg)
        #summary_reg = tag.find("p", class_="fz-14 lh-20 c-777").text.strip()

    images = soup.find_all("div",class_="c-entry-box--compact__image")
    print("圖檔數:", len(images))
    img_list= []
    for img in images:
        imgUrl = img.find("img").get("src")
        img_list.append(imgUrl)
    class title_img():  
        def __init__(self,title,img,href):
            self.title=title
            self.img=img
            self.href=href
    TV_title_img_list=[]
    for i in range(len(titles_list)):
        TV_title_img_list.append(title_img(titles_list[i],img_list[i],href_list[i]))
    #print(titles_list)
    driver.quit()
    return TV_title_img_list
#---------------------------------------------------------------------------------------
main_title='數位藝術專題研究_111032001'
app = Flask(__name__)
app.send_file_max_age_default = timedelta(seconds=1)

@app.route("/",methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if request.values['send']=='找新聞':
            TC_title_img_list=TCcrawler(request.values['user_search'])
            TV_title_img_list=TVcrawler(request.values['user_search'])
            return render_template('index.html', user_search=request.values['user_search'], main_title=main_title, TC_title_img_list=TC_title_img_list,  TV_title_img_list=TV_title_img_list)  
    title_img_list=TCcrawler("news")                 
    return render_template('home.html',main_title=main_title, title_img_list=title_img_list)  

@app.route('/home')
def index():
    return redirect('/')

@app.route('/refer')
def refer():
    return render_template('refer.html')

if __name__ == "__main__":
    app.run()


