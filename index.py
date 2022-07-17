from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from time import sleep

def initDriver():
    CHROMEDRIVER_PATH = '/usr/bin/chromedriver'
    WINDOW_SIZE = "1920,1080"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-blink-features=AutomationControllered")
    chrome_options.add_experimental_option('useAutomationExtension', False)
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--start-maximized")  # open Browser in maximized mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options
                              )
    return driver
    
def convertToCookie(cookie):
    try:
        new_cookie = ["c_user=", "xs="]
        cookie_arr = cookie.split(";")
        for i in cookie_arr:
            if i.__contains__('c_user='):
                new_cookie[0] = new_cookie[0] + (i.strip() + ";").split("c_user=")[1]
            if i.__contains__('xs='):
                new_cookie[1] = new_cookie[1] + (i.strip() + ";").split("xs=")[1]
                if (len(new_cookie[1].split("|"))):
                    new_cookie[1] = new_cookie[1].split("|")[0]
                if (";" not in new_cookie[1]):
                    new_cookie[1] = new_cookie[1] + ";"

        conv = new_cookie[0] + " " + new_cookie[1]
        if (conv.split(" ")[0] == "c_user="):
            return
        else:
            return conv
    except:
        print("Error Convert Cookie")

def loginFacebookByCookie(driver ,cookie):
    try:
        cookie = convertToCookie(cookie)
        print(cookie)
        if (cookie != None):
            script = 'javascript:void(function(){ function setCookie(t) { var list = t.split("; "); console.log(list); for (var i = list.length - 1; i >= 0; i--) { var cname = list[i].split("=")[0]; var cvalue = list[i].split("=")[1]; var d = new Date(); d.setTime(d.getTime() + (7*24*60*60*1000)); var expires = ";domain=.facebook.com;expires="+ d.toUTCString(); document.cookie = cname + "=" + cvalue + "; " + expires; } } function hex2a(hex) { var str = ""; for (var i = 0; i < hex.length; i += 2) { var v = parseInt(hex.substr(i, 2), 16); if (v) str += String.fromCharCode(v); } return str; } setCookie("' + cookie + '"); location.href = "https://mbasic.facebook.com"; })();'
            driver.execute_script(script)
            sleep(5)
    except:
        print("Error login")
        
def checkLiveCookie(driver, cookie):
    try:
        driver.get('https://mbasic.facebook.com/')
        sleep(1)
        driver.get('https://mbasic.facebook.com/')
        sleep(2)
        loginFacebookByCookie(driver ,cookie)

        return checkLiveClone(driver)
    except:
        print("check live fail")
        
cookie = 'sb=yJbCXsJLnUu0Y1WfvQZ8iWj3; datr=yZbCXtoUH86JyEBG2JMLd4Xn; dpr=0.8999999761581421; locale=vi_VN; wd=1517x741; c_user=100034043707544; xs=28%3AC2zTXO3zh6Z7wA%3A2%3A1658049295%3A-1%3A6176; fr=0Z2Emg9ecREaupco8.AWWRC73IAbJCpds-MnbP31crfIE.Bi09Jy.t6.AAA.0.0.Bi09P9.AWW5U8OAaJo; presence=C%7B%22t3%22%3A%5B%5D%2C%22utc3%22%3A1658049542012%2C%22v%22%3A1%7D'
driver = initDriver()
isLive = checkLiveCookie(driver, cookie)
