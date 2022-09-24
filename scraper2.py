
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/ushakale/Downloads/chromedriver")
browser.get(START_URL)

headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planet_data = []
new_planet_data = []
time.sleep(10)

def scrape():
    for i in range(1, 10):
        while True:
            time.sleep(2)
            soup=BeautifulSoup(browser.page_source, "html.parser")
            c=int(soup.find_all("input", attrs={"class", "page_num"})[0].get("value"))
            if c<i:
                browser.find_element("xpath" , "/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
            elif c>i:
                browser.find_element("xpath" , "/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[1]/a").click()
            else:
                break
        for ultag in soup.find_all("ul", attrs={"class","exoplanet"}):
            l = ultag.find_all("li")
            templist=[]
            for index,item in enumerate(l):
                if index==0:
                    templist.append(item.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(item.contents[0])
                    except:
                        templist.append("")
            hl=l[0]
            templist.append("https://exoplanets.nasa.gov"+ hl.find_all("a",href=True)[0]["href"])
            planet_data.append(templist)
        browser.find_element("xpath" , "/html/body/div[2]/div/div[3]/section[2]/div/section[2]/div/div/article/div/div[2]/div[1]/div[2]/div[1]/div/nav/span[2]/a").click()
def scrapedata2(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        for trtag in soup.find_all("tr", attrs={"class", "fact_row"}):
            tdtags=trtag.find_all("td")
            for t in tdtags:
                try:
                    templist.append(t.find_all("div", attrs={"class","value"})[0].contents[0])
                except:
                    templist.append("")
        new_planet_data.append(templist)
    except:
        time.sleep(1)
        scrapedata2(hyperlink)
scrape()
for index,data in enumerate(planet_data):
    scrapedata2(data[5])
    print("page Done")
    
finalPlanetData=[]
for index,data in enumerate(planet_data):
    e=new_planet_data[index]
    e=[elem.replace("\n","") for elem in e]
    e=e[:7]
    finalPlanetData.append(data+e)
with open("finaldata","w") as f:
    c=csv.writer(f)
    c.writerow(headers)
    c.writerows(finalPlanetData)
    