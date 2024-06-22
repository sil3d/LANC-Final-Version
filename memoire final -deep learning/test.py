import torch
from nltk_utils import tokenize, stem, bag_of_words, correct_spelling
from Neural_network import NeuralNet
import pyttsx3
import json
import random

# Charger les données et le modèle entraîné
data = torch.load("data.pth")
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state_dict = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state_dict)
model.eval()

with open ("intents.json",'r') as json_data:
    intents = json.load(json_data)

# Fonction pour obtenir la réponse à une question donnée
def get_response(question):
    sentence = question
    sentence = tokenize(sentence)
    sentence = [stem(token) for token in sentence]
    X = bag_of_words(sentence, all_words)
    X = X.reshape((1, X.shape[0]))
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return "Je suis désolé, je ne peux pas répondre à cette question pour le moment."

# Fonction pour faire parler l'IA
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

while True:
    # Exemple d'utilisation
    question = input("Posez une question : ")
    response = get_response(question)
    speak(response)