# encoding  = utf-8
import requests
from lxml import etree
import os
from concurrent.futures import ThreadPoolExecutor

#所爬取的图片共92个图集，分为4个页面

def get_org_url(URL):
    urls = []  # 存储四个子页面的url
    for i in range(1, 5):
        url = URL + str(i)
        resp = requests.get(url, headers=headers)
        resp.encoding = 'utf-8'
        # xpath解析
        html = etree.HTML(resp.text)
        href = html.xpath("/html/body/div[4]/div/div[2]/div/a/@href")
        urls.append(href)
    return urls    #urls中储存92个url，对应92个图集

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径

#从92个url中得到图片的下载地址
def get_son_url(urls):
    for i in urls:
        for j in i:
            resp = requests.get(j, headers=headers)
            resp.encoding = 'utf-8'
            html = etree.HTML(resp.text)
            pics = html.xpath("/html/body/div[5]/div[3]/div[1]/div[4]/a/@href")
            max = str(pics[-2]).split("_")[-1].split(".html")[0]  # 获得该图集的最大页数
            ori_pic = str(pics[0]).split(".html")[0]
            img_max.append(max)
            img_ori_pic.append(ori_pic)

            for n in range(int(max)):
                n = n + 1
                href = ori_pic + "_" + str(n) + ".html"
                img_urls.append(href)

#下载图片
def get_img(i):
    count = 0
    for n in range(int(img_max[i])):
        n = n + 1
        href = "".join(img_ori_pic[i]) + "_" + str(n) + ".html"
        name = str(count)
        resp = requests.get(href, headers=headers)
        resp.encoding = 'utf-8'
        html = etree.HTML(resp.text)
        src = html.xpath("/html/body/div[5]/div[3]/div[1]/div[1]/a/img/@src")
        src = "".join(src)  # 将list转为str,src为图片下载地址
        img_name = html.xpath("/html/body/div[5]/div[3]/div[1]/div[1]/a/img/@alt")
        img_name = "".join(img_name)  # list->str，img_name为图片名称
        resp_src = requests.get(src, headers=headers)

        # 判断是否存在文件夹如果不存在则创建为文件夹
        file = "D://img/img"
        with open(file + "/" + img_name + name + '.jpg', mode="wb") as f:
            f.write(resp_src.content)
        #  time.sleep(0.1)

        count = count + 1  # 命名排序
        print(file + "/" + img_name + name + '.jpg')




if __name__ == '__main__':
    global headers,img_urls,img_max,img_ori_pic
    img_max = []
    img_ori_pic = []
    img_urls = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    URL = 'https://www.yeitu.com/tag/nuomeiziMini/?&page='
    urls = get_org_url(URL)
    get_son_url(urls)

    file = "D://img/img"
    mkdir(file)

    #i为下载的图集个数，用50个线程下载92个图集
    with ThreadPoolExecutor(50) as tp:
        for i in range(92):
            tp.submit(get_img,i = i)

    print("over")

