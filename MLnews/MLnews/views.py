from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json
from MLnews.models import BotResponse
from MLnews.pythonvit5.sum_txt import sum_txt, getAuthor, getDate, getKeyword, getTopimg, getTopvid
from MLnews.ChatbotCNN.chatbot import response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout 
from MLnews.forms import LoginForm, RegisterForm, Watch_later
import datetime
import sqlite3
from sqlite3 import Error

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

def dashboard(request):
    return render(request, 'dashboard.html')

def get_all_user_info(request):
    return render(request, 'Get_all_user_info.html')


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
        #print(request.POST)
        form = Watch_later({'title': request.POST.get('title'),
                            'guid': request.POST.get('guid'),
                            'image': request.POST.get('image'),
                            'image_content': request.POST.get('image_content'),
                            'published_date': datetime.datetime.strptime(request.POST.get('published_date'),"%H:%M %d/%m/%Y"),
                            'save_account': request.user})
        #print(form)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    return render(request, 'ML_index.html')

def Show_watch_later(request):
    if request.method == "GET":
        conn = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT * FROM 'MLnews_watch_later_info'")
        return_JSON = []
        rows = cur.fetchall()

        #0: id
        #1: title
        #2: guid
        #3: image
        #4: image_content
        #5: published_date
        #6: save_account_id

        for row in rows:
            row_data=[]
            for i in range (len(row)):
                row_data.append(row[i])

            data_val = "{\"title\":\""+ str(row_data[1])+"\", \"guid\":\""+ str(row_data[2])+"\", \"image\":\""+ str(row_data[3])+"\", \"image_content\":\""+ str(row_data[4])+"\", \"publised_date\":\""+ str(row_data[5])+"\", \"save_account_id\":"+ str(row_data[6])+"}"
            return_JSON.append(data_val)
        return_JSON = json.dumps(return_JSON, ensure_ascii=False)
        #print(return_JSON)
        conn.close()
        return render(request, 'Watch_later.html', {'JSONs': return_JSON}) 
    return render(request, 'ML_index.html')

def Remove_watch_later(request):
    if request.method == "GET":
        guid = request.GET.get('guid')
        try:
            sqliteConnection = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            # Deleting single record now
            sql_delete_query = "DELETE from 'MLnews_watch_later_info' where guid = \'" + str(guid) + "\'"
            cursor.execute(sql_delete_query)
            sqliteConnection.commit()
            print("Record deleted successfully ")
            cursor.close()
            if sqliteConnection:
                sqliteConnection.close()
            return JsonResponse({'success': True})

        except sqlite3.Error as error:
            if sqliteConnection:
                sqliteConnection.close()
            print("Failed to delete record from sqlite table", error)
            return JsonResponse({'success': False})
    return 

def get_all_user(request):
    if request.method == "GET":
        User = get_user_model()
        all_users = User.objects.values()
        list_user = []
        for i in all_users:
            list_user.append(json.dumps({'id':i['id'], 
                              'username':i['username'], 
                              'First name': i['first_name'], 
                              'Last name': i['last_name'], 
                              'Last login': i['last_login'].strftime("%m/%d/%Y, %H:%M:%S"), 
                              'admin':i['is_staff']}))
        return JsonResponse({'all_user': json.dumps(list_user)})

def del_user(request):    
    if request.method == "GET":
        username = request.GET.get('username')
        print(username)
        try:
            u = User.objects.get(username = username)
            u.delete()
        except User.DoesNotExist:
            return JsonResponse({'err': "User not found"})

        except Exception as e: 
            return JsonResponse({'err': e})

        return render(request, 'Get_all_user_info.html')
        