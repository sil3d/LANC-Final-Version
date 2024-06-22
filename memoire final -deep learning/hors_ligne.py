from ast import Pass
import sys
from requests import request
from vosk import Model, KaldiRecognizer
import pyttsx3
import datetime
import locale
locale.setlocale(locale.LC_TIME,'')
import pyaudio
import json
import os
import time
import msvcrt as m
import random
import webbrowser   
import requests
time.clock = time.time
import subprocess
import ctypes
import pyautogui
from PIL import Image
import logging
from PIL import Image


logging.basicConfig(level=logging.INFO,filename="app.log",
                    filemode="a",
                    format='%(asctime)s - %(levelname)s - %(message)s - %(processName)s')



def wait():
    m.getch()
    
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
rate = engine.setProperty("rate",195)
engine.setProperty("voice", voices[4].id)
    

    



def speak(audio):
    print ("LANCE:" + str(audio)) #pour prototype 1
    engine.say(audio)
    engine.runAndWait()

#lors du démarrage l'IA va choisir quoi dire en fonction de l'heure
def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("bonjour!! ")
    elif hour >= 12 and hour < 18:
        speak("bonne aprés midi!")
    elif hour >= 18 and hour < 23:
        speak('Bonsoir à vous!!')
    else :
        speak("il se fait tard, vous devriez allez vous couché")

    speak('je suis LANCE pour vous servir!')  
    speak("je suis toujours en mode écoute")
    speak("je vous écoute")
    print("..") 

def time():
    Time = datetime.datetime.now().strftime("il est actuellement, %H:%M:%S") 
    speak(Time)
    

def date():
    date = datetime.datetime.now().strftime(" aujourdh'ui nous sommes, le %A %d %B %Y") 
    speak (date)



internetstatus = 0
url = 'http://www.google.com'
timeout=1.5
try:
    request = requests.get(url, timeout=timeout)
    internetstatus=1
except (requests.ConnectionError, requests.Timeout) as exception:
    internetstatus=2

if internetstatus == 1:
        speak("Accés internet détecté")
        speak('passage en mode en ligne')
        speak("le systéme passe automatiquement en mode en ligne si une connection internet est détectée")
        try:
            os.startfile('memoire_en_ligne.exe')
            sys.exit()
        except OSError:
            speak('désolé, aucun fichier trouver')
            speak("le programme va continuer à s'exécuter en mode hors ligne")
            speak("certaines fonctionnalités sont restraintes")
            speak("notamment, celles qui nécéssitent une connection internet")
           
            speak("chargement du modéle")
            speak("un instant je vous prie")
            model = Model("vosk-model-small-fr-0.22")
            speak("chargement du modéle terminé")
            print("...")
            print("écoute...")
        
            

if internetstatus == 2:
       
        speak('vous étes actuelement en mode hors ligne')
        speak("certaines fonctionnalités sont restraintes")
        speak("notamment, celles qui nécéssitent une connection internet")
        try:
           
            speak("chargement du modéle")
            speak("un instant je vous prie")
            model = Model("vosk-model-small-fr-0.22")
            speak("chargement du modéle terminé")
            print("...")
            print("écoute...")
        except:
            speak('Bonjour!')
            speak("désolé, aucun modéle n'a été trouvé!!")
            speak('veuillez télécharger le modéle sur le site de vosk!!')
            sys.exit()



os.system('cls')
wishme()





rec = KaldiRecognizer(model, 16000)
cap = pyaudio.PyAudio()
stream=cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()


while True:
    data = stream.read(4000, exception_on_overflow=False)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)
        print ("speaker: "+ result["text"])
        a = result["text"]
        
#........................................heure date...........................
        if "quelle heure est-il" in a or "donne moi l'heure" in a or "l'heure" in a or "quelle heure fait-il" in a or "il est quelle heure" in a or 'heure' in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            time() 
            speak("autre chose?")
            stream.start_stream()
            print("...")
            print('écoute...')

        elif'quelle est la date' in a or "date" in a or "date" in a or "quel jour sommes-nous"in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            date() 
            stream.start_stream()
            print("...")
            print('écoute...')
            
#...................................#CHAT..........................................................
        elif "comment tu vas" in a or "comment vas-tu" in a or "ça va toi" in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            a = ["merci, je vais bien","pas trop mal merci","ça peux aller","je n'ai pas vraiment d'émotions, mais ça peux aller"]
            speak(random.choice(a)) 
            stream.start_stream()
           
            print("...")
            print('écoute...')
        elif 'bonjour' in a or 'salut' in a or 'hello'in a or 'coucou' in a :
            reply_bonjour = ['bonjour bonjour!', 'hello, comment vous allez?',"bonjour à vous!", 'bonjour,comment vous allez?']
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak(random.choice(reply_bonjour)) 
           
            stream.start_stream()
            print("...")
            print('écoute...')
        elif "je t'admire" in a or "tu es tellement" in a:
            reply_aime = ["Je sais", "j'apprécie votre sentiment", "merci c'est gentil", "ohh merci beaucoup", "vous de meme"]
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak(random.choice(reply_aime))
            stream.start_stream()
           
            print("...")
            print('écoute...')
        elif "je vais bien" in a or "je vais bien " in a or "ça va" in a or 'ça peut aller' in a:
            reply = ["tant mieux", "heureux de l'entendre", "cool alors", "super, et sinon comment je peux t'aider?", "ravis de l'entendre, et sinon comment puis-je t'aider?"] 
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak(random.choice(reply))
            stream.start_stream()
           
            print("...")
            print('écoute...')
        elif "je ne vais pas bien" in a  or "bof" in a or "ça ne va pas bien" in a :
            reply = ["pourquoi?", "désolé pour vous",] 
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak(random.choice(reply))
            speak("je vous suggére d'allez prendre un peu d'air")
            stream.start_stream()
           
            print("...")
            print('écoute...')
        
        


        elif "comment tu t'appelles" in a or "qui es-tu" in a or "qui" in a or "²tu es" in a or "tu es qui" in a :
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak("je m'appelles LANCE")
            speak("Concraitement je suis une IA je simule l'intelligence humaine")
            speak("mais je ne suis pas autonome")
            speak("mon role: assistant")
            stream.start_stream()
           
            print("...")
            print('écoute...')
        elif "lanc" in a or "lance" in a or "debout" in a or "tu es là" in a or "tu es la" in a :
            os.system('cls')
            reply = ["toujours présent","oui, je suis là!!","hum hum","oui"]
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak(random.choice(reply))
            speak("en quoi puis-je vous être  utile?")
            stream.start_stream()
           
            print("...")
            print('écoute...')
        elif "Bonsoir lanc" in a or "Bonsoir lance" in a or "bonsoir" in a :
            os.system('cls')
            reply = ["Bonsoir!,j'éspère que vous avez passé une bonne journée!", "Bonsoir !, comment avez-vous passé la journée? j'éspère que vous n'étes pas trop fatiqué"]
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak(random.choice(reply))
            stream.start_stream()
           
            print("...")
            print('écoute...')
#.....................NEW..............////

        elif "c'est quoi une ia" in a or "es-tu une ia" in a or "c'est quoi une intelligence artificielle" in a or "es-tu une intelligence artificielle" in a or "intelligence artificielle" in a or "IA" in a:
            os.system('cls')
            stream.stop_stream()
            reply = ["Une IA, consiste à mettre en œuvre un certain nombre de techniques visant à permettre aux machines d'imiter une forme d'intelligence réelle", "L'intelligence artificielle, est un « ensemble de théories et de techniques mises en œuvre en vue de réaliser des machines capables de simuler l'intelligence humaine »"]
            print('speaker: '+ str(a))
            speak(random.choice(reply))
            stream.start_stream()
           
            print("...")
            print('écoute...')
        
        elif "ok" in a or "d'accord" in a:
            os.system('cls')
            stream.stop_stream()
            reply = ["trés bien", "ok", "bien"]
            print('speaker: '+ str(a))
            speak(random.choice(reply))
            speak("autres chose ?")
            stream.start_stream()
           
            print("...")
            print('écoute...')
        
        elif "oui" in a or "autres chose" in a or 'autre chose' in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak("quoi donc?")
            stream.start_stream()
            print("...")
            print('écoute...')

        elif "non merci" in a or "non" in a or "nop" in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak("d'accord!")
            stream.start_stream()
            print("...")
            print('écoute...')

        

        
#......................LAMPE........................./
        elif "allume la lampe du salon" in a or "allume la lumière du salon" in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a)) 
            url = 'http://192.168.1.10/?LED1=ON'
            webbrowser.open(url)
            speak("c'est fait la lumière du salon est allumée")
            pyautogui.hotkey('ctrl','F4')
            speak("autre chose?")
            stream.start_stream()
           
            print("...")
            print('écoute...')
        elif "arrête la lampe du salon" in a or "arrête la lumière du salon" in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            url = 'http://192.168.1.10/?LED1=OFF'
            webbrowser.open(url)
            speak("c'est fait la lumière du salon est éteinte")
            speak("autre chose?")
            pyautogui.hotkey('ctrl','F4')
            stream.start_stream()
            print("...")
            print('écoute...')

        elif "allume la lampe de la cuisine" in a or "allume la lumière de la cuisine" in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            #cnt.led_cuisine(1)
            speak("c'est fait, la lumière de la cuisine est allumée")
            speak("autre chose?")
            stream.start_stream()
           
            print("...")
            print('écoute...')
        elif "arrête la lampe de la cuisine" in a or "arrête la lumière de la cuisine" in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            #cnt.led_cuisine(0)
            speak("c'est fait, la lumière de la cuisine est éteinte")
            speak("autre chose?")
            stream.start_stream()
           
            print("...")
            print('écoute...')

#............................TACHES..................................
        
        elif 'réduit la fenêtre windows' in a or 'réduit le programme' in a or 'réduit la fenêtre' in a:
            os.system('cls')
            stream.stop_stream()
            speak('réduction de la fenêtre windows')            
            pyautogui.hotkey('win','down','down')
            speak("voilà c'est fait")
            stream.start_stream()
            print('')
            print('écoute')
            print('')
        elif 'augmente la fenêtre windows' in a or "augmente la fenêtre windows du programme" in a or "augmente la fenêtre" in a:
            os.system('cls')
            stream.stop_stream()
            speak('ok')
            pyautogui.hotkey('win','up','up')
            speak("quoi d'autre?")
            stream.start_stream()
            print('')            
            print('écoute')            
            print('') 
        elif 'ferme le programme' in a or "ferme le fenêtre " in a:
            os.system('cls')
            stream.stop_stream()
            speak('fermeture du programme actuellement ouvert')
            pyautogui.hotkey('alt', 'f4')
            speak('Autre chose ?')
            stream.start_stream()
            print('')            
            print('écoute')            
            print('')            

        elif "Ouvre l'explorateur de fichier" in a or 'explorateur de fichier' in a or 'explorateur' in a:
            os.system('cls')
            stream.stop_stream()
            pyautogui.hotkey('win','e')
            speak("c'est fait")
            stream.start_stream()
            print('')            
            print('écoute')            
            print('')
            
#.........................arret programme................./

        elif "éteins l'ordinateur" in a or "arrête l'ordinateur" in a :
            speak(f"Le système est sur le point de s'arreter")
            os.system("shutdown /s /t 1")


        elif "Verrouillage de l'ordinateur"  in a or "verrouille l'ordinateur" in a or "verrouille" in a or "verouillage" in a:
            speak("verrouillage de l'ordinateur")
            os.system("shutdown -l")
            stream.start_stream()
            ("l'ordinateur est actuellement vérrouiller")
            print('')            
            print('écoute')            
            print('')


        elif "au revoir" in a or "tu peux y aller" in a or "prends une pause" in a or "pause" in a or "arrêt du programme" in a or "au-revoir" in a:
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            speak("ok!")
            a = ["rappelez moi en cas de besoins","pas de problème, je reste à votre disposition"]
            speak(random.choice(a))
            os.system('taskkill /f /im gif_1.exe')
            sys.exit() 
#................................///IAMGE..................////////
        elif "affiche le programme" in a :
            os.system('cls')
            stream.stop_stream()
            print('speaker: '+ str(a))
            img = Image.open('.\\image\\bik.bip.4.jpg')
            img.show()
            #os.startfile(".\image\bik.bip.4.jpg")
            speak('voilà')
            #speak("je l'agrandi pour vous")
        #pyautogui.hotkey('')
            stream.start_stream()
            print('')            
            print('écoute')            
            print('')
            



        

       



        



