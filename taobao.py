import tkinter
import time

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver import Proxy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from pyquery import PyQuery as pq
# 实例化一个Ｃｈｒｏｍｅ浏览器的配置选项
from selenium.webdriver.common.by import By
from selenium import webdriver

import pymysql

win = tkinter.Tk()

win.title("yudanqu")

# win.geometry("400x400+200+50")


win.geometry('500x300')  # 这里的乘是小x

# 第4步，在图形界面上创建 500 * 200 大小的画布并放置各种元素
# canvas = tkinter.Canvas(win, bg='green', height=100, width=200)
# # 说明图片位置，并导入图片到画布上
# image_file = tkinter.PhotoImage(file='/home/python/Desktop/selenium淘宝/GUI/photo2.png')  # 图片位置（相对路径，与.py文件同一文件夹下，也可以用绝对路径，需要给定图片具体绝对路径）
# image = canvas.create_image(250, 0, anchor='n',image=image_file)

conn = pymysql.connect(host='127.0.0.1', port=3306, database='tb', user='root', password='mysql', charset='utf8')
cs1 = conn.cursor()


def getserach():
    global serach
    serach = entry_serach_name.get()


def showinfo():
    name = entry_usr_name.get()
    password = entry_usr_pwd.get()

    # chrome_option = webdriver.ChromeOptions()
    # # driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    # # # 最大化窗口
    # # driver.maximize_window()
    # chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
    #
    # driver = webdriver.Chrome(options=chrome_option)


    # proxy = Proxy(
    #     {
    #
    #         'httpProxy': '47.101.179.211:3111'  # 代理ip和端口
    #     }
    # )
    # 新建一个“期望的技能”，哈哈
    # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    # 把代理ip加入到技能中
    # proxy.add_to_capabilities(desired_capabilities)

    driver = webdriver.PhantomJS(executable_path=(r'E:\phantom\phantomjs-2.1.1-windows\bin\phantomjs.exe'),service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    # service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']

    driver.maximize_window()

    # proxy = Proxy(
    #     {
    #
    #         'httpProxy': '47.101.179.211:3111'  # 代理ip和端口
    #     }
    # )
    # # 新建一个“期望的技能”，哈哈
    # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    # # 把代理ip加入到技能中
    # proxy.add_to_capabilities(desired_capabilities)
    #
    # driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities,
    #                              service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
    # service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1']

    # # 最大化窗口
    # driver.maximize_window()

    # # 解析url
    # driver.get('https:/login.taobao.com/member/login.jhtml')

    time.sleep(1)

    # 请求登录页
    driver.get("https:/login.taobao.com/member/login.jhtml")

    # 点击密码登陆
    driver.find_element_by_id("J_Quick2Static").click()

    # 点击微博登陆
    driver.find_element_by_xpath("//*[@id='J_OtherLogin']/a[1]").click()

    # 输入账号密码
    driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[2]/div/input").send_keys(name)
    driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[3]/div/input").send_keys(password)
    driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[7]/div[1]/a").click()
    time.sleep(5)

    # driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[4]/div/a[1]/img").click()
    time.sleep(1)
    # image_href = driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[4]/div/a[1]/img/@src")
    # print(image_href)
    png = driver.save_screenshot(r'photo.png')  # 一次截图：形成全图
    # image_href = driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[4]/div/a[1]/img/@src")

    # 定位验证码
    tupian = driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[4]/div/a[1]/img")

    locations = tupian.location

    print(locations)

    # 图片大小
    sizes = tupian.size
    print(sizes)

    # 构造指数的位置，计算出需要截图的长宽、高度等

    # 定位截图
    rangle = (
        int(locations['x']), int(locations['y']), int(locations['x'] + sizes['width']),
        int(locations['y'] + sizes['height']))

    # top = tupian.location['x']
    # left = tupian.location['y']
    # right = left+tupian.size['width']
    # bottom = top+tupian.size['height']
    #


    picture = Image.open(r'photo.png')
    # 二次截图
    picture = picture.crop((rangle))
    picture.save(r'photo2.png')
    time.sleep(3)

    import requests
    from hashlib import md5

    # 　使用第三方打码平台　解析验证码　
    class Chaojiying_Client(object):
        def __init__(self, username, password, soft_id):
            self.username = username
            password = password.encode('utf8')
            self.password = md5(password).hexdigest()
            self.soft_id = soft_id
            self.base_params = {
                'user': self.username,
                'pass2': self.password,
                'softid': self.soft_id,
            }
            self.headers = {
                'Connection': 'Keep-Alive',
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
            }

        def PostPic(self, im, codetype):
            """
            im: 图片字节
            codetype: 题目类型 参考 http://www.chaojiying.com/price.html
            """
            params = {
                'codetype': codetype,
            }
            params.update(self.base_params)
            files = {'userfile': ('ccc.jpg', im)}
            r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                              headers=self.headers)
            return r.json()

        def ReportError(self, im_id):
            """
            im_id:报错题目的图片ID
            """
            params = {
                'id': im_id,
            }
            params.update(self.base_params)
            r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params,
                              headers=self.headers)
            return r.json()

    chaojiying = Chaojiying_Client('15655386731', 'zhw131420', '900603')  # 用户中心>>软件ID 生成一个替换 96001
    im = open('photo2.png', 'rb').read()  # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    a = chaojiying.PostPic(im, 1902)  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    code = a['pic_str']
    print("验证码是：" + code)

    # 输入验证码
    driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[4]/div/input").send_keys(code)

    # 点击登陆
    driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[7]/div[1]/a").click()
    # driver.find_element_by_xpath("//*[@id='pl_login_logged']/div/div[7]/div[1]/a").click()

    print("已经点击登陆")
    time.sleep(6)

    driver.save_screenshot(r'点击登陆后.png')  # 一次截图：形成全图

    # # 定位滑块元素
    # source = driver.find_element_by_xpath("//*[@id='nc_1_n1z']")
    #
    # # # # 定义鼠标拖放动作
    # # ActionChains(driver).drag_and_drop_by_offset(source, 100, 0).perform()
    # # ActionChains(driver).drag_and_drop_by_offset(source, 140, 0).perform()
    # # ActionChains(driver).drag_and_drop_by_offset(source, 260, 0).perform()
    # # time.sleep(2)
    #
    # ActionChains(driver).click_and_hold(on_element=source).perform()
    # time.sleep(0.15)
    # ActionChains(driver).move_to_element_with_offset(to_element=source, xoffset=100, yoffset=0).perform()
    # time.sleep(0.1)
    # ActionChains(driver).move_to_element_with_offset(to_element=source, xoffset=30, yoffset=0).perform()
    # ActionChains(driver).move_to_element_with_offset(to_element=source, xoffset=60, yoffset=0).perform()
    # time.sleep(0.5)
    # ActionChains(driver).move_to_element_with_offset(to_element=source, xoffset=200, yoffset=0).perform()




    wait = WebDriverWait(driver, 20)  # 超时时长为20s
    time.sleep(3)

    driver.find_element_by_id('q').send_keys(serach)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="J_TSearchForm"]/div[1]/button').click()

    time.sleep(3)
    # 进行向下滑动

    num = 0
    while True:
        if num == 0:
            sroll_cnt = 0

            while True:
                if sroll_cnt < 4:
                    driver.execute_script('window.scrollBy(0, 1300)')
                    time.sleep(1)
                    sroll_cnt += 1
                else:
                    break
        else:
            sroll_cnt = 0

            while True:
                if sroll_cnt < 4:
                    driver.execute_script('window.scrollBy(0, 1050)')
                    time.sleep(1)
                    sroll_cnt += 1
                else:
                    break

        lists = driver.find_elements_by_xpath("//div[@class='items']/div")
        for list in lists:
            shop_name = list.find_element_by_xpath(".//div[2]/div[3]/div[1]/a").text
            address = list.find_element_by_xpath(".//div[2]/div[3]/div[2]").text
            title = list.find_element_by_xpath(".//div[2]/div[2]/a").text
            price = list.find_element_by_xpath(".//div[2]/div[1]/div[1]/strong").text
            people = list.find_element_by_xpath(".//div[2]/div[1]/div[2]").text
            # 从第二行开始添加数据
            sql = "insert into sousuo(good_name,good_address,good_title,good_price,good_people) values(%s,%s,%s,%s,%s)"
            cs1.execute(sql, [shop_name, address, title, price, people])

            print(shop_name, address, title, price, people)
        num += 1
        print("*************第{}页打印完成".format(num))

        if num == 100:
            conn.commit()
            conn.close()
            tkinter.Label(win, text='已经存入数据库，请关闭程序！', font=('Arial', 14)).place(x=10, y=220)
            break
        else:

            time.sleep(1)
            next_button = driver.find_element_by_css_selector('li.item.next')  # 翻页按钮
            if 'next-disabled' not in next_button.get_attribute('class'):
                next_button.click()
                time.sleep(0.5)


tkinter.Label(win, text='请输入搜索词:', font=('Arial', 12)).place(x=10, y=30)
var_serach_name = tkinter.StringVar()
entry_serach_name = tkinter.Entry(win, textvariable=var_serach_name, font=('Arial', 14))
entry_serach_name.place(x=120, y=30)

button1 = tkinter.Button(win, text="确定", command=getserach).place(x=180, y=60)

tkinter.Label(win, text='User name:', font=('Arial', 14)).place(x=10, y=130)
tkinter.Label(win, text='Password:', font=('Arial', 14)).place(x=10, y=160)

# 第6步，用户登录输入框entry
# 用户名
var_usr_name = tkinter.StringVar()
entry_usr_name = tkinter.Entry(win, textvariable=var_usr_name, font=('Arial', 14))
entry_usr_name.place(x=120, y=130)
# 用户密码
var_usr_pwd = tkinter.StringVar()
entry_usr_pwd = tkinter.Entry(win, textvariable=var_usr_pwd, font=('Arial', 14), show='*')
entry_usr_pwd.place(x=120, y=160)

button2 = tkinter.Button(win, text="登陆", command=showinfo).place(x=180, y=200)

win.mainloop()
