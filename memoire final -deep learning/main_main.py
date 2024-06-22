from vosk import Model, KaldiRecognizer
import pyttsx3
import pyaudio
import msvcrt as m
import random
import os
import json
import datetime
import time
import webbrowser as web
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from lanc import Ui_MainWindow
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMessageBox)
from demarrage import Ui_Lanc
import pyautogui
import requests
import logging
import wikipedia
import pywhatkit
from bs4 import BeautifulSoup
from Neural_network import NeuralNet
from nltk_utils import tokenize, bag_of_words
import torch
import time

## ==> GLOBALS
counter = 0
 
logging.basicConfig(level=logging.INFO,filename="app.log",
                filemode="a",
                format='%(asctime)s - %(levelname)s - %(message)s - %(processName)s')

def wait():
    m.getch()
    
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
#Lanc_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_V110_frFR_JulieM"
rate = engine.setProperty("rate",195)
engine.setProperty('voice', voices[0].id)

# Wake word
WAKE_WORD = "lanc"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding='utf-8') as f:
    start = time.time()
    intents = json.load(f)
    end = time.time()
    print(f'Time taken to load json file: {end-start:.5f} seconds')

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

def speak(audio):
    print ("LANCE:" + str(audio)) #pour prototype 1
    engine.say(audio)
    engine.runAndWait()

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
    Time = datetime.datetime.now().strftime("il est actuellement %H:%M:%S") 
    speak(Time)
    
def date():
    date = datetime.datetime.now().strftime(" aujourdh'ui nous sommes le %A %d %B %Y") 
    speak (date)

try:
    modelv = Model("vosk-model-small-fr-0.22")
    rec = KaldiRecognizer(modelv, 16000)
    cap = pyaudio.PyAudio()
    stream=cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
except:
    speak('je ne detecte aucun micro')
    

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()
    def TaskExecution(self):
        wishme()
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                continue
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result = json.loads(result)
                print("speaker: " + result["text"])
                a = result["text"]

                # Supprimez le mot de déclenchement de la commande reconnue
                a = a.replace(WAKE_WORD, "").strip()
                sentence = a
                sentence = tokenize(sentence)
                X = bag_of_words(sentence, all_words)
                X = X.reshape(1, X.shape[0])
                X = torch.from_numpy(X).to(device)

                output = model(X)
                _, predicted = torch.max(output, dim=1)

                tag = tags[predicted.item()]

                probs = torch.softmax(output, dim=1)
                prob = probs[0][predicted.item()]
                if prob.item() > 0.75:
                    for intent in intents['intents']:
                        if tag == intent["tag"]:
                            os.system('cls')
                            stream.stop_stream()
                            speak(random.choice(intent['responses']))
                            stream.start_stream()
                            break
                else:
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
                    else:
                        # Si la commande n'a pas été comprise
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak("Je n'ai pas compris. Pouvez-vous reformuler?")
                        stream.start_stream()
                        print("...")
                        print('écoute...')
                    
        


startExecution = MainThread()
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Commande_pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Commandes))
        self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Acceuil))
        self.ui.Mores_pushButton_2.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Mores))
        self.ui.About_pushButton_3.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.About))
        self.ui.Contact_pushButton_4.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.Contact))
        self.ui.start_pushButton_9.clicked.connect(self.startTask)
        self.ui.enregistre_pushButton_8.clicked.connect(self.save_text)

#..............WEB PAGE.......................//
        self.ui.face_pushButton_13.clicked.connect(self.facebook)
        self.ui.email_pushButton_15.clicked.connect(self.gmail)
        self.ui.insta_pushButton_10.clicked.connect(self.instagram)
        self.ui.tiktok_pushButton_11.clicked.connect(self.tiktok)
        self.ui.google_pushButton_14.clicked.connect(self.google)
        self.ui.pushButton_12.clicked.connect(self.youtube)
#..............VOLUME.....................//
        self.ui.voulume_moins_pushButton_5.clicked.connect(self.volume_moins)
        self.ui.volume_plus_pushButton_7.clicked.connect(self.volume_up)
        self.ui.volume_mute_pushButton_6.clicked.connect(self.mute)
#controle par la main
        self.ui.lampe_pushButton_16.clicked.connect(self.hand_controle)
#change ip
        self.ui.pushButton_25.clicked.connect(self.save_ip)
#..................LED CONTROLE..................//
        self.ui.pushButton_17.clicked.connect(self.led1_on)
        self.ui.pushButton_18.clicked.connect(self.led1_off)
        self.ui.pushButton_22.clicked.connect(self.led2_on)
        self.ui.pushButton_19.clicked.connect(self.led2_off)
#led non connectées///////////
        self.ui.pushButton_24.clicked.connect(self.no_connect)
        self.ui.pushButton_26.clicked.connect(self.no_connect)
        self.ui.pushButton_27.clicked.connect(self.no_connect)
        self.ui.pushButton_23.clicked.connect(self.no_connect)


    def no_connect(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Ces boutons ne sont pas connectés")
        msg.setWindowTitle("Attention")
        ok_button = msg.addButton(QPushButton("OK"), QMessageBox.ActionRole)
        msg.exec_()
        if msg.clickedButton() == ok_button:
            msg.close()
        
    def led1_on(self):
        try:
            with open("ip.txt", "r") as f:
                ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                print(ip)
        except:
            print("erreur de lecture")
        delay =1
        requests.get(f'http://{ip}/?led1=on')
        time.sleep(delay)
    
    def led1_off(self):
        try:
            with open("ip.txt", "r") as f:
                ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                print(ip)
        except:
            print("erreur de lecture")
        delay =1
        requests.get(f'http://{ip}/?led1=off')
        time.sleep(delay)
    
    def led2_on(self):
        try:
            with open("ip.txt", "r") as f:
                ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                print(ip)
        except:
            print("erreur de lecture")
        delay =1
        requests.get(f'http://{ip}/?led2=on')
        time.sleep(delay)
    
    def led2_off(self):
        try:
            with open("ip.txt", "r") as f:
                ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                print(ip)
        except:
            print("erreur de lecture")
        delay =1
        requests.get(f'http://{ip}/?led2=off')
        time.sleep(delay)
    
        
    def hand_controle(self):
        import main_controller

        
    def save_text(self):
        self.user_lineEdit = QLineEdit()
        text = self.user_lineEdit.text() 
        with open("name.txt", "w") as f:
            f.write(text)
        msg = QMessageBox()
        msg.setText('Utilisateur enrégistré, Appuyer sur Start')
        msg.exec_()
        
    def save_ip(self):
        self.lineEdit_2 = QLineEdit()
        text = self.lineEdit_2.text() 
        with open("ip.txt", "w") as f:
            f.write(text)
        msg = QMessageBox()
        msg.setText('ip enrégistré avec succés')
        msg.exec_()
         
    def gmail(self):
        web.open("https://www.gmail.com/")
            
    def facebook(self):
        web.open("https://www.facebook.com/")

    def instagram(self):
        web.open("https://www.instagram.com/")

    def tiktok(self):
        web.open("https://www.tiktok.com/")

    def google(self):
        web.open("https://www.google.com/")

    def youtube(self):
        web.open("https://www.youtube.com/")

    def volume_moins(self):
        pyautogui.press('volumedown')

    def volume_up(self):
        pyautogui.press('volumeup')
    
    def mute(self):
        pyautogui.press('volumemute')

    def startTask(self):
        self.ui.movie = QtGui.QMovie("Images/Gif/AI-visualization-design-unscreen.gif")
        self.ui.gif_label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
      
        startExecution.start()
class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_Lanc()
        self.ui.setupUi(self)

        ## REMOVE TITLE BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        ## QTIMER ==> START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)
        # CHANGE DESCRIPTION
        # Initial Text
        self.ui.description.setText("chargement du modéle")
        # Change Texts
        QtCore.QTimer.singleShot(1500, lambda: self.ui.description.setText("Un Instant"))
        QtCore.QTimer.singleShot(3000, lambda: self.ui.description.setText("Affichage de l'interface"))
        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##
    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):
        global counter
        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(counter)
        # CLOSE SPLASH SCREE AND OPEN APP
        if counter > 100:
            # STOP TIMER
            self.timer.stop()
            # SHOW MAIN WINDOW
            self.main = Main()
            self.main.show()
            # CLOSE SPLASH SCREEN
            self.close()
        # INCREASE COUNTER
        counter += 1
app = QApplication(sys.argv)
Lanc = SplashScreen()
exit(app.exec_())
