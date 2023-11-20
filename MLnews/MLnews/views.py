from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from MLnews.models import BotResponse
from MLnews.pythonvit5.sum_txt import sum_txt, getAuthor, getDate, getKeyword, getTopimg, getTopvid
from MLnews.ChatbotCNN.chatbot import response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout 
from MLnews.forms import LoginForm, RegisterForm, Watch_later
import datetime

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


# Create your views here.

# signup page
def user_signup(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'signup.html', {'form': form})   
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return render(request, 'ML_index.html')
        else:
            return render(request, 'signup.html', {'form': form}) 

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print("login GET: ", request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return render(request, 'ML_index.html')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return render(request, 'ML_index.html')

# Watch later
def watch_later(request):
    if request.method == "POST":
        print(request.POST)
        form = Watch_later({'title': request.POST.get('title'),
                            'guid': request.POST.get('guid'),
                            'image': request.POST.get('image'),
                            'image_content': request.POST.get('image_content'),
                            'published_date': datetime.datetime.strptime(request.POST.get('published_date'),"%H:%M %d/%m/%Y"),
                            'save_account': request.user})
        print(form)
        if form.is_valid():
            #form.save()
            return JsonResponse({'success': True})
    return render(request, 'ML_index.html')