import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes
import psutil
import time
from plyer import notification
import webbrowser

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # [Male, Female]
battery = psutil.sensors_battery()


def wait():
    time.sleep(2)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def wish_me():
    print("~~~~~~~~~~~~~~~~WELCOME~~~~~~~~~~~~~~~")
    current_time_hour = datetime.datetime.now().time().hour
    wait()
    talk("hi...")
    if 0 < current_time_hour < 12:
        print("Good Morning!")
        talk("Good Morning!")
    elif 12 <= current_time_hour < 19:
        print("Good Evening!")
        talk("Good Evening!")
    else:
        print("Good Afternoon!")
        talk("Good afternoon!")

    talk("I'm Alfred, your virtual assistant")
    talk("What can i do for you?")
    # print("What can i do for you?")


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.dynamic_energy_threshold = False
            listener.energy_threshold = 350
            listener.pause_threshold = 2
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "alfred" in command:
                command = command.replace("alfred", "")
                # print(command)
    except Exception as e:
        print("An error has occurred: ", e)
        wait()
        print("Try again later...")
        exit()
        pass

    return command


def status():
    battery_level = battery.percent
    pc_plugged = battery.power_plugged

    if battery_level <= 50:
        talk("Not so good, I have low battery...")
        if not pc_plugged:
            talk("I recommend that you connect your device to power. It is running low... ")
        else:
            talk("But I'm powering up so I will be okay...")
    else:
        talk("Very good...")
        talk("I'm running with " + str(battery_level) + "percent of power.")

    print("Battery level: ", battery_level)

    if pc_plugged and battery_level != 100:
        talk("I will inform you if I'm fully charged, during my time active")


def battery_alarm():
    if battery.percent == 100:
        notification.notify(title="Alfred: ", message="Battery fully charged...", timeout=10)


def play(command):
    if "in youtube" in command or "on youtube" in command:
        command = command.replace("in youtube" or "on youtube", "")
    yt_video = command.replace("play", "")
    print("Playing" + yt_video + " on YouTube.")
    talk("Playing" + yt_video + " on YouTube.")
    pywhatkit.playonyt(yt_video)


def get_time():
    t = datetime.datetime.now().strftime("%I:%M %p")
    print(t)
    talk("The current time is" + t)


def search(command):
    wiki_search = command.replace("wikipedia" or "get info about", '')
    info = wikipedia.summary(wiki_search, 1)
    print(info)
    talk(info)


def joke():
    j = pyjokes.get_joke()
    print(j)
    talk(j)


# def send_message():
#     message = ""
#     phone = 0
#     print("For whom?")
#     talk("for whom is the message?")
#     person = take_command()
#     print(person)
#
#     if "brother" in person:
#         phone = +19393981525
#         talk("what will be the message to your brother?")
#         print("Message?")
#         message = take_command()
#         print(message)
#
#     elif "sofia" in person or "sophia" in person or "wife" in person or "my sexy tomato" in person:
#         phone = +17876673588
#         talk("what will be the message to sofia?")
#         print("Message?")
#         message = take_command()
#         print(message)
#
#     elif "me" in person:
#         phone = +17872380795
#         talk("what will be the message to yourself?")
#         print("Message?")
#         message = take_command()
#         print(message)
#
#     print("Sending message to " + person)
#     talk("sending message to " + person)
#
#     h = datetime.datetime.now().time().hour
#     m = datetime.datetime.now().time().minute + 2
#     pywhatkit.sendwhatmsg(str(phone), message, time_hour=h, time_min=m)
#
#     print("Message sent. It will arrive at " + str(h) + ":" + str(m) + "...")
#     talk("Message sent. It will arrive at " + str(h) + ":" + str(m) + "...")


def power_off(command):
    if "goodbye" in command:
        talk("Goodbye... until next time")
    elif "that's all" in command:
        talk("Okay...")
    print("~~~~~~~~~~~~~~~~~Powering off~~~~~~~~~~~~~~~")
    exit()


def open_web(web_page):
    web_page = web_page.replace("open ", "")
    if "whatsapp" == web_page:
        webbrowser.open("web.whatsapp.com")
    webbrowser.open(f"www.{web_page}.com")


def run():
    command = take_command()

    print(command)

    if "how are you" in command or "your status" in command:
        if "how are you" in command:
            status()
            talk("what can i do for you?")
            print("What can I do for you?")
            run()
        else:
            status()
        wait()

    if "play" in command:
        play(command)
        wait()

    elif "time" in command:
        get_time()
        wait()

    elif "wikipedia" in command or "get information about" in command:
        search(command)
        wait()

    elif "joke" in command:
        joke()
        wait()

    # elif "send message" in command:
    #     send_message()
    #     wait()

    elif "power off" in command or "goodbye" in command:
        power_off(command)

    elif "open" in command:
        open_web(command)

    elif "wait" in command:
        time.sleep(30)
        pass

    else:
        talk("Didn't get that. Can you say it again please?...")
        run()


wish_me()
wait()
while True:
    run()
    battery_alarm()
    talk("anything else?")
