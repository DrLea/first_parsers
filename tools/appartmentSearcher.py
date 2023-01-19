from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

URL = "https://www.olx.uz/d/nedvizhimost/kvartiry/arenda-dolgosrochnaya/tashkent/q-rent-apartment/?currency=UZS&search%5Bfilter_float_price:from%5D=2000000&search%5Bfilter_float_price:to%5D=6000000"
path = "D:\chromeDriver\chromedriver.exe"

# resp = requests.get(URL)
# resp.raise_for_status()
# soup = BeautifulSoup(resp.text, "html.parser")

# # print(soup.prettify())
# apparts = soup.find_all("div", _class="css-19ucd76")
# print(apparts)

driver = webdriver.Chrome(executable_path=path)
driver.get(URL)
apparts = driver.find_elements(By.CLASS_NAME, "css-19ucd76")
links = driver.find_elements(By.CLASS_NAME, "css-1bbgabe")
prices = []
descriptions = []
purelinks = []

for i in apparts:
    ap = i.text.split('\n')
    descriptions.append(ap[0])
    prices.append(ap[1])

for i in links:
    purelinks.append(i.get_attribute("href"))




for i in range(len(apparts)-1):
    sleep(1)

    driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfkapEN8OTLiizCCazLwWa_myJzq_3b5cV0Cod0Zy_5fkcc4A/viewform?usp=sf_link")
    description = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[2]/textarea')
    price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div[2]/textarea')
    send = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')

    if descriptions[i]=="Сохранить параметры поиска":
        continue


    try:
        description.send_keys(descriptions[i])
        price.send_keys(prices[i])
        link.send_keys(purelinks[i])
        send.click()
    except:
        pass



    
input()
