import undetected_chromedriver as uc
import time 
import xlwt

from xlwt import Workbook
from selenium.webdriver.common.by import By 
from datetime import date

driver = uc.Chrome(version_main=109)
today = date.today()

driver.get('https://batdongsan.com.vn/cho-thue-nha-rieng-ba-dinh')
time.sleep(5)

# get list element in page
lst = [element.get_attribute("href") for element in driver.find_elements(By.CSS_SELECTOR, "#product-lists-web a")]

wb = Workbook()
sheet1 = wb.add_sheet('Sheet 1')

print(lst)

cnt = 0
for itm in lst: 
    if itm == None or itm == "":
        continue

    try:
        driver.get(itm) # go to each detail page
        time.sleep(3)
    except:
        print(itm)
        wb.save('batdongsang.com.vn.xlsx')

    title = driver.find_element(By.CSS_SELECTOR, "h1[class*=title]").text
    path_menu = driver.find_element(By.CSS_SELECTOR, "[class*=re__breadcrumb]").text

    province = None
    district = None

    try:
        path_menu_lst = path_menu.split("/")
        province = path_menu_lst[1]
        district = path_menu_lst[2]
    except:
        province = None
        district = None

    address = driver.find_element(By.CSS_SELECTOR, "h1 + span").text
    description = driver.find_element(By.CSS_SELECTOR, "[class*=re__pr-description] > div").text

    phone_number = None
    try:
        phone_number = driver.find_element(By.CSS_SELECTOR, "[class*=re__pr-scrollbar-tablet] > a").get_attribute("data-href")
        phone_number = phone_number.replace("sms://", "")
        phone_number = phone_number.split("/")[0]
    except: 
        phone_number = None

    owner = driver.find_element(By.CSS_SELECTOR, "[class*=re__contact-name] > a").text
    
    print("Title: " + title)
    print("Path Menu: " + path_menu)
    print("Address: " + address)
    print("Description: " + description)
    print("Phone Number: " + phone_number)
    print("Owner: " + owner)

    sheet1.write(cnt, 0, today.strftime("%d/%m/%Y"))
    sheet1.write(cnt, 1, title)
    sheet1.write(cnt, 2, path_menu)
    sheet1.write(cnt, 3, province)
    sheet1.write(cnt, 4, district)
    sheet1.write(cnt, 5, address)
    sheet1.write(cnt, 6, description)
    sheet1.write(cnt, 7, phone_number)
    sheet1.write(cnt, 8, owner)

    cnt += 1

wb.save('batdongsan.xlsx')

driver.close()
