from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
import tkinter as tk

def submit():
    global product
    product = name_var.get()
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    driver = webdriver.Chrome('chromedriver',options=option)
    driver.get('https://www.flipkart.com/')
    driver.find_element_by_xpath('/html/body/div[2]/div/div/button').click()
    driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input').send_keys(product)
    driver.find_element_by_xpath('//*[@id="container"]/div/div[1]/div[1]/div[2]/div[2]/form/div/button').click()
    url = driver.current_url
    driver.close()

    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.content , 'lxml')
    product_list = soup.find_all(class_='_4rR01T')
    price_list = soup.find_all(class_='_30jeq3 _1_WHN1')
    rating_list = soup.find_all(class_='_1lRcqv')
    no_of_rating = soup.find_all(class_='_2_R_DZ')
    if len(product_list)==0:
        product_list = soup.find_all(class_='s1Q9rs')
        price_list = soup.find_all(class_='_30jeq3')
        rating_list = soup.find_all(class_='_3LWZlK')
        no_of_rating = soup.find_all(class_='_2_R_DZ')

    for i in range(len(price_list)):
        price_list[i] = price_list[i].text
    for i in range(len(product_list)):
        product_list[i] = product_list[i].text
    for i in range(len(rating_list)):
        rating_list[i] = rating_list[i].text
    for i in range(len(no_of_rating)):
        no_of_rating[i] = no_of_rating[i].text
        no_of_rating[i] = no_of_rating[i].split('R')[0]

    product_dict = dict(zip(product_list , zip(price_list,rating_list,no_of_rating)))
    df = pd.DataFrame(product_dict ,['PRICE','Rating','No.of.Ratings']).T
    writer = pd.ExcelWriter('product_listing.xlsx')
    df.to_excel(writer, 'productListing')
    writer.save()
    tk.Label(root, text="THE DATA HAS BEEN EXPORTED TO THE EXCEL FILE ",font=('calibre', 10, 'bold'),bg='yellow').pack(side=tk.BOTTOM)

root = tk.Tk()
root.geometry("400x200")
root.config(bg = 'yellow')
root.title('FLIPKART PRODUCT SCRAP')
name_var = tk.StringVar()
tk.Label(root, text='PRODUCT NAME', font=('calibre', 10, 'bold'),bg='yellow').place(x=20,y=60)
tk.Entry(root, textvariable=name_var, font=('calibre', 10, 'normal')).place(x=200,y=60)
tk.Button(root, text='IMPORT DETAILS', command=submit).place(x=100,y=100)
root.mainloop()