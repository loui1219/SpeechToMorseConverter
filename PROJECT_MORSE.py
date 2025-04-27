import speech_recognition as sr
import time
import RPi.GPIO as GPIO
import pyttsx3
import os

OUT_LED = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(OUT_LED, GPIO.OUT)
OUT_LED2 = 18
GPIO.setup(OUT_LED2, GPIO.OUT)
OUT_LED3 = 23
GPIO.setup(OUT_LED3, GPIO.OUT)


MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/'
}
REVERSE_MORSE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def text_to_morse(text):
    return ' '.join(MORSE_CODE_DICT.get(c.upper(), '') for c in text)

def morse_to_text(morse_code):
    words = morse_code.split(' / ')
    return ' '.join(''.join(REVERSE_MORSE_DICT.get(ch, '') for ch in word.split()) for word in words)


def play_morse_light(morse_code):
    for symbol in morse_code:
        if symbol == '.':
            print('.', end='', flush=True)
            GPIO.output(OUT_LED, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(OUT_LED, GPIO.LOW)
        elif symbol == '-':
            print('-', end='', flush=True)
            GPIO.output(OUT_LED2, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(OUT_LED2, GPIO.LOW)
        elif symbol == '/':
            print('/', end='', flush=True)
            GPIO.output(OUT_LED3, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(OUT_LED3, GPIO.LOW)
        time.sleep(0.2)
    print()


def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print("Recognized Text:", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand")
        return ""
    except sr.RequestError:
        print("Request Error")
        return ""

def read_morse_from_buttons():
    print("INPUT MORSE : \n")
    morse_code = ""
    while True:
        inp = input()
        if(inp==""):
            break
        morse_code+=inp + " "
    return morse_code.strip()

def convertSpeechToMorse():
    spoken_text = speech_to_text()
    if(spoken_text!="yes"):
        print("Recognized Text: ", spoken_text)
        print("Press CONFIRM to convert to Morse...")
        input()
        morse = text_to_morse(spoken_text)
        print("Morse Code:", morse)
        play_morse_light(morse)
    else:
        convertSpeechToMorse()

def convertMorseToText():
    morse = read_morse_from_buttons()
    print("INPUT MORSE : " + morse)
    convertedText = morse_to_text(morse)
    print("\n CONVERTED TEXT : " + convertedText)
    
try:
    while True:
        inp = input("Press 1 to Convert Text to Morse || Press 2 to Convert Morse to Text\n")
        if(inp == "1"):
            convertSpeechToMorse()  
        elif(inp == "2"):
            convertMorseToText()
        inp= input("do you want to continue?\n")
        if(inp=="no"):
            break
        

except KeyboardInterrupt:
    print("\nExiting...")
