#Description: This is a virtual assistant program that gets the date, the current time, 
#responds back with a random greeting, and returns information on a person from wikipedia

import speech_recognition as sr     
from gtts import gTTS
import os
import datetime
import warnings
import calendar
import random
import wikipedia


#Record audio and return it as string
def record_audio():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something:")
        audio = r.listen(source)

    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: "+data)
    except sr.UnknownValueError:
        print("Our speech recognition API couldn't understand the audio")
    except sr.RequestError:
        print("Request errors, please check your internet connection")

    return data


#A function to get the virtual assistant response
def assistantResponse(text):
    print(text)

    #Convert text to speech
    #en-us:US Accent,en-gb:British,en-au:Australian,en-in:Indian
    myObj = gTTS(text=text,lang='en-us',slow=False)

    #Save the converted audio to a file
    myObj.save('assistant_response.mp3')

    #Play the converted file
    os.system('start assistant_response.mp3')


#A function for wake words or phrase
def wakeWord(text):
    WAKE_WORDS = ["hey computer","ok computer","hey assistant"]

    text = text.lower()

    #Check to see if the users command/text contains a wake word
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True
    
    #If there is no wake word in the text
    return False


#Function to get current date
def getDate():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()] #e.g. Sunday
    monthNum = now.month
    dayNum = now.day

    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September','October', 'November', 'December']
    ordinalNumbers = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th','13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd','24th', '25th', '26th', '27th', '28th', '29th', '30th', '31st']
    
    return "Today is "+weekday+" "+month_names[monthNum - 1]+" the "+ordinalNumbers[dayNum-1]+"."


#A function to create random greeting response
def greeting(text):
    #Greeting inputs
    GREETING_INPUTS=['hi','hey','hello','greetings','namaste','ok']

    #Greeting responses
    GREETING_RESPONSES=['hi there','hello there','namaste','greetings']

    #If the users input is a greeting, then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) + "."


#A function to get a persons first and last name from the text
def getPerson(text):
    wordList = text.split()
    for i in range(0,len(wordList)):
        if i+3<=len(wordList)-1 and wordList[i].lower()=='who' and wordList[i+1].lower()=='is':
            return wordList[i+2] + " " + wordList[i+3]


#A function to create bye
def farewell(text):
    #Greeting inputs
    FAREWELL_INPUTS=['bye','goodbye','farewell']

    #Greeting responses
    FAREWELL_RESPONSES=['farewell']

    #If the users input is a farewell, then return a farewell response
    for word in text.split():
        if word.lower() in FAREWELL_INPUTS:
            return random.choice(FAREWELL_RESPONSES) + "."



while True:
    #Record audio
    text = record_audio()
    response = ""

    #Check for wake word
    if(wakeWord(text) == True):
        response = response + greeting(text)
        
        #Check if user asks date
        if('date' in text):
            get_date = getDate()
            response = response + " " + getDate()

        #Check if user asks who is
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person,sentences=2)
            response = response + " " + wiki

        #Have assistant speak to you
        assistantResponse(response)

    if('bye' in text):
        response = response + farewell(text)
        assistantResponse(response)
        break