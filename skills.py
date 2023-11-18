import os, webbrowser, sys, requests, pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speaker(text):
    engine.say(text)
    engine.runAndWait()

def browser():
    webbrowser.open('https://www.youtube.com/', new = 2)


def offpc():
    os.system('shutdown /s')



def offBot():
    sys.exit()