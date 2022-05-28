from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

path = r"C:/chromedriver_win32/chromedriver.exe"
# 进入浏览器设置
chrome_options = Options()

# 设置中文
chrome_options.add_extension('D:/code/spider/chrome_plugin/src.crx')

chrome_options.add_argument('lang=zh_CN.UTF-8')
driver = webdriver.Chrome(executable_path=path, options=chrome_options)
driver.get("https://www2.javhdporn.net/video/juy-328/")
driver.maximize_window()
time.sleep(3)

ActionChains(driver).move_by_offset(
    531, 272).click().perform()  # 鼠标左键点击， 200为x坐标， 100为y坐标
# ActionChains(driver).move_by_offset(
#     531, 272).context_click().perform()  # 鼠标右键点击
