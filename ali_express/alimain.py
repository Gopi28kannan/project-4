from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from data import Data
from locators import locate
import pandas as pd
import csv

class Test_AliExpress:
    
    item_name=input('search product name : ')
    price1 = input('minimum price value = ')
    price2 = input('maximum price value = ')
    reviews = int(input('maximum reviews = '))
    buy_orders = int(input('maximum buying orders = '))
    csv_file = input('enter save to csv file name : ')
    field_names = ['Product Name', 'Description', 'Images Link', 'Price', 'Product Link']
    csv_name = 'result/'+csv_file+'.csv'
    with open(csv_name, 'w') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = field_names) 
        writer.writeheader()
    
    driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def test_1_get_url(self):
        self.driver.get(Data.datas().url)
        self.driver.maximize_window()
        print("website load successfully completed")
    
    def test_2_search_item(self):
        wait=WebDriverWait(self.driver,10)
        try:
            #close the pop window
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, locate.locates().pop_up))).click()
                print("pop-up window closed")
            except TimeoutException:
                print()
            #search to product
            wait.until(EC.visibility_of_element_located((By.XPATH, locate.locates().search_item))).send_keys(self.item_name)
            self.driver.find_element(By.XPATH, locate.locates().submit_button).click()
            print("product searched")
            #select minimum price
            wait.until(EC.presence_of_element_located((By.XPATH,locate.locates().select_price1))).send_keys(self.price1)
            #select maximum price
            wait.until(EC.presence_of_element_located((By.XPATH,locate.locates().select_price2))).send_keys(self.price2)
            self.driver.find_element(By.XPATH, locate.locates().price_click_ok).click()
            print("price selected")  
        except NoSuchElementException:
            print("click button not cliking in main page")
        except TimeoutException:
            print('Page link not loaded')

    def open_item(self):
        wait=WebDriverWait(self.driver,10)
        #switch to windows page control
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            #get review counts
            reviews = self.driver.find_elements(By.XPATH,locate.locates().review)
            reviews_length=len(reviews)
            if reviews_length !=0:
                for review in reviews:
                    review_text=review.text
                    review_num=int(''.join([n for n in review_text if n.isdigit()]))
            else:
                review_num = 0
            
            #get buy order counts
            solds = self.driver.find_elements(By.XPATH,locate.locates().buy_orders)
            solds_length=len(solds)
            if solds_length !=0:
                last_sold= solds[-1]
                sold_text=last_sold.text
                sold_num=int(''.join([n for n in sold_text if n.isdigit()]))
            else:
                sold_num=0
            
            #check to reviews and buy orders
            if review_num <=self.reviews and sold_num <=self.buy_orders:
                #get product name
                p_name =self.driver.find_element(By.XPATH, locate.locates().product_name).text
                Product_name = 'Product Name : \n'+p_name
                #print('Product Name : \n',Product_name)

                #scroll down page in 1200pixels
                self.driver.execute_script("window.scrollTo(0, 1200)")
                
                #get description
                try:
                    click_des = wait.until(EC.visibility_of_element_located((By.XPATH,locate.locates().click_description)))
                    click_des.click()
                    try:
                        Description = wait.until(EC.presence_of_element_located((By.ID, locate.locates().description)))    
                        Des = '\nDescription : \n'+Description.text+'\n'
                        #print('Description : \n',Des)
                    except TimeoutException:
                        Des = '\nDescription : \n Not found description \n'
                        #print('Description : not found description')
                    
                except TimeoutException:
                    Description = "\nDescription : \nNone \n"
                    #print('Description : None')

                #get image links
                images_link=[]
                try:
                    Image_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, locate.locates().image_link)))
                    #print("Image Links : ")
                    for link in Image_links:
                        img_li = link.get_attribute("src")
                        #print(img_li)
                        images_link.append(img_li)
                        
                except TimeoutException:
                    try:
                        self.driver.execute_script("window.scrollTo(1200,0)")
                        Image_links = wait.until(EC.presence_of_all_elements_located((By.XPATH, locate.locates().image_link_1)))
                        #print("Image Links : ")
                        for link in Image_links:
                            img_li = link.get_attribute("src")
                            #print(img_li)
                            images_link.append(img_li)

                    except TimeoutException:
                        Image_links = self.driver.find_elements(By.XPATH, locate.locates().image_link_2)
                        #print("Image Links : ")
                        for link in Image_links:
                            img_li = link.get_attribute("src")
                            #print(img_li)
                            images_link.append(img_li)
                            
                images_link1= 'Images Link : ',images_link

                #get price
                Price1 = self.driver.find_element(By.XPATH, locate.locates().price).text 
                Price = '\nPrice : '+Price1
                #print('Price = ', Price)
                
                #get product link
                Product_link = '\nProduct Link : '+self.driver.current_url
                #print('Product Link : \n',Product_link)

                # open csv file and add to collected data
                table=[]
                table_dict = {'Product Name': Product_name, 'Description': Des,'Images Link': images_link1, 'Price': Price, 'Product Link': Product_link}
                table.append(table_dict)
                try:
                    with open(self.csv_name, 'a') as adds:
                        writer = csv.DictWriter(adds, fieldnames = self.field_names)
                        writer.writerows(table)
                    print('Data added in csv file')
                except:
                    print("Data None")
                time.sleep(1)
                # clear table and images_link data
                table.clear()
                images_link.clear()
            
        except NoSuchElementException as error:
            print('webpage item not showed : \n', error)
        except TimeoutException  as error:
            print("webpage item not showed because timeout :\n",error)

        print('item closed')
        print('----------------------------------------------------------------------------------------------')
        self.driver.close()

             
    def select_items(self):
        wait=WebDriverWait(self.driver,10)
        try:
            time.sleep(10)
            #run to 100 items
            n=1
            while n<=100:
                try:
                    #collect items
                    items=wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, locate.locates().items+str(n))))
                    print('Item ',n,' is selected and open for item')
                    for item in items:
                        highlight = ActionChains(self.driver)
                        #highlight the item
                        highlight.move_to_element(item).perform()
                        time.sleep(2)
                        # click to open new tab in highlighted item
                        item.click()
                        time.sleep(1)
                        # Go to open_item def
                        self.open_item()
                        #switch to windows page control
                        self.driver.switch_to.window(self.driver.window_handles[0])
                        time.sleep(1)
                except TimeoutException:
                    break
                n=n+1
        except NoSuchElementException as selenium_error:
            print("select_items :\n",selenium_error)

    def test_3_click_next_page(self):
        wait=WebDriverWait(self.driver,10)
        print("current page : 1")
        # go to select_items def
        self.select_items()
        print('=======================================================================')
        try:
            for i in range(1,1000+1):
                next_page_false = self.driver.find_elements(By.XPATH, locate.locates().click_next_2)
                next_p = len(next_page_false)
                #next page false is 0, run to if
                if next_p == 0:
                    highlight = ActionChains(self.driver)
                    try:
                        #go to next page
                        click_next = self.driver.find_element(By.XPATH, locate.locates().click_next_1)
                        highlight.move_to_element(click_next).perform()
                        time.sleep(2)
                        click_next.click()
                    except NoSuchElementException:
                        print("webpage products not showed")
                        break
                    time.sleep(2)
                    print('current page : ',i+1)
                    self.select_items()
                    print('=======================================================================')
                # next page false is 1, run to else
                else:
                    print('=======================================================================')
                    print("All data collected")
                    break
        except NoSuchElementException as selenium_error:
            print('webpage products not showed and next button not showed')
                
        
ali = Test_AliExpress()
ali.test_1_get_url()
ali.test_2_search_item()
ali.test_3_click_next_page()
    

    
