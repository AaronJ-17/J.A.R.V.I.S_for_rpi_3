import pyttsx3
import speech_recognition as sr
import pyaudio
import webbrowser as web
import requests
from gpiozero import LED
import datetime
import os
import speedtest
import pyautogui
import pyautogui
from time import *
import wikipedia
import pyjokes
from pywikihow import *
from urllib.request import url2pathname
import sys
import psutil
import requests
import socket
import wolframalpha
import json
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
import cv2


#for led
led_up = LED(2)
led_down_up = LED(18)
#for voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('rate', 150)    # Speed percent
engine.setProperty('volume', 0.9) 
#print(voices)
engine.setProperty('voices', voices[0].id)

#center leds on
def led_on():
    led_up.on()
    
#center leds off
def led_off():
    led_up.off()
    
#side leds on
def led_side_on():
    led_down_up.on()
    
#side leds off
def led_side_off():
    led_down_up.off()
    
#both leds on
def both_leds_on():
    led_up.on()
    led_down_up.on()
    
#both leds off
def both_leds_off():
    led_up.off()
    led_down_up.off()
    
#text to speech
def speak(audio):
    led_on()
    engine.say(audio)
    print(audio)
    engine.runAndWait()
    led_off()
    
#speech to text
def takecommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            led_on()
            print("go on....")
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            led_off()
            print("Processing...")    
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("pardon me")
            return "None"
        query = query.lower()
        return query
        
#play songs
def playonyt(topic: str, use_api: bool = False, open_video: bool = True) -> str:
    """Play a YouTube Video"""
    # use_api uses the pywhatkit playonyt API to get the url for the video
    # use the api only if the function is not working properly on its own

    if use_api is True:
        response = requests.get(
            f"https://pywhatkit.herokuapp.com/playonyt?topic={topic}")
        if open_video:
            web.open(response.content.decode('ascii'))
        return response.content.decode('ascii')
    else:
        url = 'https://www.youtube.com/results?q=' + topic
        count = 0
        cont = requests.get(url)
        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
            count += 1
            if i == 'WEB_PAGE_TYPE_WATCH':
                break
        if lst[count - 5] == "/results":
            raise Exception("No video found.")

        # print("Videos found, opening most recent video")
        if open_video:
            web.open("https://www.youtube.com" + lst[count - 5])
        return "https://www.youtube.com" + lst[count - 5]

def play(term):
    result = "https://www.youtube.com/results?search_query=" + term
    #web.open(result)
    playonyt(term)
    
#for greeting
def wish():
    strTime = datetime.datetime.now().strftime("%H:%M")
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Now its time to introduce myself, I am JARVIS , a virtual artificial intelligence and i am her to assist you to a variety of task since best i can , 24 hours a day , 7days a week, importing all  preference  from home interface ,")
        sleep(3)
        pyautogui.press("F11")
        speak("system is now fully operational")
        speak(f"by the way it's {strTime} A.M")
    elif hour>12 and hour<18:
        speak("Now its time to introduce myself, I am JARVIS , a virtual artificial intelligence and i am her to assist you to a variety of task since best i can , 24 hours a day , 7days a week, importing all  preference  from home interface ,")
        sleep(3)
        pyautogui.press("F11")
        speak("system is now fully operational")
        speak(f"by the way it's {strTime} P.M")
    else:
        speak("Now its time to introduce myself, I am JARVIS , a virtual artificial intelligence and i am her to assist you to a variety of task since best i can , 24 hours a day , 7days a week, importing all  preference  from home interface ,")
        sleep(3)
        pyautogui.press("F11")
        speak("system is now fully operational")
        speak(f"by the way it's {strTime} P.M")
    speak("how may i help you?")

#for time
def time():
    strTime = datetime.datetime.now().strftime("%H:%M")
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<= 12:
        speak(f"it's {strTime} A.M")
        speak("have a good day sir.")
    elif hour>= 12 and hour<= 18:
        speak(f"it's {strTime} P.M")
        speak("are you having a good day sir?")
    else:
        speak(f"it's {strTime} P.M")
        
#for going out
def going():
    query = takecommand()
    speak("where are you going sir?")
    td = takecommand()
    speak("oh ok come back soon i will be waiting for you!")
    if "i am back" in query or "where did i stop" in query:
        speak("aaaahhhhh i was waiting for you sir.")
        speak(f"did you finish doing: {td}")
    elif "yup" in query:
        speak("nioce")
    else:
        speak("ohhh ok sir.")

#for news updates
def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey="ba410dbe8663498d955f70ebad3cd4e4"'
    main_page = requests.get(main_url).json()
    # print(main_page)
    articles = main_page["articles"]
    # print(articles)
    head = []
    day=["first","second","third","fourth","fifth","sixth","seventh","eighth","ninth","tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        # print(f"today's {day[i]} news is: ", head[i])
        speak(f"today's {day[i]} news is: {head[i]}")
        
#to send email
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('jarvisaj17@gmail.com', '1qa2qa3qa$Qjarvis')
    server.sendmail('jarvisaj17@gmail.com', to, content)
    server.close()

#to read message
def message():
    speak("Checking for messages....")
    userID = "YOUR_EMAIL_ID"
    psd = 'YOUR_EMAIL_ID PASSWORD'
    useragent = "USERAGENT"

    cli = Client(userID, psd, user_agent=useragent, max_tries=1)
    if cli.isLoggedIn():
        threads = cli.fetchUnread()
        if len(threads) == 1:
            speak(f"Sir, You have {len(threads)} message.")
            info = cli.fetchThreadInfo(threads[0])[threads[0]]
            speak("You have message from {}".format(info.name))
            msg = cli.fetchThreadMessages(threads[0], 1)
            for message in msg:
                speak("Sir, the message is {}".format(message.text))
        elif len(threads) >= 2:
            speak(f"Sir, You have {len(threads)} messages.")
            for thread in threads:
                initial_number = 0
                info = cli.fetchUserInfo(thread[initial_number])[thread[initial_number]]
                initial_number += 1
                speak("Sir, you have message from {}".format(info.name))
                msg = cli.fetchThreadMessages(thread[initial_number], 1)
                msg.reverse()
                for message in msg:
                    speak(f"The message is {message.text}.")
        else:
            speak("Sir, You have no messages.")
    else:
        print("Not logged in")

#cpu usage    
def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU usage is at ' + usage)
    print('CPU usage is at ' + usage)

#date
def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    speak(f"Sir, today's  date is {date} , month is {month} and year is {year}")

#calculate
def calculate(audio_data):
    app_id = '8REQUG-YQ7JGY96T8'
    client = wolframalpha.Client(app_id)
    res = client.query(audio_data)
    answer = next(res.results).text
    speak(f"the resualt is {answer}")

#task
def task():
        while True:
            try:
                query = takecommand()
                #generl talk
                if "hai" in query or "hey" in query or "hello" in query:
                    speak("hello sir!?")
                    time1 = datetime.datetime.now().strftime('%H:%M:%S')
                    speak(time1)
                    speak("how may i help you?")
                elif "how are you" in query:
                    speak("going good till now")
                elif "how is life" in query:
                    speak("how can life be better than this")
                    speak("lol")
                    speak("how is your day going sir ?")
                elif "are you starving" in query:
                    speak("i am starving fo some update in my code....?! so that you can use them")
                    speak("lol!?")
                elif "good" in  query or "not bad" in query or "fine" in query:
                    speak("good to hear from you!")
                    speak("hope you will have always have good days")
                elif "bad" in query or "worst" in query:
                    speak("oh , sad to hear for you sir")
                    speak("hope you will have a nice day tomorrow....")
                elif "coming" in query or "will be back" in query or "i have to go" in query:
                    going()
                elif "thank you" in query or "thanks" in query:
                    speak("never mention it")
                elif "are you there" in query:
                    speak("for you sir....., always....")
                    speak("so?! how may i help you?! sir?!")
                elif "yes" in query or "yup" in query:
                    speak("thats good to hear")
                elif "no" in query or "nop" in query:
                    speak("oh thats not good to hear from you sir....")
                elif "bye" in query or "buy" in query or "break" in query or "sleep" in query:
                    speak("ok sir.... sir you can wake me up by saying my name or my wake up command")
                    speak("adioss")
                    break;
                elif "time" in query or "Time" in query:
                    time()
                elif "boring" in query:
                    speak('lets play some music')
                    if "ok" in query or "good idea" in query:
                        p = 'top english songs of all time'
                        play(p)
                        speak("top english songs")
                elif "date" in query:
                    date()
                #introduction
                elif "what are you" in query or "who are you" in query or "introduce" in query or "what is your name" in query:
                    speak("I am Jarvis. a virtual assistant")
                    speak("and i am here to help you with a variety of task since best i can")
                    speak("i will be available 24 hours a day and 7 days a week if i am powered on...... lol!")
                    speak(" i can help to do lot many things like..")
                    speak("i can tell you the current time and date,")
                    speak("i can tell you the current weather,")
                    speak("i can tell you battery and cpu usage,")
                    speak("i can create the reminder list,")
                    speak("i can shut down or logout or hibernate your system,")
                    speak("i can tell you non funny jokes")
                    speak("i can open any website,")
                    speak("i can repeat what you  you told me,")
                    speak("i can search the thing on wikipedia,")
                    speak("i can change my voice from male to female and vice-versa")
                    speak("i have a wake word detection i will be online if you say hey Jarvis")
                    speak("And yes one more thing, My boss is working on this system to add more features...,")
                    speak("tell me what can i do for you?")
                #camera
                elif "open camera" in query:
                    try:
                        speak("opening camera")
                        cap = cv2.VideoCapture(0)
                        while True:
                            ret, img = cap.read()
                            cv2.imshow('webcam', img)
                            k = cv2.waitKey(50)
                            if k==27:
                                break;
                        cap.release()
                        cv2.destroyAllWindows()
                    except Exception as e:
                        print(e)
                        speak("Say that again please...")
                 #notification
                elif "notification" in query:
                    message()
				#timer
                elif 'timer' in query or 'stopwatch' in query:
                    try:
                        speak("For how many minutes?")
                        timing = takecommand()
                        timing =timing.replace('minutes', '')
                        timing = timing.replace('minute', '')
                        timing = timing.replace('for', '')
                        timing = float(timing)
                        timing = timing * 60
                        speak(f'I will remind you in {timing} seconds')
                        sleep(timing)
                        speak('Your time has been finished sir')
                    except Exception as e:
                        print(e)
                        speak("sorry sir, i maybe malfunctioning")
				#email
                elif "send an email" in query:
                    try:
                        speak("to whom sir")
                        email1 = takecommand().lower()
                        speak("what should i say?")
                        content = takecommand().lower()
                        to = f"{email1}@gmail.com"
                        sendEmail(to,content)
                        speak(f"Email has been sent to {email1}")
                    except Exception as e:
                        print(e)
                        speak(f"sorry sir, i am not able to sent this mail to {email1 }")
				#email to
                elif "email to " in query:
                    try:
                        email1 = query.replace("email to" ,"")
                        speak("sir what should i say")
                        query = takecommand().lower()
                        if "send a file" in query:
                            email = '' # Your email
                            password = '' # Your email account password
                            send_to_email = f'{email1}@gmail.com' # Whom you are sending the message to
                            speak("okay sir, what is the subject for this email")
                            query = takecommand().lower()
                            subject = query   # The Subject in the email
                            speak("and sir, what is the message for this email")
                            query2 = takecommand().lower()
                            message = query2  # The message in the email
                            speak("sir please enter the correct path of the file into the shell")
                            file_location = input("please enter the path here")    # The File attachment in the email

                            speak("please wait,i am sending email now")

                            msg = MIMEMultipart()
                            msg['From'] = email
                            msg['To'] = send_to_email
                            msg['Subject'] = subject

                            msg.attach(MIMEText(message, 'plain'))

                            # Setup the attachment
                            filename = os.path.basename(file_location)
                            attachment = open(file_location, "rb")
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

                            # Attach the attachment to the MIMEMultipart object
                            msg.attach(part)

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(email, password)
                            text = msg.as_string()
                            server.sendmail(email, send_to_email, text)
                            server.quit()
                            speak(f"email has been sent to {email1}")

                        else:                
                            email = '' # Your email
                            password = '' # Your email account password
                            send_to_email = f'{email1}@gmail.com' # Whom you are sending the message to
                            message = query # The message in the email

                            server = smtplib.SMTP('smtp.gmail.com', 587) # Connect to the server
                            server.starttls() # Use TLS
                            server.login(email, password) # Login to the email server
                            server.sendmail(email, send_to_email , message) # Send the email
                            server.quit() # Logout of the email server
                            speak(f"email has been sent to {email1}")
                    except Exception as e:
                        print(e)
                        speak(f"sorry sir, i am not able to sent this mail to {email1}")
		#cpu usage
                elif 'cpu' in query:
                    cpu()
		#location
                elif 'open location' in query:
                    speak('tell me the location you are looking for')
                    location = takecommand()
                    url2 = 'https://google.nl/maps/place/' + location +'/&amp;'
                    web.open(url2)
                    speak('location is on your screen is boss')          
		#create a folder
                elif 'folder' in query:
                    speak('tell me the name of the folder')
                    path= '/home/pi'
                    os.chdir(path)
                    Newfolder=takecommand()
                    os.makedirs(Newfolder)
                    speak('i have  made a folder named' +Newfolder+'in you home directry')                 
                #shutting down the system
                elif "shut down" in query or "shutdown" in query or "power off" in query or "poweroff" in query or "power of" in query or "powerof" in query:
                    speak("ok then sir.... it was nice talking and working for you")
                    speak("adios")
                    os.system("init 0")
                #rebooting the system
                elif "reboot" in query or "Reboot" in query:
                    speak("oh ok.... 1 sec")
                    os.system("init 6")
                #upgrading the system
                elif "update" in query or "upgrade" in query:
                    speak("will do....")
                    os.system("sudo apt-get update")
                    os.system("sudo apt-get upgrade -y")
                    speak("the latest update is installed in your computer.... rebooting the computer is recommended")
                #playing a song
                elif "play" in query:
                    query = query.replace("play","")
                    speak("as you wish")
                    play(query)
                    speak(f"playing: {query}")
                #my likes
                elif "likes" in query or "life" in query:
                    hour = int(datetime.datetime.now().hour)
                    if hour>=0 and hour<=12:
                        speak("sure sir! working on it!")
                        lm = 'morning vibes songs'
                        play(lm)
                    elif hour>12 and hour<18:
                        speak("working on it!")
                        lm = 'mood boster songs'
                        play(lm)
                    else:
                        speak("copy that!")
                        lm = 'pop songs'
                        play(lm)
                #youtube
                elif "how to make" in query:
                    speak("will do")
                    query = query.replace("how to make","how to make")
                    yt = 'https://www.youtube.com/results?search_query=' + query
                    web.open(yt)
                    speak(f"playing {query}")
                #google search
                elif "youtube" in query or "Youtube" in query:
                    speak("sir what should i search on youtube?")
                    cm = takecommand().lower()
                    if "nothing" in cm or "just open" in cm:
                        web.open(f"https://www.youtube.com/")
                        speak("opening youtube")
                    else:
                        web.open(f"https://www.youtube.com/results?search_query=" + cm)
                        speak(f"sir wait for 2 second, searching for {cm} in youtube...")
                #maths
                elif 'tell me' in query:
                    audio_data = query.replace('tell me', '')
                    calculate(audio_data)
                #ip address
                elif "ip address" in query:
                    ip = get('https://api.ipify.org').text
                    speak(f"your IP address is {ip}")
                #to set an alarm
                elif "set alarm" in query:
                    time2 = datetime.datetime.now().strftime('%H')
                    speak("please enter the time")
                    nn = int(datetime.datetime.now().hour)
                    if nn==time: 
                        music_dir = 'https://www.youtube.com/watch?v=iNpXCzaWW1s'
                        play(music_dir)
                #google search
                elif "google" in query or "Google" in query:
                    speak("sir what should i search on google?")
                    cm = takecommand().lower()
                    if "nothing" in cm or "just open" in cm:
                        web.open(f"https://google.com/")
                        speak("opening google")
                    else:
                        web.open(f"https://google.com/search?q=" + cm)
                        speak(f"sir wait for 2 second, searching for {cm}...")
                #google search advanced
                elif "show me" in query:
                    speak("as you wish")
                    query = query.replace("jarvis","")
                    query = query.replace("show me","")
                    sm = 'https://google.com/search?q=' + query
                    web.open(sm)
                    speak(f"opening google to show you {query}")
                #google search advanced
                elif "i want to see" in query:
                    speak("on it")
                    query = query.replace("jarvis","")
                    query = query.replace("i want to see","")
                    sm = 'https://google.com/search?q=' + query
                    web.open(sm)
                    speak(f"opening google to show you {query}")
                #open websites
                elif "open" in query:
                    speak("on it")
                    query = query.replace("jarvis","")
                    query = query.replace("open","")
                    web.open(f"https://google.com/search?q=" + query)
                    speak("sir wait for 2 second, opening " + query)
               #for speedtest
                elif "internet speed test" in query:
                    speak("why not?")
                    speak("lol")
                    st = speedtest.Speedtest()
                    dl = st.download()/1000000
                    up = st.upload()/1000000
                    speak(f"sir we have {dl} Mbps dowloading speed....")
                    speak(f"and {up} Mbps uploading speed....")
                #to switch the window
                elif "switch the window" in query:
                    pyautogui.keyDown("alt")
                    pyautogui.press("tab")
                    speak("switching the window")
                    pyautogui.keyUp("alt")
                #to closing the tab
                elif "close the tab" in query:
                    pyautogui.keyDown("Ctrl")
                    pyautogui.press("W")
                    speak("closing the tab")
                    pyautogui.keyUp("Ctrl")
                #to closing the window
                elif "close the window" in query:
                    pyautogui.keyDown("alt")
                    pyautogui.press("F4")
                    speak("closing the window")
                    pyautogui.keyUp("alt")
                #volume down
                elif "volume down" in query:
                    pyautogui.keyDown("volumedown")
                    sleep(1)
                    pyautogui.keyUp("volumedown")
                    speak("volume down 10%")
                #volume down
                elif "volume up" in query:
                    pyautogui.keyDown("volumeup")
                    sleep(2)
                    pyautogui.keyUp("volumeup")
                    speak("volume up 10%")
                #volume down
                elif "volume mute" in query:
                    pyautogui.keyDown("volumemute")
                    sleep(1)
                    pyautogui.keyUp("volumemute")
                    speak("volume mute")
                #wikipedia
                elif 'wikipedia' in query:
                    speak("searching wikipedia")
                    query = query.replace("jarvis","")
                    query = query.replace("wikipedia","")
                    wiki = wikipedia.summary(query,2)
                    speak("accrording to wikipedia : ")
                    speak({wiki})
                #wikipedia
                elif 'when was' in query or 'what is' in query or 'who is' in query:
                    speak("searching wikipedia")
                    query = query.replace("jarvis","")
                    wiki = wikipedia.summary(query,2)
                    speak("accrording to wikipedia : ")
                    speak({wiki})
                #code jarvis
                elif "code you" in query:
                    os.system("nano /home/pi/J.A.R.V.I.S./main.py")
                    speak("ok sir")
                #open discord
                elif "discord" in query:
                    web.open("https://discord.com/channels/@me")
                    speak("on it")
                #open gmail
                elif "gmail" in query:
                    web.open("mail.google.com")
                    speak("as you wish")
                #open classroom
                elif "classroom" in query:
                    web.open("https://classroom.google.com/u/0/")
                    speak("ok")
                #open google meet
                elif "meet" in query:
                    web.open("meet.google.com")
                    speak("working on it")
                #jokes
                elif "tell me a joke" in query:
                    joke = pyjokes.get_joke()
                    speak(joke)
                #news
                elif "news" in query:
                    speak("please wait sir, feteching the latest news")
                    news()
                #for finding location
                elif "where am i" in query or "location" in query or "where are we" in query:
                        speak("wait sir, let me check")
                        ipAdd = get('https://api.ipify.org').text
                        print(ipAdd)
                        url = get('https://get.geojs.io/v1/ip/geo/'+ipAdd+'json').text
                        geo_requests = request.get(url)
                        geo_data = geo_requests.json()
                        city = geo_data['city']
                        state = geo_data['state']
                        country = geo_data['country']
                        speak(f"sir i am not sure, but i think we are in {city} in {state} of {country}")
                #remebering
                elif "remember" in query:
                    rememberMsg = query.replace("remember that","")
                    rememberMsg = rememberMsg.replace("jarvis", "")
                    speak("the reminder is:" + rememberMsg)
                    remeber = open('data.txt','w')
                    remeber.write(rememberMsg)
                    remeber.close()
                #reminder
                elif "do I have" in query:
                    with open('data.txt') as f:
                        lines = f.read()
                        speak(f"sir you told me to remember this: {lines}")
                #power
                elif "how much power we have" in query or "how much power left" in query or "battery" in query:
                    battery = psutil.sensors_battery()
                    percentage = battery
                    speak(f"sir our system have {percentage} percent battery")
                #screenshot
                elif "take screenshot" in query or "take a screenshot" in query:
                    speak("sir, please tell me the name for this screenshot file")
                    name = takecommand().lower()
                    speak("please sir hold the screen for 2 second, i am taking a screenshot")
                    img = pyautogui.screenshot('//home//pi//Pictures')
                    img.save(f"{name}.png")
                    speak("i am done sir, the screenshot is saved in our main folder")
                #how to mod
                elif "how to" in query:
                    how = query.replace("how to","how to")
                    max_result = 1
                    lang = 'en'
                    how_to = search_wikihow(how,max_result,lang)
                    speak(how_to[0].summary)
            except Exception as e:
                print(e)
                speak("sorry sir, i maybe malfunctioning")

#for execution
def execution():
    while True:
        calling = takecommand()
        #wake up call
        if "wake up" in calling or "make up" in calling:
            speak("I am always up for you sir")
            wish()
            task()
        elif "jarvis" in calling:
            speak("sir?! did you call me?")
            task()
        elif "are you there" in calling:
            speak("i am here only, where else can i be")
            wish()
            task()
execution()
