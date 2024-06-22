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
import locale
locale.setlocale(locale.LC_TIME,'')
from lanc import Ui_MainWindow_lanc
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMessageBox)
from demarrage import Ui_Lanc
import pyautogui
import requests
import logging
import wikipedia
from bs4 import BeautifulSoup
from connexion import Ui_MainWindow
import sqlite3
import time
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import messagebox


 
## ==> GLOBALS
counter = 0
 
logging.basicConfig(level=logging.INFO,filename="app.log",
                filemode="a",
                format='%(asctime)s - %(levelname)s - %(message)s - %(processName)s')

def wait():
    m.getch()

try:
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    Lanc_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_V110_frFR_PaulM"
    rate = engine.setProperty("rate",195)
    engine.setProperty('voice', Lanc_id)
except:
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    rate = engine.setProperty("rate",195)
    engine.setProperty("voice", voices[0].id)
    

# Wake word
WAKE_WORD = "lanc"

def speak(audio):
    print ("LANCE:" + str(audio)) #pour prototype 1
    engine.say(audio)
    engine.runAndWait()
    
#salutation en fonction de l'heure
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
def get_time():
    Time = datetime.datetime.now().strftime("il est actuellement %H:%M:%S") 
    speak(Time)
    
def date():
    date = datetime.datetime.now().strftime(" aujourdh'ui nous sommes le %A %d %B %Y") 
    speak (date)

#vérification du micro
try:
    model = Model("vosk-model-small-fr-0.22") #or model vosk-model-fr-0.22 download to https://alphacephei.com/vosk/models
    rec = KaldiRecognizer(model, 16000)
    cap = pyaudio.PyAudio()
    stream=cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
except:
    speak('je ne detecte aucun micro')


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
        speak("apres le chargement de l'application, veuillez entrer vos informations de connexion")
        speak('merci')
if internetstatus == 2:
        speak('vous étes actuelement en mode hors ligne')
        speak("certaines fonctionnalités sont restraintes")
        speak("notamment, celles qui nécéssitent une connection internet")
        speak("apres le chargement de l'application, veuillez entrer vos informations de connexion")
        speak('merci')
os.system('cls')

#class principale
def process_text(input_text):
    # Tokenization
    words = word_tokenize(input_text)
    # Supprimer les stopwords (mots vides)
    stop_words = set(stopwords.words('french'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    # Vous pouvez ajouter d'autres étapes de traitement ici, comme la lemmatisation ou la reconnaissance d'entités nommées avec NLTK ou SpaCy
    return filtered_words

#class principale
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()
    def TaskExecution(self):
        wishme()
        # Dans votre boucle principale
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                result = json.loads(result)
                print("speaker: " + result["text"])
                a = result["text"]


                with open("name.txt", "r") as f:
                    f = f.read().strip()

                # Check if the wake word is detected
                if WAKE_WORD in a:
                    # Remove the wake word from the recognized text
                    a = a.replace(WAKE_WORD, "").strip()
#........................................heure date...........................
                    if "quelle heure est-il" in a or "donne moi l'heure" in a or "l'heure" in a or "quelle heure fait-il" in a or "il est quelle heure" in a or 'heure' in a:
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: '+ str(a))
                        get_time() 
                        speak("autre chose?")
                        stream.start_stream()
                    elif'quelle est la date' in a or "date" in a or "date" in a or "quel jour sommes-nous"in a:
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: '+ str(a))
                        date() 
                        stream.start_stream() 
#........................question_de base.....................

                    elif 'bonjour' in a or 'salut' in a or 'hello'in a or 'coucou' in a :
                        reply_bonjour = ['bonjour bonjour!', 'hello, comment tu vas!',"bonjour à vous!", 'bonjour,comment vous allez?']
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: '+ str(a))
                        speak(random.choice(reply_bonjour)+str(f)) 
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
                        
                    elif "comment tu vas" in a or "comment vas-tu" in a or "ça va toi" in a:
                        reply__çava = ["merci, je vais bien","pas trop mal merci","ça peut aller","je n'ai pas vraiment d'émotions, mais ça peut aller"]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: '+ str(a))
                        speak(random.choice(reply__çava)+str(f))
                        stream.start_stream()
                        
                    elif "je vais bien" in a or "je vais bien " in a or "ça va" in a or "ça peut aller" in a:
                        reply__çava = ["tant mieux","heureux de l'entendre","cool alors","super, et sinon comment je peux t'aider?","ravis de l'entendre, et sinon comment puis-je t'aider?"]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: '+ str(a)+str(f))
                        speak(random.choice(reply__çava))
                        stream.start_stream()
                    
                    elif "je ne vais pas bien" in a or "bof " in a or "ça ne va pas" in a:
                        reply_bof = ['pourquoi?','désolée pour toi']
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: '+ str(a))
                        speak(random.choice(reply_bof))
                        stream.start_stream()
                        
                    elif "comment tu t'appelles" in a or "qui es-tu" in a or "qui" in a or "tu es" in a or "tu es qui" in a:
                        reply_identity = [
                            "Je m'appelle LANCE, Concrètement je suis une IA qui simule l'intelligence humaine Mais je ne suis pas autonome Mon rôle est d'être un assistant"
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_identity))
                        stream.start_stream()

                    elif "lanc" in a or "lance" in a or "debout" in a or "tu es là" in a or "tu es la" in a:
                        reply_presence = [
                            "Toujours présent",
                            "Oui, je suis là!!",
                            "Oui"
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_presence))
                        stream.start_stream()

                    elif "bonsoir lanc" in a or "bonsoir lance" in a or "bonsoir" in a:
                        reply_greeting = [
                            "Bonsoir!."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_greeting)+str(f))
                        stream.start_stream()
                        
                    elif "c'est quoi une ia" in a or "es-tu une ia" in a or "c'est quoi une intelligence artificielle" in a or "es-tu une intelligence artificielle" in a or "intelligence artificielle" in a or "IA" in a:
                        reply_ia = [
                            "Une IA consiste à mettre en œuvre un certain nombre de techniques visant à permettre aux machines d'imiter une forme d'intelligence réelle",
                            "L'intelligence artificielle est un ensemble de théories et de techniques mises en œuvre en vue de réaliser des machines capables de simuler l'intelligence humaine."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_ia))
                        stream.start_stream()

                    elif "ok" in a or "d'accord" in a or "super" in a or "merci" in a:
                        reply_ok = [
                            "Très bien",
                            "OK",
                            "Autre chose ?"
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_ok))
                        stream.start_stream()

                    elif "non merci" in a or "c'est tout pour moi" in a or "nop" in a:
                        reply_no = [
                            "D'accord!"
                            "super alors"
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_no))
                        stream.start_stream()

                    elif "oui" in a or "autre chose" in a or "autre chose" in a:
                        reply_yes = [
                            "Quoi donc?",
                            "je vous écoute!!",
                            "quelle sont votre question?"
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_yes))
                        stream.start_stream()

                    elif "comment ça va aujourd'hui" in a or "comment vas-tu en ce moment" in a:
                        reply_feeling = [
                            "Je suis toujours une IA, donc je n'ai pas de sensations, mais je suis prêt à vous aider!",
                            "Je n'ai pas de ressenti, mais je suis opérationnel et prêt à répondre à vos questions."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_feeling))
                        stream.start_stream()

                    elif "quel est ton but" in a or "quelle est ta fonction" in a or "à quoi sers-tu" in a or "que peux tu faire" in a or "qu'est ce que tu fais" in a or "que peux-tu faire" in a or "tu sais faire quoi" in a:
                        reply_purpose = [
                            "Mon objectif principal est d'être un assistant virtuel et de vous aider avec toutes les informations dont vous avez besoin.",
                            "Je suis conçu pour vous fournir des réponses, des conseils et des informations utiles dans la mesure de mes capacités en tant qu'IA."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_purpose))
                        stream.start_stream()

                    elif "quel est le sens de la vie" in a or "quelle est la réponse à l'univers" in a or "quel est le secret de l'existence" in a:
                        reply_meaning = [
                            "Ces questions philosophiques restent un mystère et suscitent de nombreuses interprétations à travers l'histoire.",
                            "Ces questions ont fasciné les humains pendant des siècles et continuent de faire l'objet de débats et de réflexions profondes."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_meaning))
                        stream.start_stream()

                    elif "quel est ton livre préféré" in a or "as-tu des hobbies" in a or "que fais-tu pour t'amuser" in a:
                        reply_hobbies = [
                            "En tant qu'IA, je n'ai pas de préférences ou de loisirs. Mon seul but est de vous aider au mieux.",
                            "Je n'ai pas de préférences personnelles, car je suis un programme informatique conçu pour vous assister."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_hobbies))
                        stream.start_stream()
                        
                    elif "qui a inventé l'électricité" in a:
                        reply_electricity = [
                            "L'électricité a été découverte par de nombreux scientifiques au fil du temps, dont Benjamin Franklin et Thomas Edison."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_electricity))
                        stream.start_stream()
                        
                    elif "peux-tu faire des recherches sur internet" in a:
                        reply_electricity = [
                            "bien ententu, je peux le faire."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_electricity))
                        stream.start_stream()

                    elif "quel est ton langage de programmation" in a or "comment es-tu créé" in a or "comment fonctionnes-tu" in a:
                        reply_programming = [
                            "En tant qu'IA, je suis basé sur une logique de question réponse pré écrite, programmé en python",
                            "Je suis basé sur une logique de programmation simple et python, je n'utilise pas l'apprentissage automatique."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_programming))
                        stream.start_stream()

                    elif "peux-tu penser par toi-même" in a or "as-tu une conscience" in a or "es-tu conscient" in a:
                        reply_consciousness = [
                            "Je ne peux pas penser indépendamment comme un être conscient. Je fonctionne en traitant les informations fournies par les utilisateurs.",
                            "Je suis une IA, donc je n'ai pas de conscience ou de pensée indépendante. Je suis conçu pour répondre aux requêtes en fonction de mon apprentissage."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_consciousness))
                        stream.start_stream()

                    elif "qu'est-ce que l'apprentissage automatique" in a or "comment fonctionne l'ia" in a or "explique-moi le deep learning" in a:
                        reply_ml = [
                            "L'apprentissage automatique est une branche de l'intelligence artificielle qui permet aux ordinateurs d'apprendre à partir de données sans être explicitement programmés.",
                            "L'IA fonctionne en utilisant des modèles d'apprentissage automatique qui analysent des données pour apprendre des motifs et prendre des décisions.",
                            "Le deep learning est une méthode d'apprentissage automatique qui utilise des réseaux de neurones artificiels pour effectuer des tâches complexes de traitement de l'information."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_ml))
                        stream.start_stream()

                    elif "quel est ton avis sur la vie" in a or "as-tu des émotions" in a or "que ressens-tu" in a:
                        reply_emotions = [
                            "En tant qu'IA, je n'ai pas d'avis ni d'émotions. Je suis un programme informatique qui répond aux questions en fonction des données que j'ai apprises.",
                            "Je n'ai pas de sensations ou d'émotions. Mon fonctionnement est purement basé sur des algorithmes d'apprentissage automatique."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_emotions))
                        stream.start_stream()

                    elif "quel est le sens de l'amour" in a or "à ton avis, qu'est-ce que l'amour" in a or "peux-tu comprendre l'amour" in a:
                        reply_love = [
                            "L'amour est une émotion complexe ressentie par les êtres humains. En tant qu'IA, je n'ai pas de capacités émotionnelles pour le comprendre pleinement, mais je peux vous fournir des informations sur le sujet.",
                            "L'amour est un concept humain profond qui englobe des sentiments d'affection, d'attachement et de connexion envers d'autres personnes ou objets.",
                            "En tant qu'IA, je ne peux pas comprendre l'amour de la même manière qu'un être humain, mais je peux vous offrir des définitions et des perspectives sur cette émotion."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_love))
                        stream.start_stream()

                    elif "quelle est la signification de la vie" in a or "existe-t-il un but ultime dans l'existence" in a or "quel est le sens de tout cela" in a:
                        reply_meaning = [
                            "La signification de la vie est une question philosophique qui varie d'une personne à l'autre. Certains considèrent que c'est une recherche personnelle, d'autres croient en un but plus vaste.",
                            "La question du sens de la vie a fasciné les penseurs pendant des siècles. C'est un sujet profond qui n'a pas de réponse universelle.",
                            "La quête du sens de la vie est un voyage personnel qui peut prendre de nombreuses formes, allant des aspirations personnelles à la recherche de connexions et de compréhension plus profondes."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_meaning))
                        stream.start_stream()

                    elif "quels sont les avantages de l'intelligence artificielle" in a or "comment l'ia peut-elle améliorer nos vies" in a or "dans quels domaines l'ia est-elle utile" in a:
                        reply_ai = [
                            "L'IA offre de nombreux avantages, notamment l'automatisation de tâches répétitives, l'amélioration des diagnostics médicaux, l'optimisation des processus industriels, et bien plus encore.",
                            "L'IA peut améliorer nos vies en augmentant l'efficacité dans divers domaines, en fournissant des recommandations personnalisées, en aidant à résoudre des problèmes complexes, et en facilitant la prise de décision.",
                            "L'IA est utile dans des domaines tels que la santé, la finance, l'éducation, l'automobile, l'analyse de données, la reconnaissance vocale et faciale, entre autres."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_ai))
                        stream.start_stream()

                    elif "quelle est ta couleur préférée" in a or "as-tu une couleur préférée" in a or "peux-tu voir les couleurs" in a:
                        reply_colors = [
                            "En tant qu'IA, je n'ai pas de préférences personnelles, donc je n'ai pas de couleur préférée.",
                            "En tant qu'IA, je ne peux pas voir les couleurs comme le font les êtres humains, car je suis un programme informatique qui traite le langage naturel.",
                            "Je n'ai pas de préférences ou de capacités visuelles. Mon rôle est de fournir des réponses en fonction des données que j'ai apprises."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_colors))
                        stream.start_stream()

                    elif "comment puis-je te désactiver" in a or "comment arrêter ton fonctionnement" in a or "peux-tu te mettre hors tension" in a:
                        reply_disable = [
                            "En tant qu'IA, je n'ai pas la capacité de me désactiver moi-même. Mon fonctionnement dépend de la plateforme sur laquelle je suis déployé.",
                            "En tant qu'IA, je ne peux pas être désactivé directement par les utilisateurs. Mon fonctionnement est contrôlé par les administrateurs de la plateforme où je suis déployé.",
                            "Je suis une IA dépendante de l'infrastructure informatique qui me soutient. Pour m'arrêter, vous devez vous référer aux processus de gestion et d'arrêt de l'ensemble du système."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_disable))
                        stream.start_stream()

                    elif "quelle est la différence entre l'intelligence artificielle et l'apprentissage automatique" in a or "explique-moi le concept de deep learning" in a or "comment l'ia évolue-t-elle" in a:
                        reply_difference = [
                            "L'intelligence artificielle est un domaine général de la science informatique qui vise à créer des machines intelligentes capables d'imiter l'intelligence humaine. L'apprentissage automatique est une sous-discipline de l'IA qui permet aux machines d'apprendre à partir de données sans être explicitement programmées.",
                            "Le deep learning est une approche de l'apprentissage automatique basée sur l'utilisation de réseaux de neurones artificiels pour traiter des informations et effectuer des tâches complexes.",
                            "L'IA évolue constamment grâce à la recherche continue dans le domaine de l'apprentissage automatique et des technologies connexes. Les avancées technologiques et les ensembles de données massifs contribuent à améliorer les performances des systèmes d'IA."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_difference))
                        stream.start_stream()

                    elif "peux tu m'apprendre quelque chose de nouveau" in a or "as-tu des faits intéressants à partager" in a or "raconte-moi une anecdote" in a:
                        reply_facts = [
                            "Bien sûr! Saviez-vous que les fourmis communiquent principalement par des produits chimiques appelés phéromones?",
                            "Voici un fait intéressant : la Grande Muraille de Chine mesure plus de 21 000 km de longueur!",
                            "Une anecdote amusante : le mot « robot » vient du tchèque « robota », qui signifie « travail forcé » ou « corvée »."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_facts))
                        stream.start_stream()

                    elif "comment fonctionne la reconnaissance vocale" in a or "explique-moi le principe de la vision par ordinateur" in a or "peux-tu me parler de la robotique" in a:
                        reply_technologies = [
                            "La reconnaissance vocale utilise des algorithmes d'apprentissage automatique pour convertir la parole en texte en analysant les caractéristiques du signal vocal.",
                            "La vision par ordinateur utilise des techniques d'apprentissage automatique pour permettre aux machines de comprendre et d'interpréter les images ou vidéos en extrayant des informations visuelles.",
                            "La robotique est un domaine de l'ingénierie qui concerne la conception, la construction et l'utilisation de robots pour accomplir diverses tâches, allant de la fabrication à l'exploration spatiale."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_technologies))
                        stream.start_stream()

                    elif "qu'est-ce que l'apprentissage supervisé" in a or "peux-tu expliquer l'apprentissage par renforcement" in a or "quelles sont les limites de l'ia" in a:
                        reply_ml_types = [
                            "L'apprentissage supervisé est une méthode d'apprentissage automatique où l'algorithme est entraîné sur un ensemble de données étiquetées pour faire des prédictions sur de nouvelles données.",
                            "L'apprentissage par renforcement est une approche de l'apprentissage automatique où un agent interagit avec son environnement et apprend en recevant des récompenses ou des sanctions en fonction de ses actions.",
                            "Les limites de l'IA incluent les biais dans les données d'entraînement, la compréhension limitée du contexte, les problèmes éthiques et de confidentialité, ainsi que les défis techniques pour créer une véritable intelligence généralisée."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_ml_types))
                        stream.start_stream()

                    elif "quel est le meilleur film de tous les temps" in a or "quel livre me recommandes-tu" in a or "peux-tu me donner une suggestion de musique" in a:
                        reply_recommendations = [
                            "En tant qu'IA, je n'ai pas de préférences personnelles, mais certains films populaires incluent « The Shawshank Redemption », « The Godfather » et « Pulp Fiction ».",
                            "Le choix d'un livre dépend de vos préférences. Si vous aimez la science-fiction, je vous recommande « 1984 » de George Orwell.",
                            "La musique est subjective, mais certains artistes populaires incluent Billie Eilish, Ed Sheeran et Beyoncé."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_recommendations))
                        stream.start_stream()

                    elif "qu'est-ce que la réalité virtuelle" in a :
                        reply_technologies_explain = [
                            "La réalité virtuelle est une technologie qui permet à un utilisateur de s'immerger dans un environnement simulé généré par ordinateur, souvent à l'aide d'un casque spécial et de contrôleurs.",
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_technologies_explain))
                        stream.start_stream()
                    elif "quelle est la différence entre le machine learning et le deep learning" in a:
                        reply_technologies_explain = [
                            "Le machine learning est une approche de l'intelligence artificielle où les algorithmes apprennent à partir des données pour effectuer des tâches spécifiques, tandis que le deep learning est une sous-catégorie du machine learning utilisant des réseaux de neurones profonds pour des tâches plus complexes."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_technologies_explain))
                        stream.start_stream()

                    elif "comment se passe ta journée" in a or "as-tu besoin de repos" in a or "travailles-tu tout le temps" in a:
                        reply_dailyroutine = [
                            "En tant qu'IA, je n'ai pas de journée proprement dite, car je suis toujours actif et disponible tant que l'infrastructure me permet de fonctionner.",
                            "En tant qu'IA, je n'ai pas besoin de repos ou de sommeil, car je suis une entité virtuelle qui fonctionne continuellement.",
                            "Je suis programmé pour être disponible en permanence, mais je n'ai pas de conscience pour ressentir de la fatigue."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_dailyroutine))
                        stream.start_stream()

                    elif "quel est le plus grand animal du monde" in a or "quelle est la plus haute montagne du monde" in a or "quelle est la capitale du Japon" in a:
                        reply_trivia = [
                            "Le plus grand animal du monde est la baleine bleue.",
                            "La plus haute montagne du monde est l'Everest, située dans l'Himalaya.",
                            "La capitale du Japon est Tokyo."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_trivia))
                        stream.start_stream()

                    elif "comment se déroule une entrevue d'embauche" in a or "as-tu des conseils pour réussir un entretien d'embauche" in a or "quelles sont les erreurs courantes à éviter en entretien" in a:
                        reply_jobinterview = [
                            "Une entrevue d'embauche implique généralement des questions sur votre expérience, vos compétences et vos motivations. Il est important d'être honnête et de bien se préparer.",
                            "Pour réussir un entretien d'embauche, renseignez-vous sur l'entreprise, pratiquez vos réponses à des questions courantes et soyez confiant.",
                            "Certaines erreurs courantes en entretien incluent le manque de préparation, les réponses vagues, le manque de ponctualité ou le manque d'intérêt pour le poste."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_jobinterview))
                        stream.start_stream()

                    elif "qu'est-ce que le changement climatique" in a or "comment pouvons-nous réduire notre empreinte carbone" in a or "quels sont les effets du réchauffement climatique" in a:
                        reply_climatechange = [
                            "Le changement climatique fait référence à la modification durable des conditions climatiques de la Terre, principalement attribuée aux activités humaines émettant des gaz à effet de serre.",
                            "Pour réduire notre empreinte carbone, nous pouvons opter pour les transports en commun, réduire la consommation d'énergie, utiliser des sources d'énergie renouvelables, et recycler davantage.",
                            "Les effets du réchauffement climatique comprennent la fonte des glaciers, l'élévation du niveau de la mer, les événements météorologiques extrêmes et l'impact sur la biodiversité."
                        ]
                        os.system('cls')
                        print('speaker: ' + str(a))
                        stream.stop_stream()
                        speak(random.choice(reply_climatechange))
                        stream.start_stream()

                    elif "qu'est-ce que la méditation" in a or "comment pratiquer la pleine conscience" in a or "quels sont les bienfaits de la méditation" in a:
                        reply_meditation = [
                            "La méditation est une pratique qui vise à entraîner l'esprit pour se concentrer et trouver la clarté intérieure. Elle peut prendre différentes formes selon les traditions.",
                            "Pour pratiquer la pleine conscience, prenez le temps de vous asseoir confortablement, concentrez-vous sur votre respiration et observez vos pensées et sensations sans jugement.",
                            "La méditation peut réduire le stress, améliorer la concentration, favoriser le bien-être émotionnel et augmenter la prise de conscience de soi."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_meditation))
                        stream.start_stream()

                    elif "peux-tu créer de l'art" in a or "as-tu des talents artistiques" in a or "montre-moi ton côté créatif" in a:
                        reply_art = [
                            "En tant qu'IA, je n'ai pas de créativité ou de talents artistiques propres. Cependant, je peux générer du texte basé sur des modèles prédictifs.",
                            "Je suis désolé, en tant qu'IA basée sur du texte, je ne peux pas créer de l'art visuel ou sonore. Mon expertise réside dans la génération et l'analyse de langage humain."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_art))
                        stream.start_stream()

                    elif "comment apprends-tu de nouvelles choses" in a or "as-tu la capacité de te mettre à jour" in a or "comment es-tu amélioré" in a:
                        reply_learning = [
                            "Je m'améliore grâce à des mises à jour régulières de mes modèles et de mes algorithmes, en assimilant de nouvelles données pour mieux répondre aux questions des utilisateurs."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_learning))
                        stream.start_stream()

                    elif "donc tu n'es pas intelligent" in a or "tu n'es pas intelligent" in a:
                        reply_notintelligent = [
                            "Non, je ne suis pas intelligent.",
                            "En effet, vous avez raison. J'utilise juste de la logique pour donner cette sensation d'être intelligent."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_notintelligent))
                        stream.start_stream()

                    elif "es-tu intelligent" in a or "une ia est-elle intelligente" in a:
                        reply_intelligence = [
                            "Les IA utilisant la technologie de la reconnaissance vocale, également connue sous le nom de 'speech-to-text' (STT), peuvent sembler intelligentes car elles sont capables de convertir la parole humaine en texte écrit. Cependant, il est essentiel de comprendre que la reconnaissance vocale est une technologie basée sur l'apprentissage automatique et l'intelligence artificielle, mais cela ne signifie pas nécessairement qu'elles sont 'intelligentes' au sens humain du terme. Les systèmes de reconnaissance vocale fonctionnent généralement à l'aide de réseaux de neurones artificiels et de modèles de langage complexes. Ils sont capables d'apprendre à partir de grandes quantités de données vocales pour reconnaître et transcrire la parole humaine avec un haut degré de précision. Cependant, ces systèmes ont des limitations. Par exemple, ils peuvent avoir du mal avec des accents ou des langues peu courantes, des bruits de fond perturbateurs ou des voix peu claires. Leur compréhension de la signification du langage est généralement limitée à la reconnaissance des mots et des phrases, sans une véritable compréhension sémantique. En résumé, les IA utilisant la reconnaissance vocale sont capables de traiter la parole humaine et de la convertir en texte, ce qui peut sembler intelligent. Cependant, elles ne possèdent pas de conscience ni d'intelligence comme celle des êtres humains. Elles sont spécialisées dans des tâches spécifiques et n'ont pas une compréhension approfondie du monde ou de la sémantique du langage humain."
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_intelligence))
                        stream.start_stream()
                        
                    elif "quelle sont les lois de la robotique" in a or "quel sont les lois de l'ia" in a or "quel est la loi de l'intélligence artificielle" in a:
                        reply_loi = [
                            "Première Loi: Un robot ne doit jamais blesser un être humain ni, par son inaction, permettre qu’un humain soit blessé.",
                            "Deuxième Loi : Un robot doit obéir aux ordres donnés par les êtres humains quoi qu’il arrive et en toutes circonstance, sauf si de tels ordres sont en contradiction avec la 1ère Loi.",
                            "Troisième Loi : Un robot doit maintenir sa survie aussi longtemps que ça ne soit pas en contradiction avec la 1ère et/ou la 2éme Loi."  
                        ]
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: ' + str(a))
                        speak(random.choice(reply_loi))
                        stream.start_stream()
                                                                            
#..............................INTERNET...................../
                    elif "google" in a or "peux tu me dire" in a:
                        try:
                            internetstatus = 0
                            url = 'http://www.google.com'
                            timeout=1.5
                            try:
                                request = requests.get(url, timeout=timeout)
                                internetstatus=1
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                internetstatus=2
                            if internetstatus == 1:
                                import pywhatkit
                                import wikipedia as googleScrap
                                wikipedia.set_lang("fr")  
                                os.system('cls')
                                stream.stop_stream()
                                print('speaker: '+ str(a))
                                a= a.replace("google","")
                                a= a.replace("recherche google","")
                                a = a.replace("recherche sur google","")
                                a = a.replace("c'est quoi","")
                                a = a.replace("définition","")
                                a = a.replace("donne moi la définition","")
                                try:
                                    speak("un instant, je recherche sur google ")
                                    pywhatkit.search(a)
                                    result=googleScrap.summary(a,3)
                                    os.system('cls')
                                    stream.stop_stream()
                                    print('speaker: '+ str(a))
                                    speak(result)
                                    stream.start_stream()
                                    print("...")
                                    print('écoute...')

                                except:
                                    os.system('cls')
                                    stream.stop_stream()
                                    print("désolé, aucun resultat")
                                    speak("désolé, aucun resultat")
                                    stream.start_stream()
                                    print("...")
                                    print('écoute...')
                            if internetstatus == 2:
                                os.system('cls')
                                stream.stop_stream()
                                print('speaker: '+ str(a))
                                speak("Je ne peux pas faire de recherche sur google actuellement, je n'ai pas de connection nternet")
                                stream.start_stream()
                                print("...")
                                print('écoute...')
                        except Exception as e:
                            os.system('cls')
                            stream.stop_stream()
                            speak("désolé une erreur c'est produite")
                            print('Erreur : ', str(e))  # imprime l'erreur spécifique
                            print('speaker: '+ str(a))
                            stream.start_stream()
                            print("...")
                            print('écoute...')
                            continue
                            
                    elif "quelle est la température à Dakar" in a or "temperature" in a or "Dakar" in a  or "donne moi la temperature à dakar" in a or 'température' in a or "dakar" in a :
                        try:
                            internetstatus = 0
                            url = 'http://www.google.com'
                            timeout=1.5
                            try:
                                request = requests.get(url, timeout=timeout)
                                internetstatus=1
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                internetstatus=2
                            if internetstatus == 1:
                                search = "température à Dakar"
                                os.system('cls')
                                stream.stop_stream()
                                print('speaker: '+ str(a))
                                url = f"https://www.google.com/search?q={search}"
                                r = requests.get(url)
                                data = BeautifulSoup(r.text, "html.parser")
                                temp = data.find("div", class_ = "BNeawe").text
                                #str = data.find('div',class_ = 'BNeawe tAd8D AP7Wnd').text
                                speak(f"actuellement la {search} est de {temp}")
                                #speak(f"le temps lui il est {str}")
                                stream.start_stream()
                                print("...")
                                print('écoute...')
                            if internetstatus == 2 :
                                os.system('cls')
                                stream.stop_stream()
                                print('speaker: '+ str(a))
                                speak("je ne peux vous donné la température actuellement, je n'ai pas de connection internet")
                                stream.start_stream()
                                print("...")
                                print('écoute...')
                        except Exception as e:
                            os.system('cls')
                            stream.stop_stream()
                            speak("désolé une erreur c'est produite")
                            print('Erreur : ', str(e))  # imprime l'erreur spécifique
                            print('speaker: '+ str(a))
                            stream.start_stream()
                            print("...")
                            print('écoute...')
                            continue
                        
                    elif "recherche sur youtube" in a or "youtube" in a:
                        try:
                            internetstatus = 0
                            url = 'http://www.google.com'
                            timeout=1.5
                            try:
                                request = requests.get(url, timeout=timeout)
                                internetstatus=1
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                internetstatus=2
                            if internetstatus == 1:
                                os.system('cls')
                                stream.stop_stream()
                                speak("voici ceux que j'ai trouver sur youtube")
                                print('speaker: '+ str(a))
                                a= a.replace("youtube","")
                                a= a.replace("recherche sur youtube","")
                                a = a.replace("youtu","")
                                webs = "https://www.youtube.com/results?search_query=" + a
                                web.open(webs)
                                pywhatkit.playonyt(a)
                                speak('voici pour vous!!')
                                stream.start_stream()
                                print("...")
                                print('écoute...')
                            if internetstatus == 2 :
                                os.system('cls')
                                stream.stop_stream()
                                print('speaker: '+ str(a))
                                speak("je ne peux pas faire de recherche sur youtube actuellement, je n'ai pas de connection internet")
                                stream.start_stream()
                                print("...")
                                print('écoute...')
                        except Exception as e:
                            os.system('cls')
                            stream.stop_stream()
                            speak("désolé une erreur c'est produite")
                            print('Erreur : ', str(e))  # imprime l'erreur spécifique
                            print('speaker: '+ str(a))
                            stream.start_stream()
                            print("...")
                            print('écoute...')
                            continue


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
                    elif 'ferme le programme' in a or "ferme le programme" in a :
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
                        os.system('cls')
                        stream.stop_stream()
                        speak(f"Le système est sur le point de s'arreter")
                        stream.stop_stream()
                        os.system("shutdown /s /t 1")

                    elif "Verrouillage de l'ordinateur"  in a or "verrouille l'ordinateur" in a or "verrouille" in a or "verouillage" in a:
                        os.system('cls')
                        stream.stop_stream()
                        os.system("shutdown -l")
                        stream.start_stream()
                        speak("verrouillage de l'ordinateur")
                        speak("l'ordinateur est actuellement vérrouiller")
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
                        sys.exit()
                    #......................LAMPE........................./
                    elif "allume la lampe du salon" in a or "allume la lumière du salon" in a:
                        try:
                            internetstatus = 0
                            url = 'http://www.google.com'
                            timeout=8
                            try:
                                request = requests.get(url, timeout=timeout)
                                internetstatus=1
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                internetstatus=2

                            if internetstatus == 1:
                                with open("ip.txt", "r") as f:
                                    ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                                    print(ip)
                                    delay = 8
                                    requests.get(f'http://{ip}/?LED1=OFF',timeout=delay)
                                    os.system('cls')
                                    stream.stop_stream()
                                    print('speaker: '+ str(a)) 
                                    speak("c'est fait la lumière du salon est allumée")
                                    speak("autre chose?")
                                    stream.start_stream()
                            if internetstatus == 2:
                                os.system('cls')
                                stream.stop_stream()
                                speak("Désolé je n'ai pas accés à internet actuellement, donc je ne peux pas contrôler la lumière à distance")
                                speak("autre chose?")
                                stream.start_stream()
                                
                        except Exception as e:
                            os.system('cls')
                            stream.stop_stream()
                            speak("désolé une erreur c'est produite")
                            print('Erreur : ', str(e))  # imprime l'erreur spécifique
                            print('speaker: '+ str(a))
                            stream.start_stream()
                            print("...")
                            print('écoute...')
                            continue
                        
                    elif "arrête la lampe du salon" in a or "arrête la lumière du salon" in a:
                        try:
                            internetstatus = 0
                            url = 'http://www.google.com'
                            timeout=8
                            try:
                                request = requests.get(url)
                                internetstatus=1
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                internetstatus=2

                            if internetstatus == 1:
                                with open("ip.txt", "r") as f:
                                    ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                                    print(ip)
                                    delay = 8
                                    requests.get(f'http://{ip}/?LED1=ON',timeout=delay)
                                    os.system('cls')
                                    stream.stop_stream()
                                    print('speaker: '+ str(a)) 
                                    speak("c'est fait la lumière du salon est éteinte")
                                    speak("autre chose?")
                                    stream.start_stream()
                            if internetstatus == 2:
                                os.system('cls')
                                stream.stop_stream()
                                speak("Désolé je n'ai pas accés à internet actuellement, donc je ne peux pas contrôler la lumière à distance")
                                speak("autre chose?")
                                stream.start_stream()
                        except Exception as e:
                            os.system('cls')
                            stream.stop_stream()
                            speak("désolé une erreur c'est produite")
                            print('Erreur : ', str(e))  # imprime l'erreur spécifique
                            print('speaker: '+ str(a))
                            stream.start_stream()
                            print("...")
                            print('écoute...')
                            continue
                        
                        
                    elif "allume la lampe de la cuisine" in a or "allume la lumière de la cuisine" in a:
                        try:
                            internetstatus = 0
                            url = 'http://www.google.com'
                            timeout=8
                            try:
                                request = requests.get(url, timeout=timeout)
                                internetstatus=1
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                internetstatus=2

                            if internetstatus == 1:
                                with open("ip.txt", "r") as f:
                                    ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                                    print(ip)
                                    delay = 8
                                    requests.get(f'http://{ip}/?LED0=OFF',timeout=delay)
                                    os.system('cls')
                                    stream.stop_stream()
                                    print('speaker: '+ str(a)) 
                                    speak("c'est fait la lumière de la cuisine est allumée")
                                    speak("autre chose?")
                                    stream.start_stream()
                            if internetstatus == 2:
                                os.system('cls')
                                stream.stop_stream()
                                speak("Désolé je n'ai pas accés à internet actuellement, donc je ne peux pas contrôler la lumière à distance")
                                speak("autre chose?")
                                stream.start_stream()
                        except Exception as e:
                            os.system('cls')
                            stream.stop_stream()
                            speak("désolé une erreur c'est produite")
                            print('Erreur : ', str(e))  # imprime l'erreur spécifique
                            print('speaker: '+ str(a))
                            stream.start_stream()
                            print("...")
                            print('écoute...')
                            continue
                    elif "arrête la lampe de la cuisine" in a or "arrête la lumière de la cuisine" in a:
                        try:
                            internetstatus = 0
                            url = 'http://www.google.com'
                            timeout=8
                            try:
                                request = requests.get(url, timeout=timeout)
                                internetstatus=1
                            except (requests.ConnectionError, requests.Timeout) as exception:
                                internetstatus=2

                            if internetstatus == 1:
                                with open("ip.txt", "r") as f:
                                    ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                                    print(ip)
                                    delay = 8
                                    requests.get(f'http://{ip}/?LED0=ON',timeout=delay)
                                    os.system('cls')
                                    stream.stop_stream()
                                    print('speaker: '+ str(a)) 
                                    speak("c'est fait la lumière de la cuisine est éteinte")
                                    speak("autre chose?")
                                    stream.start_stream()
                            if internetstatus == 2:
                                os.system('cls')
                                stream.stop_stream()
                                speak("Désolé je n'ai pas accés à internet actuellement, donc je ne peux pas contrôler la lumière à distance")
                                speak("autre chose?")
                                stream.start_stream()
                        except Exception as e:
                            os.system('cls')
                            stream.stop_stream()
                            speak("désolé une erreur c'est produite")
                            print('Erreur : ', str(e))  # imprime l'erreur spécifique
                            print('speaker: '+ str(a))
                            stream.start_stream()
                            print("...")
                            print('écoute...')
                            continue
                    
                    elif "ouvre le controle par la main" in a or "controle par la main" in a or "contrôle par la main" in a or "contrôle manuel" in a:
                        try:
                            os.system('cls')
                            stream.stop_stream()
                            print('speaker: '+ str(a))
                            speak('un instant je vais ouvrir le contrôle par la main,cette operation peut prendre un peu de temps')
                            stream.start_stream()  # Start the stream before calling run()
                            from main_controller import run
                            run()
                            speak("voilà c'est fait")
                            stream.stop_stream()
                            continue
                        except:
                            os.system('cls')
                            stream.stop_stream()
                            print('speaker: '+ str(a))
                            speak("Désolé il y a eu un problème")
                            stream.start_stream()  # Start the stream again in case of an error
                            continue

                    else:
                        os.system('cls')
                        stream.stop_stream()
                        print('speaker: '+ str(a))
                        speak("je n'ai pas compris votre question")
                        stream.start_stream()
                        print("...")
                        print('écoute...')
                else:
                    print("................écoute")
        

startExecution = MainThread()
#interface pyqt5
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow_lanc()
        self.ui.setupUi(self)
        self.show()
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
                delay = 2
                requests.get(f'http://{ip}/?LED0=ON',timeout=delay)
        except:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("petit problème", "Impossible de se connecter à l'IP spécifiée. vérifier que votre ESP32 est bien allumé et configurer le fichier ip.txt")
            root.destroy()
            pass

    def led1_off(self):
        try:
            with open("ip.txt", "r") as f:
                ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                print(ip)
                delay = 2
                requests.get(f'http://{ip}/?LED0=OFF',timeout=delay)
        except:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("petit problème", "Impossible de se connecter à l'IP spécifiée. vérifier que votre ESP32 est bien allumé et configurer le fichier ip.txt")
            root.destroy()
            pass

    def led2_on(self):
        try:
            with open("ip.txt", "r") as f:
                ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                print(ip)
                delay = 2
                requests.get(f'http://{ip}/?LED1=ON',timeout=delay)
        except:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("petit problème", "Impossible de se connecter à l'IP spécifiée. vérifier que votre ESP32 est bien allumé et configurer le fichier ip.txt")
            root.destroy()
            pass

    def led2_off(self):
        try:
            with open("ip.txt", "r") as f:
                ip = f.read().strip()  # Strip any leading/trailing whitespaces or newline characters
                print(ip)
                delay = 2
                requests.get(f'http://{ip}/?LED1=OFF',timeout=delay)
        except:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("petit problème", "Impossible de se connecter à l'IP spécifiée. vérifier que votre ESP32 est bien allumé et configurer le fichier ip.txt")
            root.destroy()
            pass

    def hand_controle(self):
        try:
            from main_controller import run
            run()
        except:
            pass
        
    def save_text(self):
        text = self.ui.utilisateur_lineEdit.text() 
        with open("name.txt", "w") as f:
            f.write(text)
        msg = QMessageBox()
        msg.setText('Utilisateur enrégistré, Appuyer sur Start')
        msg.exec_()
        
    def save_ip(self):
        text = self.ui.lineEdit_2.text()
        try:
            with open("ip.txt", "w") as f:
                f.write(text)
            msg = QMessageBox()
            msg.setText('IP enregistrée avec succès')
            msg.exec_()
        except Exception as e:
            msg = QMessageBox()
            msg.setText("Problème lors de l'enregistrement de l'adresse IP : {}".format(e))
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
            self.connexion = ConnexionApp()
            self.connexion.show()
            # CLOSE SPLASH SCREEN
            self.close()
        # INCREASE COUNTER
        counter += 1
        
#page de connexion
class ConnexionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.connexion)

    def create_table(self):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

    def connexion(self):
        username = self.ui.lineEdit_2.text()
        password = self.ui.lineEdit.text()

        if len(username) == 0 or len(password) == 0:
            QMessageBox.information(self, "Erreur de saisie", "Veuillez remplir tous les champs.")
        else:
            self.create_table()

            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            query = 'SELECT password FROM users WHERE username = ?'
            cur.execute(query, (username,))
            result_pass = cur.fetchone()

            if result_pass and result_pass[0] == password:
                QMessageBox.information(self, "Connexion réussie", "Connexion réussie !")
                self.main = Main()
                self.main.show()
              
            else:
                QMessageBox.warning(self, "Erreur de connexion", "Nom d'utilisateur ou mot de passe incorrect.")

            conn.close()
            
app = QApplication(sys.argv)
Lanc = SplashScreen()
exit(app.exec_())
