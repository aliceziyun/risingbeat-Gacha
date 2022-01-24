from mimetypes import init
from os import name
from pickle import NONE
import requests
from bs4 import BeautifulSoup  # HTML/XML解析库
import urllib

count = 0

def download_img(imgurl,name,type):
    global count
    count = count + 1
    r = requests.get(imgurl)
    imgpath = type + 'img\\' + name + '.png'
    print('第' + str(count) + '张' + "下载成功")
    with open(imgpath, 'wb') as f:
        f.write(r.content)
        f.close()


def find_img(i, name):
    print(i)
    charapage = requests.get(i)
    charasoup = BeautifulSoup(charapage.content, "lxml")
    ssr = charasoup.find('div', id="content_3_7")
    pageheader = ssr.parent
    cardindex = pageheader.contents.index(ssr) + 3
    card = pageheader.contents[cardindex]
    tmp = card.contents[0].find('a').get('href')
    print(tmp)
    cardurl = "https://tennis-risingbeat.gamerch.com"+urllib.parse.quote(tmp)
    cardpage = requests.get(cardurl)
    cardsoup = BeautifulSoup(cardpage.content, 'lxml')
    img = cardsoup.find(
        'div', id="ui_wikidb_main_img_wrap").find('a').get('href')
    download_img(img,name,'SSR')


def get_SSR_SR_card():
    url = "https://tennis-risingbeat.gamerch.com/"
    homepage = requests.get(url)  # Get该网页从而获取该html内容
    soup = BeautifulSoup(homepage.content, "lxml")  # 用lxml解析器解析该网页的内容
    # print(homepage.content.decode())  #debug

    box = soup.find('div', id="js_oc_box_0")
    for table in box.find_all('tr'):
        for chara in table.find_all('a'):
            chara_ = chara.get('href')  # 这里的page可能是学校的也可能是人物的，需要区分一下
            tmppage = requests.get(chara_)
            tmpsoup = BeautifulSoup(tmppage.content, "lxml")

            # 判断部分：
            uac = tmpsoup.find('div', class_="ui_anchor_container")
            judge = uac.find('h2', class_="ui_h-large")

            if judge != None and judge.text == "所属キャラクター一覧":
                continue

            # 获得人物名字部分
            uheader = tmpsoup.find('div', class_="ui_contentsHead")
            charaname = uheader.find(
                'span', id="js_async_main_column_name").text.split()
            charaname = charaname[0]
            print(charaname)
            # namepath = 'img\\character.txt'
            # with open(namepath, 'a') as f:
            #     f.write("{}\n".format(charaname))
            #     f.close()

            if judge == None:
                find_img(chara_, charaname)
                continue
            else:
                find_img(chara_, charaname)
                continue


def get_R_card():
    url = "https://tennis-risingbeat.gamerch.com/%E3%82%AB%E3%83%BC%E3%83%89%E4%B8%80%E8%A6%A7%EF%BC%9AR"
    homepage = requests.get(url)
    soup = BeautifulSoup(homepage.content, "lxml")

    for each in soup.find_all('tr'):
        if len(each.contents) >= 5:
            Rcard = each.contents[1]
            if Rcard.text == "カード名":
                continue
            tmp = Rcard.find('a')
            if tmp == NONE:
                break
            cardurl = tmp.get('href')
            name  = Rcard.find('a').text
            print(name)
            cardpage = requests.get(cardurl)
            cardsoup = BeautifulSoup(cardpage.content, "lxml")
            cardcontainer = cardsoup.find('section', id="js_async_main_column_text")
            imgurl = cardcontainer.contents[3].find('a').get('href')
            download_img(imgurl,name,'R')
        else:
            continue

def main():
    while(True):
        type = input("想下载哪种卡面？SSR\SR\R?")
        if type == 'SSR' or type == 'SR':
            get_SSR_SR_card()
            break
        if type == 'R':
            get_R_card()
            break
        else:
            print("没有这种类型的卡")

if __name__ == "__main__":
    main()