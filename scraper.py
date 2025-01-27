from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"

browser=webdriver.chrome(service=ChromeService(ChromeDriverManager().install()))
browser.get(START_URL)
time.sleep(10)

planets_data=[]

def scrape():
    for i in range(0,10):
        print(f'coletando dados da página{i+1}...')
        
        soup=BeautifulSoup(browser.page_source,'html.parser')
        for ul_tag in soup.find_all('ul',attrs={"class","exoplanet"}):
            li_tags=ul_tag.find_all('li')
    
            temp_list=[]
            
            for index,li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
                        
            planets_data.append(temp_list)
        browser.find_element(by=By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        
scrape() 

headers=["name","light_years_from_earth","planet_mass","stellar_magnitude","discovery_date"]

planet_df_1=pd.DataFrame(planets_data,columns=headers)

planet_df_1.to_csv("scraped_data.csv",index=True,index_label="id")                           