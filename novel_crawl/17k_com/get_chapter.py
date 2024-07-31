# encoding  = utf-8
import hashlib
from MyMongoDB import MyMongoDB
from lxml import etree
from loguru import logger
import aiohttp
import asyncio
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # windows系统请求https网站报错时调用此方法
import re, requests, csv
import random
from fake_useragent import UserAgent
import execjs


# def open_proxy():
#     # with open('./proxies.txt', 'r') as f:
#     #     #一行一行读取
#     #     ips = [line.strip() for line in f]
#     #     ip = random.choice(ips)
#     #     ip = str(ip)
#     #     proxy = {
#     #         'http':ip,
#     #         'https':ip,
#     #     }
#     #     logger.info(proxy)
#     # 隧道域名:端口号
#     tunnel = "x166.kdltpspro.com:15818"
#
#     # 用户名和密码方式
#     username = "t12234287674421"
#     password = "duaignd3"
#
#     proxy_auth = aiohttp.BasicAuth(username, password)
#     return proxy

# 测试参数是否需要更新

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


# 更新请求头和代理
async def ua_proxy(str_judge):
    USER_AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36'
    ]
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
        'User-Agent': UserAgent().random,
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }  # 随机选择UA

    # 隧道域名:端口号
    tunnel = "快代理的tunnel"

    # 用户名密码方式
    username = "username"
    password = "password"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel},
        "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": tunnel}
    }
    proxy_auth = aiohttp.BasicAuth(username, password)
    if str_judge == 'proxies':
        return headers, proxies
    elif str_judge == 'proxy_auth':
        return headers, proxy_auth
    else:
        print('请输入正确的字符串')


# 返回新的cookie
async def cookies_params(arg1):
    with open('./get_acw_sc__v2.js', 'r') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    acw_sc__v2 = ctx.call('get_arg2', arg1[0])
    cookies = {'acw_sc__v2': acw_sc__v2}
    return cookies


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
    mongo_instance.db_insert(client_name='novel', title=insert_list[0]['name'], insert_dicts=insert_list)
    return insert_list[0]['urls']


# 异步请求，得到小说章节的内容
async def chapter_content(resp_text):
    htm = etree.HTML(resp_text)
    if htm.xpath('//*[@id="readArea"]/div[1]/h1/text()'):
        cha_name = htm.xpath('//*[@id="readArea"]/div[1]/h1/text()')[0]
    else:
        cha_name = ''
    if htm.xpath('//*[@id="readArea"]/div[1]/div[2]/p'):
        ps = htm.xpath('//*[@id="readArea"]/div[1]/div[2]/p')
    else:
        ps = []
    cha_content = ''
    if ps:
        for p in ps:
            if (p.xpath('./text()') != []) and ('书首发' in p.xpath('./text()')[0]):
                continue
            else:
                cha_content += p.xpath('./text()')[0] + '\n'
        mongo_instance.db_insert(client_name='novel', title=insert_list[0]['name'], insert_dicts=[{
            'cha_name': cha_name,
            'cha_content': cha_content
        }])
        logger.info(f'已下载{cha_name}')


# 设置aiohttp的服务器，请求网页
async def fetch_data(num, headers, proxy_auth, cookies, url):
    # aiohttp默认使用严格的HTTPS协议检查。可以通过将ssl设置为False来放松认证检查
    # async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
    if num == 0:  # 如果num为0 则是请求处理章节内容页面
        async with aiohttp.ClientSession() as session:
            tunnel = "x166.kdltpspro.com:15818"
            try:
                async with session.get(url, headers=headers, cookies=cookies, proxy="http://" + tunnel,
                                       proxy_auth=proxy_auth) as response:
                    # response.raise_for_status()  # 检查状态，如果不是 200 会抛出异常
                    resp_text = await response.text()
                    arg1 = re_rule['arg1'].findall(resp_text)
                    if arg1 == []:
                        await chapter_content(resp_text)
                    else:
                        headers, proxy_auth = await ua_proxy('proxy_auth')
                        cookies = await cookies_params(arg1)
                        async with session.get(url, headers=headers, cookies=cookies, proxy="http://" + tunnel,
                                               proxy_auth=proxy_auth) as response:
                            response.raise_for_status()  # 检查状态，如果不是 200 会抛出异常
                            resp1_text = await response.text()  # 返回响应内容
                            await chapter_content(resp1_text)
            except aiohttp.ClientResponseError as e:
                logger.info(f"Second request failed with proxy {proxy_auth}: {e}")
    elif num == 1:  # 如果num为1 则是请求处理章节的url
        async with aiohttp.ClientSession() as session:
            tunnel = "快代理的tunnel"
            try:
                async with session.get(url, headers=headers, cookies=cookies, proxy="http://" + tunnel,
                                       proxy_auth=proxy_auth) as response:
                    # response.raise_for_status()  # 检查状态，如果不是 200 会抛出异常
                    resp_text = await response.text()
                    arg1 = re_rule['arg1'].findall(resp_text)
                    if arg1 == []:
                        return resp_text
                    else:
                        headers, proxy_auth = await ua_proxy('proxy_auth')
                        cookies = await cookies_params(arg1)
                        async with session.get(url, headers=headers, cookies=cookies, proxy="http://" + tunnel,
                                               proxy_auth=proxy_auth) as response:
                            response.raise_for_status()  # 检查状态，如果不是 200 会抛出异常
                            resp1_text = await response.text()  # 返回响应内容
                            return resp1_text
            except aiohttp.ClientResponseError as e:
                pass
                # logger.info(f"Second request failed with proxy {proxy_auth}: {e}")


async def main():
    global headers, proxy_auth, cookies
    cookies = {}
    headers, proxy_auth = await ua_proxy('proxy_auth')
    book_list = read_url()
    for url in book_list[:5]:
        logger.info('download novel')
        resp_text = await fetch_data(1, headers, proxy_auth, cookies, url)
        urls = await chapter_urls(resp_text)  # 得到url列表
        tasks = []
        # 批量创建任务
        batch_size = 10
        for i in range(0, len(urls), batch_size):
            batch_urls = urls[i:i + batch_size]
            batch_tasks = [asyncio.create_task(fetch_data(0, headers, proxy_auth, cookies, url)) for url in batch_urls]
            tasks.extend(batch_tasks)
            await asyncio.sleep(0.1)

        # 同时执行所有任务
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    insert_list = [{
        'md5_name': '',
        'name': '',
        'md5_urls': [],
        'urls': [],
    }]
    re_rule = {
        'arg1': re.compile("var arg1='(.*?)'"),

    }
    mongo_instance = MyMongoDB()

    # asyncio.run() 可以方便地运行主函数
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
