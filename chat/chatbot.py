import nltk
import random
import json
import pickle
import numpy as np

from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

# Inicializar lematizador
lemmatizer = WordNetLemmatizer()

# Cargar archivos necesarios
with open('intents.json') as file:
    intents_json = json.load(file)

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_simple_libro_model.h5')

# Preprocesamiento de entrada del usuario
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Convertir oración a bag-of-words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predecir la intención del usuario
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]

    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Obtener respuesta del chatbot
def get_response(intents_list, intents_json):
    list_of_intents = intents_json['intents']
    tag = intents_list[0]['intent']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

if __name__ == '__main__':
    print("The bot is running")
    while True:
        message = input("You: ")
        if message.lower() == "quit":
            print("Chatbot: Goodbye!")
            break

        intents = predict_class(message)
        response = get_response(intents, intents_json)
        print(f"Chatbot: {response}")

# # Iniciar el chatbot
# print("The bot is running")
# while True:
#     message = input("You: ")
#     if message.lower() == "quit":
#         print("Chatbot: Goodbye!")
#         break
#
#     intents = predict_class(message)
#     response = get_response(intents, intents_json)
#     print(f"Chatbot: {response}")