from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import telebot
from datetime import datetime


URL = "https://chipta.railway.uz/ru/home"
FROM = "Ташкент"
TO = "Самарканд"
DATE = "2022-11-21"



def get_train():

    year,month,_day=DATE.split('-')



    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    fromCity = driver.find_element(By.XPATH, "/html/body/app-root/app-home/section[1]/div[1]/search-panel/div/div/div/form/div[1]/div[1]/input")
    toCity = driver.find_element(By.XPATH, "/html/body/app-root/app-home/section[1]/div[1]/search-panel/div/div/div/form/div[1]/div[2]/input")

    fromCity.click()
    fromlist = driver.find_elements(By.TAG_NAME, "li")[0:-3]
    for city in fromlist:
        if city.text == FROM:
            city.click()
            break

    toCity.click()
    tolist = driver.find_elements(By.TAG_NAME, "li")[0:-3]
    for city in tolist:
        if city.text == TO:
            city.click()
            break

    calendar = driver.find_element(By.XPATH, "/html/body/app-root/app-home/section[1]/div[1]/search-panel/div/div/div/form/div[2]/div[1]/datepicker-adapter/div/div/div")
    calendar.click()
    month_year = driver.find_elements(By.CSS_SELECTOR, ".custom-select option")
    for i in month_year:
        if i.get_attribute("value") == month or i.get_attribute("value") == year:
            i.click()

    days = driver.find_elements(By.CSS_SELECTOR, ".ngb-dp-week .ngb-dp-day")
    start,end, i = -1,-1,0

    for day in days:
        if day.text == "1":
            if start != -1:
                end = i
            else:
                start = i
        i+=1
    days = days[start:end]

    for i in days:
        if i.text == _day:
            i.click()
            break


    searchBtn = driver.find_element(By.XPATH, "/html/body/app-root/app-home/section[1]/div[1]/search-panel/div/div/div/form/div[2]/div[3]/button")
    searchBtn.click()

    sleep(8)

    trains = driver.find_elements(By.CSS_SELECTOR, ".direction__table .direction__list li")

    counter = 0
    for i in trains:
        if i.get_attribute("class") == "direction__item info direction__item--disabled":
            break
        counter+=1
    # trains = trains[0:counter]

    names = driver.find_elements(By.CSS_SELECTOR, ".direction__table .direction__list li .info__badge")
    fromTime = driver.find_elements(By.CSS_SELECTOR, ".direction__table .direction__list li .info__item .bold-big")
    timeLim = []

    for i in range(0,len(fromTime),3):
        st = fromTime[i+1].text
        en = fromTime[i+2].text
        timeLim.append((st,en))

    names = names[0:counter]
    timeLim = timeLim[0:counter]

    trainList = []
    for i in names:
        if i.text == "Afrosiyob" or i.text == "Шарк":
            for i in zip(names, timeLim):
                trainList.append((i[0].text, i[1]))
            return trainList



config = {
    'token':'Your Token'
}


bot = telebot.TeleBot(config['token'])
listening = False


@bot.message_handler(commands=["samtotash"])
def sam_to_tash(message):
    global FROM,TO
    TO = "Ташкент"
    FROM = "Самарканд"
    bot.send_message(message.chat.id, "\nChanged to Samarkand>>Tashkent \n")

@bot.message_handler(commands=["tashtosam"])
def tash_to_sam(message):
    global FROM,TO
    FROM = "Ташкент"
    TO = "Самарканд"
    bot.send_message(message.chat.id, "\nChanged to Tashkent>>Samarkand \n")

@bot.message_handler(commands = ["find"])
def find(message):
    global listening
    listening = True
    bot.send_message(message.chat.id, "\nPlease enter the date as following yyyy-mm-dd: \n")


@bot.message_handler(content_types= ["text"])
def get(message):
    global listening, DATE
    if listening:
        try:
            a,b,c = message.text.split("-")
            a = int(a)
            b = int(b)
            c = int(c)
            assert (a>=datetime.now().year and a<datetime.now().year+2)
            assert (b>=1 and b<13)
            assert (c>=1 and c<32)
            DATE = message.text
            trainList = get_train()
            if trainList:
                bot.send_message(message.chat.id, f"Trains from {FROM} to {TO} on {DATE} are:\n")
                for i in trainList:
                    bot.send_message(message.chat.id, f"{i[0]}  >>  {i[1]}")
            else:
                bot.send_message(message.chat.id, f"No trains from {FROM} to {TO} on {DATE}")
            listening = False 
        except Exception as ex:
            bot.send_message(message.chat.id, f"\n{ex}\n")
            # bot.send_message(message.chat.id, "\nWrong input\n")


bot.polling(none_stop=True)

