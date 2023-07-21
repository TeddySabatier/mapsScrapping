from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os
import time

numFichier=0
class GoogleMapsScraper:
    def __init__(self,headless=False):
        self.headless=headless
        self.Data={'Title':[],'Address':[],'Time':[],'Link':[],'Phone':[],'Mark':[],'GmapLink':[],'Keyword':[],'City':[]}
        options=Options()
        options.add_experimental_option("detach", True)
        if headless:
            options.headless=True
        else:
            options.headless=False

        self.driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
        
    def SearchMaps(self,places,cities):
        doublons=0

        global numFichier
        self.driver.get("https://www.google.com/maps/search/")
        #wait till the accept button on maps load
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']")))
        #click the restaurant button to get nearest places 
        self.driver.find_element_by_xpath("//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']").click()
        counterSave=0
        for place in places:
            for city in cities:
                #first page
                self.driver.get("https://www.google.com/maps/search/"+place+" "+city)
                try:
                    element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']")))
                     #click the restaurant button to get nearest places 
                    self.driver.find_element_by_xpath("//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']").click()
                except:
                    pass
                try:
                    #If google maps is unable to search the place
                    NotFound=self.driver.find_element_by_xpath("//*[@class='IPum6b']")
                    return "Search Not found"     #try improving your search keywords
                
                except:
              
                    try:    
                        #scroll 2 times to load all the places. "initially data of only 4 is loaded"
                        counter=0
                        end_scrolling=True
                        while(end_scrolling and counter < 600):
                            try:
                                self.driver.find_element_by_xpath("//*[@class='HlvSq']")
                                end_scrolling=False
                                print("Fini")
                            except:
                                counter=counter+1
                                end_scrolling=True
                                time.sleep(1)
                                scroll=self.driver.find_elements_by_xpath("//a[@jsan='7.hfpxzc,0.aria-label,8.href,0.jsaction,0.jslog']")
                                scroll[-1].send_keys(Keys.END)
                                
             


                    except:
                        print("end")

                 
                    #fetch places data# an store in rest
                    fetched_restaurants=self.driver.find_elements_by_xpath("//*[@class='hfpxzc']")
                    links=[]
                    #iterate over all places data and store its datas
                    for res in fetched_restaurants:
                        links.append(res.get_attribute("href"))
                    print(len(links))

                    for link_ in links:
                        self.driver.get(link_)
                        try:
                            title=self.driver.find_element(By.XPATH, '//h1[@class="DUwDvf fontHeadlineLarge"]/span[1]').text
                        except:
                            title="none"
                        try:
                            adress=self.driver.find_element(By.XPATH, "//*[@data-item-id='address']/div[1]/div[2]/div[1]").text
                        except:
                            adress="none"
                        try:
                            hours=self.driver.find_element(By.XPATH, "//*[@class='t39EBf GUrTXd']").get_attribute('aria-label')
                        except:
                            hours="none"
                        try:
                            link=self.driver.find_element(By.XPATH, "//*[@data-item-id='authority']").get_attribute('href')
                        except:
                            link="none"
                        try:
                            phone=self.driver.find_element(By.XPATH, "//*[contains (@data-item-id,'phone')]/div[1]/div[2]/div[1]").text
                        except:
                            phone="none"
                        try:
                            mark=self.driver.find_element(By.XPATH, '//div[@class="F7nice mmu3tf"]/span[1]/span[1]/span[1]').text
                        except:
                            mark="none"
                        if phone not in self.Data['Phone'] :
                            self.Data['Title'].append(title)
                            self.Data['Address'].append(adress)
                            self.Data['Time'].append(hours)
                            self.Data['Link'].append(link)                
                            self.Data['Phone'].append(phone)
                            self.Data['Mark'].append(mark)
                            self.Data['GmapLink'].append(link_)
                            self.Data['Keyword'].append(place)
                            self.Data['City'].append(city)
                        else:
                            if phone =='none':
                                self.Data['Title'].append(title)
                                self.Data['Address'].append(adress)
                                self.Data['Time'].append(hours)
                                self.Data['Link'].append(link)                
                                self.Data['Phone'].append(phone)
                                self.Data['Mark'].append(mark)
                                self.Data['GmapLink'].append(link_)
                                self.Data['Keyword'].append(place)
                                self.Data['City'].append(city)
                            else:
                                doublons=doublons+1
                counterSave=counterSave+1
                if(counterSave==10):
                    print(str(counterSave)+':'+str(numFichier))
                    name='data'+str(numFichier)+'.xlsx'
                    pd.DataFrame(self.Data).to_excel(name,index=False)
                    self.Data.clear()
                    self.Data={'Title':[],'Address':[],'Time':[],'Link':[],'Phone':[],'Mark':[],'GmapLink':[],'Keyword':[],'City':[]}
                    self.driver.delete_all_cookies()
                    counterSave=0
                    numFichier=numFichier+1

        print("Doublons: "+str(doublons))
        return (self.Data)
            
            
        
            
#main
gs=GoogleMapsScraper()

cities=open(os.getcwd()+"/Cities.txt").readlines()
places=open(os.getcwd()+"/Places.txt").readlines()
p=gs.SearchMaps(places,cities)
name='data'+str(numFichier)+'.xlsx'
pd.DataFrame(p).to_excel(name,index=False)

