#import modules
#write def functions
#write mainfunc and give commands
# proccess-
# greating
# kanna's job-listening->then write on screen
# user job- speak (give command)
# commands-
# open chrome
# open pycharm
# open youtube
# open inbox
# open wikipedia
# open google colab
# play music
# ask time
# reminder(water, any form ,tickets booking, food)
# quit kanna

import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser
import wikipedia
import time
import os
import smtplib,ssl

#initialisation
engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
recognizer=sr.Recognizer()
microphone=sr.Microphone()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#greetings
def wishme():
    hr=int(datetime.datetime.now().hour)
    if hr>=0 and hr<12:
        speak("Good Morning! Poonam")
    elif hr>=12 and hr<18:
        speak("Good Afternoon! Poonam")
    else:
        speak("Good evening! Pooja")
    speak("I am Kanna..How may I help you")

def recognition_from_mic(recognizer,microphone):
    """Transcribe speech from recorded from `microphone`.

        Returns a dictionary with three keys:
        "success": a boolean indicating whether or not the API request was
                   successful
        "error":   `None` if no error occured, otherwise a string containing
                   an error message if the API could not be reached or
                   speech was unrecognizable
        "transcription": `None` if speech could not be transcribed,
                   otherwise a string containing the transcribed text
        """
    #check that recognizer and microphone argument are appropriate type
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError('recognizer must be Recognizer instance')

    if not isinstance(microphone,sr.Microphone):
        raise TypeError('microphone must be Microphone instance')

    #adjust the recognizer noise sensitivity to ambient and record audio
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("listening...")
        audio=recognizer.listen(source)

    #set up response object
    response={
        "success":True,
        "error":None,
        "transcription":None
    }
    #updating the response after listening
    try:
        response["transcription"]=recognizer.recognize_google(audio)
        print("recognizing...")
    except sr.RequestError:
        response["success"]=False
        response["error"]="API unavailable"
    except sr.UnknownValueError:
        response["error"] = "unable to recognize speech"

    return response

def sendemail(to,content):
    port=465
    speak("type your password")
    password=input("type your password")
    context=ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com",port,context=context) as server:
        server.login("poonamprajapat4689@gmail.com",password)
    server.sendmail("poonamprajapat4689@gmail.com",to,content)

if __name__=="__main__":
    wishme()
    while True:
        while True:
            command = recognition_from_mic(recognizer, microphone)
            if command["transcription"]:
                break
            if not command["success"]:
                break
            print("audio didn't catched. Please say it again")
        print(command["transcription"])
        query = command["transcription"].lower()
        # execution of tasks
        if "open google" in query:
            webbrowser.open("C:\Program Files\Google\Chrome\Application\chrome.exe")

        elif "open pycharm" in query:
            webbrowser.open("C:\Program Files\JetBrains\PyCharm Community Edition 2022.3.3\bin\pycharm64.exe")

        elif "open youtube" in query:
            webbrowser.open("https://youtube.com/")

        elif "send email" in query:
            try:
                speak("what should I write in email")
                content = recognition_from_mic(recognizer, microphone)
                to = "poonamp.cogni@gmail.com"
                sendemail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("sorry! your email couldn't be send")


        elif "wikipedia" in query:
            result = wikipedia.summary(query.replace('wikipedia', ""), sentences=4)
            print(result)
            speak("according to wikipedia")
            speak(result)

        elif "meaning" in query:
            result = wikipedia.search(query.replace('what is', ""))
            print(result)
            speak(result)

        elif "google notebook" in query:
            webbrowser.open("https://colab.research.google.com/?utm_source=scs-index")

        elif "play music" in query:
            webbrowser.open("https://music.youtube.com/watch?v=NXEIW4e3sOc&feature=share")

        elif "time" in query:
            print(time.ctime())
            current_time = time.strftime("%H:%M:%S")
            speak(f"the current time is {current_time}")

        # elif "remind" in query:

        elif "shut up" in query:
            print("okay bye")
            break





