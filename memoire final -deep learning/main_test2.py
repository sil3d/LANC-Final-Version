import speech_recognition as sr
import pyttsx3
import json
import torch
from nltk_utils import bag_of_words, tokenize, stem
from Neural_network import NeuralNet

# Charger le modèle de chat
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

# Créer le modèle de chat
model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

# Initialiser le moteur de synthèse vocale pyttsx3
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Fonction pour répondre à une question
def chat(question):
    # Convertir la question en un sac de mots
    question = tokenize(question)
    X = bag_of_words(question, all_words)
    X = X.reshape(1, X.shape[0])

    # Faire la prédiction
    X = torch.from_numpy(X).to(torch.float32)
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    # Trouver la réponse dans les intents
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            response = random.choice(intent["responses"])
            speak(response)
            break

if __name__ == "__main__":
    recognizer = sr.Recognizer()

    with open('intents.json', 'r') as f:
        intents = json.load(f)

    print("Bonjour ! Posez une question vocalement ou tapez 'exit' pour quitter.")
    while True:
        with sr.Microphone() as source:
            print("Vous: (Dites votre question)")
            audio = recognizer.listen(source)

        try:
            user_input = recognizer.recognize_google(audio, language='fr-FR')
            print("Vous (reconnu):", user_input)
            if user_input.lower() == "exit":
                break
            else:
                chat(user_input)
        except sr.UnknownValueError:
            print("Désolé, je n'ai pas compris ce que vous avez dit.")
        except sr.RequestError as e:
            print("Erreur lors de la demande de reconnaissance vocale ; {0}".format(e))
