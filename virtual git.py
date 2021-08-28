import pyttsx3 
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes
import requests, json
from selenium import webdriver
from time import sleep
import re


engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('volume', 1)


#change voice
def voice_change(v):
    x = int(v)
    engine.setProperty('voice', voices[x].id)
    speak("done sir")


#speak function for everything
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#time function to tell time and all
def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S")
    speak("The current time is")
    speak(Time)


#date function for current date
def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(date)
    speak(month)
    speak(year)


def checktime(tt):
    hour = datetime.datetime.now().hour
    if ("morning" in tt):
        if (hour >= 6 and hour < 12):
            speak("Good morning sir")
        else:
            if (hour >= 12 and hour < 18):
                speak("it's Good afternoon sir")
            elif (hour >= 18 and hour < 24):
                speak("it's Good Evening sir")
            else:
                speak("it's Goodnight sir")
    elif ("afternoon" in tt):
        if (hour >= 12 and hour < 18):
            speak("it's Good afternoon sir")
        else:
            if (hour >= 6 and hour < 12):
                speak("Good morning sir")
            elif (hour >= 18 and hour < 24):
                speak("it's Good Evening sir")
            else:
                speak("it's Goodnight sir")
    else:
        speak("it's night sir!")

#welcome function
def wishme():
    speak("Welcome Back")
    hour = datetime.datetime.now().hour
    if (hour >= 6 and hour < 12):
        speak("Good Morning sir!")
    elif (hour >= 12 and hour < 18):
        speak("Good afternoon sir")
    elif (hour >= 18 and hour < 24):
        speak("Good Evening sir")
    else:
        speak("Goodnight sir")

    speak("jarvis at your service, Please tell me how can i help you?")


def wishme_end():
    speak("signing off")
    hour = datetime.datetime.now().hour
    if (hour >= 6 and hour < 12):
        speak("Good Morning")
    elif (hour >= 12 and hour < 18):
        speak("Good afternoon")
    elif (hour >= 18 and hour < 24):
        speak("Good Evening")
    else:
        speak("Goodnight.. Sweet dreams")
    quit()

#take command function
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        #speak(query)
        #print(query)
    except Exception as e:
        print(e)
        speak("Say that again please...")

        return "None"

    return query


#sending email function
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    email=''
    password=''
    server.login(email,password)
    server.sendmail(email, to, content)
    server.close()


#screenshot function
def screenshot():
    img = pyautogui.screenshot()
    img.save(
        "C:\\Users\\Nilabh PC\\images\\ss.png"
    )

#function for battery usage and cpu usage
def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU usage is at ' + usage)
    print('CPU usage is at ' + usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)
    print("battery is at:" + str(battery.percent))

class Coronavirus():
    def __init__(self):
        self.driver = webdriver.Chrome("C:\\Users\\Nilabh PC\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe")

    def get_data(self):
        #try:
        self.driver.get('https://www.worldometers.info/coronavirus/')
        table = self.driver.find_element_by_xpath('//*[@id="main_table_countries_today"]/tbody[1]')
        country_element = table.find_element_by_xpath("//td[contains(., 'India')]")
        row = country_element.find_element_by_xpath("./..")
        data = row.text.split(" ")
        total_cases = data[1]
        new_cases = data[2]
        total_deaths = data[3]
        new_deaths = data[4]
        active_cases = data[5]
        total_recovered = data[6]
        serious_critical = data[7]

        #total_cases = row.find_element_by_class_name('sorting_1')
        #new_cases = row.find_element_by_xpath("//td[3]")
        #total_deaths = row.find_element_by_xpath("//td[4]")
        #new_deaths = row.find_element_by_xpath("//td[5]")
        #active_cases = row.find_element_by_xpath("//td[6]")
        #total_recovered = row.find_element_by_xpath("//td[7]")
        #serious_critical = row.find_element_by_xpath("//td[8]")
        print("Country: " + country_element.text)
        print("Total cases: " + total_cases)
        print("New cases: " + new_cases)
        print("Total deaths: " + total_deaths)
        print("New deaths: " + new_deaths)
        print("Active cases: " + active_cases)
        print("Total recovered: " + total_recovered)
        print("Serious, critical cases: " + serious_critical)

        send_mail(country_element.text, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical)

        self.driver.close()
        #except:
        self.driver.quit()

def send_mail(country_element, total_cases, new_cases, total_deaths, new_deaths, active_cases, total_recovered, serious_critical):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    email = ''
    password = ''

    server.login(email, password)

    subject = 'Coronavirus stats in your country today!'

    body = 'Today in ' + country_element + '\
        \nThere is new data on coronavirus:\
        \nTotal cases: ' + total_cases +'\
        \nNew cases: ' + new_cases + '\
        \nTotal deaths: ' + total_deaths + '\
        \nNew deaths: ' + new_deaths + '\
        \nActive cases: ' + active_cases + '\
        \nTotal recovered: ' + total_recovered + '\
        \nSerious, critical cases: ' + serious_critical  + '\
        \nCheck the link: https://www.worldometers.info/coronavirus/'

    msg = f"Subject: {subject}\n\n{body}"
    to = ''

    server.sendmail(email,to,msg)
    print('Hey Email has been sent!')

    server.quit()


#function for jokes
def jokes():
    j = pyjokes.get_joke()
    print(j)
    speak(j)


#weather condition
def weather():
    api_key = "" 
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    speak("tell me which city")
    city_name = takeCommand()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]
        r = ("in " + city_name + " Temperature is " +
             str(int(current_temperature - 273.15)) + " degree celsius " +
             ", atmospheric pressure " + str(current_pressure) + " hpa unit" +
             ", humidity is " + str(current_humidiy) + " percent"
             " and " + str(weather_description))
        print(r)
        speak(r)
    else:
        speak(" City Not Found ")


def personal():
    speak(
        "I am Jarvis, version 1.0, I am an AI assistent, I am developed by Nilabh on 31 July 2021 in INDIA"
    )
    speak("Now i hope you know me")


if __name__ == "__main__":
    wishme()
    while True:
        query = takeCommand().lower()
        #time
        if ('time' in query):
            time()

        elif ('date' in query):
            date()

        elif ("tell me about yourself" in query):
            personal()
        elif ("about you" in query):
            personal()
        elif ("who are you" in query):
            personal()
        elif ("yourself" in query):
            personal()

        elif ("developer" in query or "tell me about your developer" in query
              or "father" in query or "who develop you" in query
              or "developer" in query or "God" in query or "Your god" in query):
            res = open("about.txt", 'r')
            speak("here is the details: " + res.read())

#searching on wikipedia

        elif ('wikipedia' in query or 'what' in query or 'who' in query
              or 'when' in query or 'where' in query):
            speak("searching...")
            query = query.replace("wikipedia", "")
            query = query.replace("search", "")
            query = query.replace("what", "")
            query = query.replace("when", "")
            query = query.replace("where", "")
            query = query.replace("who", "")
            query = query.replace("is", "")
            result = wikipedia.summary(query, sentences=2)
            print(query)
            print(result)
            speak(result)

# Corona Report with email facility

        elif ("Corona" in query or "corona report" in query or
        "covid 19" in query or "covid 19 report" in query
        or "india corona cases" in query or "report" in query):
            bot= Coronavirus()
            bot.get_data()

#sending email

        elif ("send email" in query):
            try:
                speak("What is the message for the email")
                content = takeCommand()
                to = 'sahunilabh@gmail.com'
                sendEmail(to, content)
                speak("Email has sent")
            except Exception as e:
                print(e)
                speak(
                    "Unable to send email check the address of the recipient")
        elif ("search on google" in query or "open website" in query):
            speak("What should i search or open?")
            chromepath = "C:\\Users\\Nilabh PC\\Downloads\\chromedriver_win32 (1)\\chromedriver.exe"
            search = takeCommand().lower()
            wb.get(chromepath).open_new_tab(search + '.com')

#sysytem logout/ shut down etc

        elif ("logout" in query):
            os.system("shutdown -1")
        elif ("restart" in query):
            os.system("shutdown /r /t 1")
        elif ("shut down" in query):
            os.system("shutdown /r /t 1")

#play songs

        elif ("play songs" in query):
            speak("Playing...")
            songs_dir = "C:\\Music"
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir, songs[1]))
            quit()

#reminder function

        elif ("create a reminder list" in query or "reminder" in query):
            speak("What is the reminder?")
            data = takeCommand()
            speak("You said to remember that" + data)
            reminder_file = open("data.txt", 'a')
            reminder_file.write('\n')
            reminder_file.write(data)
            reminder_file.close()

#reading reminder list

        elif ("do you know anything" in query or "remember" in query):
            reminder_file = open("data.txt", 'r')
            speak("You said me to remember that: " + reminder_file.read())

#screenshot
        elif ("screenshot" in query):
            screenshot()
            speak("Done!")

#cpu and battery usage
        elif ("cpu and battery" in query or "battery" in query
              or "cpu" in query):
            cpu()

#jokes
        elif ("tell me a joke" in query or "joke" in query or "jokes" in query):
            jokes()

#weather
        elif ("weather" in query or "temperature" in query):
            weather()

#jarvis features
        elif ("tell me your powers" in query or "help" in query
              or "features" in query):
            features = ''' i can help to do lot many things like..
            i can tell you the current time and date,
            i can tell you the current weather,
            i can tell you battery and cpu usage,
            i can create the reminder list,
            i can take screenshots,
            i can send email to your boss or family or your friend,
            i can shut down or logout or hibernate your system,
            i can tell you non funny jokes,
            i can open any website,
            i can search the thing on wikipedia,
            i can change my voice from male to female and vice-versa
            And yes one more thing, My boss is working on this system to add more features...,
            tell me what can i do for you??
            '''
            print(features)
            speak(features)

        elif ("hii" in query or "hello" in query or "goodmorning" in query
              or "goodafternoon" in query or "goodnight" in query
              or "morning" in query or "noon" in query or "night" in query):
            query = query.replace("jarvis", "")
            query = query.replace("hi", "")
            query = query.replace("hello", "")
            if ("morning" in query or "night" in query or "goodnight" in query
                    or "afternoon" in query or "noon" in query):
                checktime(query)
            else:
                speak("what can i do for you")

#changing voice
        elif ("voice" in query):
            speak("for female say female and, for male say male")
            q = takeCommand()
            if ("female" in q):
                voice_change(1)
            elif ("male" in q):
                voice_change(0)
        elif ("male" in query or "female" in query):
            if ("female" in query):
                voice_change(1)
            elif ("male" in query):
                voice_change(0)

#exit function

        elif ('i am done' in query or 'bye bye jarvis' in query
              or 'go offline jarvis' in query or 'bye' in query
              or 'nothing' in query):
            wishme_end()
