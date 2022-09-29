from curses import window
import locale
from turtle import down
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import locale
import random

#Internet speed
PROVIDER = 'Your internet provider'
PROMISED_UP = 200 #Megas
PROMISED_DOWN = 100 #Megas

#Twitter login info.
TWITTER_EMAIL = "Your twitter email"
TWITTER_USER = "Your twitter user"
TWITTER_PASSWORD = "Your twitter password"

# ADDING RANDOMNESS IN TINDER BOT
# So we need the bot to behave less robotic-ally.

# Random Sleeping

# For this, I created a function which sleeps for random seconds between actions.

def rand_sleep():
    """
    Method to sleep randomly between 1 to 3 seconds (float)
    This randomness prevents our bot from getting detected by tinder
    :return:
    """
    sleep_sec = random.uniform(2, 4)
    print('Sleeping for {} seconds'.format(str(sleep_sec)))
    sleep(sleep_sec)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

class InternetSpeedTwitterBot():
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        sleep(5)
        # Clicks on privacy and it opens in new window
        self.driver.find_element(By.CSS_SELECTOR, '.start-button').click() #class
        #self.driver.maximize_window()
        #Hay una clase oculta visualmente llamada progreso general que realiza un seguimiento del progreso. 
        # Entonces, cada pocos segundos, verificamos si la prueba terminó. Si es asi, obtenemos los valores.

        speed_tester_progress = ".overall-progress" #class
        download_speed_css = ".download-speed" #class (clase completa: result-data-large number result-data-value download-speed)
        upload_speed_css = ".upload-speed" #class (clase completa: result-data-large number result-data-value upload-speed)
        #Seccion para detectar el avance del test. Basado en la clase oculta "overall progress".
        in_progress = True
        while in_progress:
            progress = self.driver.find_element(By.CSS_SELECTOR, speed_tester_progress).text
            print(progress)
            if progress.startswith("Your speed test has completed"):
                self.down = float(self.driver.find_element(By.CSS_SELECTOR, download_speed_css).text)
                self.up = float(self.driver.find_element(By.CSS_SELECTOR, upload_speed_css).text)
                print(f"Your download speed is {self.down} MBit/s and your upload speed is {self.up} MBit/s")
                in_progress = False
            else:
                sleep(5)

    def tweet_at_provider(self):
        #Creamos el twit que se enviara cada vez que se incumpla la promeza de velocidad de internet.
        twit = f"Hey @{provider}!, por que mi internet es de {self.down}down/{self.up}up cuando me prometieron {PROMISED_DOWN}down/{PROMISED_UP}up??"

        self.driver.get("https://twitter.com/")
        sleep(5)
        # print title of twitter window
        print("First window title = " + self.driver.title)

################ Important fact!!!!!!!! To search by class, when it is composed,
         #it is necessary to replace the spaces with ., so that selenium will recognize that it is a multiple class.
        # Ej:
        #css-901oao r-1awozwy r-6koalj r-18u37iz r-16y2uox r-37j5jr r-a023e6 r-b88u0q r-1777fci r-rjixqe r-bcqeeo r-q4m81j r-qvutc0
        login_button = '.css-901oao.r-1awozwy.r-1cvl2hr.r-6koalj.r-18u37iz.r-16y2uox.r-37j5jr.r-a023e6.r-b88u0q.r-1777fci.r-rjixqe.r-bcqeeo.r-q4m81j.r-qvutc0'
        self.driver.find_element(By.CSS_SELECTOR, login_button).click() #class
    
        #Access to twitter account.
        sleep(5)
        #User 
        search = self.driver.find_element(By.TAG_NAME, 'input')
        search.send_keys(TWITTER_USER)
        self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]').click()
        sleep(5)
        #Password
        search = self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        search.send_keys(TWITTER_PASSWORD)
        print(search.text)
        self.driver.find_element(By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div').click()
        sleep(5)
        #Write a twit
        search = self.driver.find_element(By.CSS_SELECTOR, '.public-DraftStyleDefault-block.public-DraftStyleDefault-ltr')
        search.send_keys(twit)
        #Press key button and post the twitter.
        self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4.css-1dbjc4n.r-l5o3uw.r-42olwf.r-sdzlij.r-1phboty.r-rs99b7.r-19u6a5r.r-2yi16.r-1qi8awa.r-1ny4l3l.r-ymttw5.r-o7ynqc.r-6416eg.r-lrvibr').click()
            
internetspeed = InternetSpeedTwitterBot()
internetspeed.get_internet_speed()
#If up and down speed is lower than promised, write and post the twit.
if internetspeed.up < PROMISED_DOWN or internetspeed.down < PROMISED_DOWN:
    internetspeed.tweet_at_provider()