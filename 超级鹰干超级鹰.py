# encoding  = utf-8
from selenium.webdriver import Chrome
from chaojiying import Chaojiying_Client
import time

web = Chrome()

web.get("http://www.chaojiying.com/user/login/")

web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input").send_keys("18371998539")

web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input").send_keys("415926tX$")
time.sleep(0.5)

# 获得验证码图片
img = web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/div/img").screenshot_as_png
chaojiying = Chaojiying_Client('18371998539', '415926tX$', '951013')
dic = chaojiying.PostPic(img, 1902)
verify_code = dic['pic_str']
time.sleep(2)

web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input").send_keys(verify_code)

web.find_element_by_xpath("/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input").click()








