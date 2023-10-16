from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from MLnews.models import BotResponse
#from .forms import PostForm, ContactForm
from newspaper import Config
from newspaper import Article
from MLnews.pythonvit5.sum_txt import sum_txt, getAuthor, getDate, getKeyword, getTopimg, getTopvid
from MLnews.ChatbotCNN.chatbot import response

def chatbot(request):
    return render(request, 'Chatbot.html')

def home(request):
    #print(sum_txt(request.GET))
    return render(request, 'ML_index.html')

def finance(request):
    return render(request, 'Price.html')

def changecurr(request):
    return render(request, 'Change_currency.html')

def changegold(request):
    return render(request, 'Change_gold.html')

def changestock(request):
    return render(request, 'Change_stock.html')


def bot_response(request):
    if request.method == 'GET':
        print("bot content: ", request.GET['BotContent'])
        bot_content = BotResponse({'bot_res':request.GET['BotContent']})
        
        if bot_content.is_valid():
            return JsonResponse({'success': True,
                                 'bot_content': response(bot_content.cleaned_data['bot_res'])})
        else:
            return JsonResponse({'success': False,
                                 'bot_content': "",
                                 'errors': bot_content.errors})
        #obj = YourModel()
        #obj.sensor_name = bot_content.get("BotContent")
        # other fields
        #obj.save()
        # return or redirect
    else:
        bot_content = BotResponse()
    return render(request, 'Chatbot.html', {'bot_content': bot_content})