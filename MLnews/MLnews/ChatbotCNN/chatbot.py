import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
import time
import webbrowser
import urllib.request
import urllib.parse 
from bs4 import BeautifulSoup
import requests
#from googlesearch import *
from nltk.stem import WordNetLemmatizer
from keras.models import load_model
from ..pythonvit5.sum_txt import sum_txt

lemmatizer = WordNetLemmatizer()
model = load_model('MLnews\ChatbotCNN\chatbot_model_VN')
intents = json.loads(open("MLnews\ChatbotCNN\intents_VN.json", "r", encoding='utf8').read())
words = pickle.load(open('MLnews\ChatbotCNN\words.pkl','rb'))
classes = pickle.load(open('MLnews\ChatbotCNN\classes.pkl','rb'))

#Predict
def clean_up(sentence):
    sentence_words=nltk.word_tokenize(sentence)
    sentence_words=[ lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def create_bow(sentence,words):
    sentence_words=clean_up(sentence)
    bag=list(np.zeros(len(words)))
    
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence,model):
    p=create_bow(sentence,words)
    res=model.predict(np.array([p]))[0]
    threshold=0.8
    results=[[i,r] for i,r in enumerate(res) if r>threshold]
    results.sort(key=lambda x: x[1],reverse=True)
    return_list=[]
    
    for result in results:
        return_list.append({'intent':classes[result[0]],'prob':str(result[1])})
    return return_list

def uri_validator(x):
    try:
        result = urllib.parse.urlparse(x)
        return result.scheme and result.netloc
    except:
        return False


def get_response(return_list,intents_json, user_text):
    print(return_list)
    if len(return_list)==0:
        if uri_validator(user_text):
            return user_text
        else:
            tag='noanswer'
    else:    
        tag=return_list[0]['intent']

    list_of_intents= intents_json['intents']    
    for i in list_of_intents:
        if tag==i['tag'] :
            return random.choice(i['responses'])
    return None

def response(text):
    return_list=predict_class(text,model)
    response=get_response(return_list,intents, text)
    #temp = sum_txt(text)
    return response
