# encoding  = utf-8
import hashlib
from MyMongoDB import MyMongoDB
from lxml import etree
from loguru import logger
import aiohttp
import asyncio
import re, requests, csv

import execjs

# 测试参数是否需要更新
def test_req(acw_sc__v2):
    if acw_sc__v2:
        acw_sc__v2 = acw_sc__v2
    else:
        acw_sc__v2 = '66a397b7108082ff5035163964433c1adc21aaa1'  # 后期优化

    cookies = {
        # 'acw_tc': '2760829517219840039894037e90a263295f55b625b7fa3f61766b9c99a3c0',
        'acw_sc__v2': acw_sc__v2,
        'GUID': '4dd12378-ee2e-4575-99ea-4a988375a352',
        'Hm_lvt_9793f42b498361373512340937deb2a0': '1721983680,1721984019',
        'Hm_lpvt_9793f42b498361373512340937deb2a0': '1721984019',
        'HMACCOUNT': '9D54C5252E97E51E',
        'sajssdk_2015_cross_new_user': '1',
        'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%224dd12378-ee2e-4575-99ea-4a988375a352%22%2C%22%24device_id%22%3A%22190ee3ee902c5b-0b75b7bea6e196-26001e51-1327104-190ee3ee9036df%22%2C%22props%22%3A%7B%7D%7D',
    }
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.17k.com/list/493239.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get('https://www.17k.com/top/refactor/top100/06_vipclick/06_click_freeBook_top_100_pc.html',
                            headers=headers, cookies=cookies)
    arg1 = re_rule['arg1'].findall(response.text)
    if arg1 == []:
        return cookies

    else:
        with open('./get_acw_sc__v2.js', 'r') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        acw_sc__v2 = ctx.call('get_arg2', arg1[0])
        cookies = test_req(acw_sc__v2)

        return cookies

# 从csv中导入需要请求的小说url
def read_url():
    CSV_FILE = './book_url_list.csv'
    book_list = []
    with open(CSV_FILE, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            book_list.append(row['url'])
        # logger.info(row['url'])
    return book_list

# 返回字符串的MD5
def calculate_md5(url):
    md5_hash = hashlib.md5(url.encode()).hexdigest()
    return md5_hash

# 异步操作，请求得到小说的章节url
async def chapter_urls(resp_text):
    htm = etree.HTML(resp_text)
    title = htm.xpath('/html/body/div[5]/h1/text()')[0]
    insert_list[0]['id'] = calculate_md5(title)
    insert_list[0]['name'] = title

    logger.info(f'正在下载{title}')
    dls = htm.xpath('//dl[@class="Volume"]')
    for dl in dls[1:]:
        # https://www.17k.com/chapter/493239/10108402.html
        # /chapter/493239/10108402.html
        href = dl.xpath('./dd/a/@href')
        for i in href:
            url = 'https://www.17k.com' + i
            insert_list[0]['urls'].append(url)
            insert_list[0]['md5_urls'].append(calculate_md5(url))
    # 储存到mongodb中
    mongo_instance.db_insert(client_name='novel',title=insert_list[0]['name'],insert_dicts=insert_list)
    return insert_list[0]['urls']

# 异步请求，得到小说章节的内容
async def chapter_content(resp_text):
    htm = etree.HTML(resp_text)
    cha_name = htm.xpath('//*[@id="readArea"]/div[1]/h1/text()')[0]
    ps = htm.xpath('//*[@id="readArea"]/div[1]/div[2]/p')
    cha_content = ''
    for p in ps:
        if '书首发' in p.xpath('./text()')[0]:
            continue
        else:
            cha_content += p.xpath('./text()')[0] + '\n'
    mongo_instance.db_insert(client_name='novel',title=insert_list[0]['name'],insert_dicts=[{
        'cha_name':cha_name,
        'cha_content':cha_content
    }])
    logger.info(f'已下载{cha_name}')

# 设置aiohttp的服务器并请求，返回网页text文本方便处理
async def fetch_data(cookies, url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Referer': 'https://www.17k.com/list/493239.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, cookies=cookies) as response:
            return await response.text()



async def main():
    book_list = read_url()
    for url in book_list[:5]:
        resp_text = await fetch_data(cookies, url)
        urls = await chapter_urls(resp_text)
        tasks = []
        # 批量创建任务
        batch_size = 100
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            batch_tasks = [asyncio.create_task(chapter_content(await fetch_data(cookies=cookies, url=url))) for url in batch_urls]
            tasks.extend(batch_tasks)

        # 同时执行所有任务
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    insert_list = [{
        'md5_name': '',
        'name': '',
        'md5_urls':[],
        'urls': [],
    }]

    re_rule = {
        'arg1': re.compile("var arg1='(.*?)'"),

    }
    mongo_instance = MyMongoDB()

    cookies = test_req('')

    # asyncio.run() 可以方便地运行主函数
    asyncio.run(main())
