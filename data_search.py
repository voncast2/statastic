import os
import requests
from bs4 import BeautifulSoup

num = 1


def text_processing(text):
    text = text.replace("\n",
                        "").replace("\r",
                                    "").replace("。”",
                                                "” ").replace("记者 ", "记者")
    punctuation_group = ["。", "？", "！"]
    for punctuation in punctuation_group:
        text = text.replace(punctuation, " ")
    text = text.split(" ")
    del text[-1]
    i = 0
    while i<len(text):
        if len(text[i])<10:
            del text[i]
        else:
            i+=1
    return text


def data_collection(url):
    global num
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }
    response = requests.get(url, headers)
    response.encoding = "utf-8"
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    li_list = soup.select("div.list.list_1.list_2 > ul.listTxt > li > h4")
    for li in li_list:
        title = str(li.a.text) + " " + str(li.span.text)
        print(title)
        new_url = str(li.a['href'])
        new_response = requests.get(new_url, headers)
        new_response.encoding = "utf-8"
        new_html = new_response.text
        new_soup = BeautifulSoup(new_html, 'lxml')
        try:
            content = new_soup.find('div', class_="pages_content").text
            content = text_processing(content)
            if (os.path.exists("textdata\\" + str(num) + ".txt")):
                num += 1
                print("Have Done")
            else:
                fp = open("textdata\\" + str(num) + ".txt",
                          "w",
                          encoding='utf-8')
                num += 1
                fp.write(title + "\n")
                for line in content:
                    fp.write(line + '。' + '\n')
        except Exception:
            print("pass it")


for i in range(15):
    url = "http://sousuo.gov.cn/column/31421/{}.htm".format(i)
    data_collection(url)