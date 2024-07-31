# encoding  = utf-8
import hashlib
import requests,re,os
from lxml import etree
from loguru import logger
import execjs
import csv


re_rule = {
    'arg1':re.compile("var arg1='(.*?)'"),

}


# 得到原始数据页面/参数
def get_url_list(acw_sc__v2):
    if acw_sc__v2:
        acw_sc__v2 = acw_sc__v2
    else:
        acw_sc__v2 = '66a397b7108082ff5035163964433c1adc21aaa1'


    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': 'acw_tc=2760829117219785666108715e9a238bceb7e341862dec4ec2a5b4aa4bea8b; GUID=a85aa86f-f0cd-4459-834f-f6be41ae0fbd;'
                  ' acw_sc__v2='+ acw_sc__v2 +'; Hm_lvt_9793f42b498361373512340937deb2a0=1721909460; HMACCOUNT=135DEA475AA0E00B; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22a85aa86f-f0cd-4459-834f-f6be41ae0fbd%22%2C%22%24device_id%22%3A%22190e9cd3e856cc-0b34c124bf48ac-26001f51-1327104-190e9cd3e866d%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; BAIDU_SSP_lcr=https://www.baidu.com/link?url=SR61ebxflDtyscD39MxEnKi1bziRMGSUpmpbofzi1Fm&wd=&eqid=e3ce37e100161ea10000000666a24192; Hm_lpvt_9793f42b498361373512340937deb2a0=1721909736; tfstk=fpNmcSftW-kbw18Om7cfCn0W6OWJhnG__ldtXfnNU0oWDndY7b-z00FxDrhq7l4sVVeA5tii7uzt0Chx6bzr50iwQsgOsPra4rFYDjzyU8rs6rIbDupgSkqiCZitbcqT7-QR96UblfGajMCd9YjdVZEDQVuV7YuIRVq5d34blfTSZQUJ6r9Gj5HcofrZaYusufR23lura0gs7nuwga4rVVlZ7Ao2zLunShJ2_b1f3mNaa7SD7eczV7vaNqDmjCnks7ND9AoUu0Aw_j3D1DzqqCRZctwD7z4AmBa-GWqnJoCyik4aRRkus3Snf74zgRzWmal3r8eKn8j2s0FxVvFqtF54rjmmLSZVsNqUrPyKE7QFOjcq0RhbWejYrSqYl7497LlmM8D3iX5B0ce8-50g1G1uxPzQQYVMmg-DUp5QiCgPW7J6CxuSrDss7mIuLxIOzabkLNMqPqidrav6CxuSrDQlrp5s34gjv; ssxmod_itna=Yqfxu7eDqCTqzxAxeukRKTit3=dr0eZD7qDtqFDl=rlDA5D8D6DQeGTNurI3Nq33A0eqadQ7gDoaIYPhpbamniip4LFzDB3DEx0=qEQZDiiyDCeDIDWeDiDG4Gml4GtDpxG=Djnz/1lXxGWDmbkDWPDYxDr61KDRxi7DDHQCx07DQHkmDeC3DDz3Yf4KjKO3WA+CgA1Fbvx3t2e6xG1740HeCL46ooUSfDs34LjqfRODlKRDCKz9cvHF4Gd0gHzq/uTqQ+NqQFaT70eIAremSmP=QtiRSqxhdSBxppNaADDi=h4aYLP4D===; ssxmod_itna2=Yqfxu7eDqCTqzxAxeukRKTit3=dr0eZD7qDtqD6pbitx0vdo03q33urqKI3XKuDfgcG8u7lk9mOqoeCIEmPvi3gRArW4cSF8Owt1krG7sFUYBOB+SpgLjLsgCob8AskjEFmQQK1/FZ1cdIAIkthue/iqta2Abd87OBGeC587aOxidyhYmBhqxGUcb8tYi2aWfb/4tIfeo/BSbPlRL2EofkhT+apLhY1dj6Rf0r2EhWOMbZUC2SfQRBfM2SKjpqEo=XzChBFYy94/GIFS1IFmIs6jLm6lIt1lepSUE0XaguAOhRH3VXLNPhNxfo=QiHO0wO0ZhXPbwwge6hX/00w6E/7rZO0j6=qz6D+LYIikP2oCU21RDzt3FAGPr8m=395HfNGAYk6Ejlrm1jn1UnaNG0TCfN18dh3ekxWl6Eu6EScWIfXuPrhm4DQIKA+AIyQYie0hxWiFIDxGhD=E43nD+Gx5GoB0dS88HkkhnDmkA+iFekstGqmMb/3sk01Vr++GxAaNWbKi++ab+Hl8i+DTCrYhFhb4QiGO4o0jIX0KRMvLksKixflbn0ofreenKD08DiQPYD==',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.17k.com/mianfei/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    response = requests.get('https://www.17k.com/top/refactor/top100/06_vipclick/06_click_freeBook_top_100_pc.html', headers=headers,timeout=4)
    my_html = etree.HTML(response.text)
    return my_html,response.text

# 数据提取 如果页面中无数据，则提取参数进行加密，得到加密参数后再进行请求＋数据提取
def get_book_list(arg1,my_html):
    global book_list
    if not arg1:
        trs = my_html.xpath('/html/body/div[4]/div[2]/div[3]/div[1]/table/tr')
        for tr in trs:
            hraf = ''.join(tr.xpath('./td[3]/a/@href'))
            if hraf != '':
                hraf = hraf.replace('book','list')
                book_list.append('https:'+hraf)

    else:
        with open('./get_acw_sc__v2.js','r') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        acw_sc__v2 = ctx.call('get_arg2',arg1[0])
        # logger.info(acw_sc__v2)
        my_html,res_text = get_url_list(acw_sc__v2)

        trs = my_html.xpath('/html/body/div[4]/div[2]/div[3]/div[1]/table/tr')
        for tr in trs:
            hraf = ''.join(tr.xpath('./td[3]/a/@href'))
            if hraf != '':
                hraf = hraf.replace('book', 'list')
                book_list.append('https:' + hraf)

    logger.info(book_list)
    # return book_list

# 检查 CSV 文件是否存在，如果不存在则创建，并写入表头
def setup_csv():
    global CSV_FILE
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['md5_value', 'url'])
            writer.writeheader()
        logger.info(f"Created new CSV file: {CSV_FILE}")

# 计算 URL 的 MD5 值
def calculate_md5(url):
    md5_hash = hashlib.md5(url.encode()).hexdigest()
    return md5_hash

# 检查给定的 MD5 值是否已经存在于 CSV 文件中
def is_md5_in_csv(md5_hash):
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['md5_value'] == md5_hash:
                logger.info('这本书的url已存在。')
                return True
    return False

# 将给定的 URL 添加到 CSV 文件中
def add_url_to_csv(md5_hash,url):
    # md5_hash = calculate_md5(url)
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([md5_hash, url])
    logger.info(f"Added URL to CSV: {url}")

if __name__ == '__main__':
    book_list = []
    my_html,res_text = get_url_list('')
    arg1 = re_rule['arg1'].findall(res_text)
    get_book_list(arg1,my_html)     # 得到小说的url


    exit()
    CSV_FILE = './book_url_list.csv'
    setup_csv()

    for url in book_list:
        md5_value = calculate_md5(url)
        if not is_md5_in_csv(md5_value):
            add_url_to_csv(md5_value,url)






