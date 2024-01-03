from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import json
from MLnews.models import BotResponse
from MLnews.pythonvit5.sum_txt import sum_txt, getAuthor, getDate, getKeyword, getTopimg, getTopvid
from MLnews.ChatbotCNN.chatbot import response
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout 
from MLnews.forms import LoginForm, RegisterForm, Watch_later, User_info, Watch_user_info
from .forms import SetPasswordForm
from django.contrib.auth import password_validation
import datetime
import sqlite3
from sqlite3 import Error
from newspaper import Config
from newspaper import Article
import requests

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

def update_info(request):
    return render(request, 'update_info.html')

def weather_forecast(request):
    return render(request, 'plot_weather.html')


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
        print(request.POST)
        if form.is_valid():
            name = request.POST.get("username").lower()
            user = form.save(commit=False)
            user.username = request.POST.get("username").lower()
            user.first_name = request.POST.get("username").lower()
            user.is_staff = False if request.POST.get("is_staff")==None else True
            user.is_admin = False if request.POST.get("is_staff")==None else True
            user.is_superuser = False if request.POST.get("is_staff")==None else True
            user.save()
            sqliteConnection = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
            cursor = sqliteConnection.cursor()
            sql_delete_query = "INSERT INTO 'MLnews_user_info' (username, first_name, last_name, email, phone, address ) VALUES (\'" + str(user.id)+"\', \'"+ name+"\','','','','')"
            cursor.execute(sql_delete_query)
            sqliteConnection.commit()
            cursor.close()
            login(request, user)
            return render(request, 'ML_index.html')
        else:
            return render(request, 'signup.html', {'form': form}) 

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return render(request, 'ML_index.html')
            else:
                return render(request, 'login.html', {'error': "Tài khoản hoặc mật khẩu không đúng",
                                                      'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return render(request, 'ML_index.html')

def user_signup_admin(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        print(request.POST)
        if form.is_valid():
            name = request.POST.get("username").lower()
            user = form.save(commit=False)
            user.username = request.POST.get("username").lower()
            user.first_name = request.POST.get("username").lower()
            user.is_staff = False if request.POST.get("is_staff")==None else True
            user.is_admin = False if request.POST.get("is_staff")==None else True
            user.is_superuser = False if request.POST.get("is_staff")==None else True
            user.save()
            sqliteConnection = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
            cursor = sqliteConnection.cursor()
            sql_delete_query = "INSERT INTO 'MLnews_user_info' (username, first_name, last_name, email, phone, address ) VALUES (\'" + str(user.id)+"\', \'"+ name+"\','','','','')"
            cursor.execute(sql_delete_query)
            sqliteConnection.commit()
            cursor.close()
            return JsonResponse({"success":"Tạo tài khoản thành công"})
        else:
            print(form.errors)
            return JsonResponse(form.errors)

# Watch later
def watch_later(request):
    if request.method == "POST":
        conn = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
        guid = str(request.POST.get('guid'))
        print((guid))
        cur = conn.cursor()
        cur.execute("SELECT * FROM 'MLnews_watch_later_info' WHERE save_account_id=" + str(request.user.id) +" AND guid =\"" + guid + "\"")
        rows = cur.fetchall()
        if(len(rows) == 0):
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
        conn.close()
    return render(request, 'ML_index.html')

def Show_watch_later(request):
    if request.method == "GET":
        conn = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT * FROM 'MLnews_watch_later_info' WHERE save_account_id=" + str(request.user.id))
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
            sql_delete_query = "DELETE from 'MLnews_watch_later_info' where guid = \'" + str(guid) + "\' AND save_account_id=" + str(request.user.id)
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
                              'Last login': i['last_login'].strftime("%m/%d/%Y, %H:%M:%S") if i['last_login']!=None else "Chưa đăng nhập", 
                              'admin':i['is_staff']}))
        return JsonResponse({'all_user': json.dumps(list_user)})

def del_user(request):    
    if request.method == "GET":
        username = request.GET.get('username')
        try:
            u = User.objects.get(username = username)
            u.delete()
        except User.DoesNotExist:
            return JsonResponse({'err': "User not found"})

        except Exception as e: 
            return JsonResponse({'err': e})

        return render(request, 'Get_all_user_info.html')
    
def sum_txt(request):
    if request.method == "GET":
        url = request.GET.get('url')
        USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' #Change yours
        config = Config()
        config.browser_user_agent = USER_AGENT
        config.request_timeout = 10
        article = Article(url, config=config)
        article.download()
        article.parse()
        # the replace is used to remove newlines
        article_text = article.text.replace('\n', ' ')
        #print(article_text)
        return JsonResponse({"sum_text":article_text})
    return JsonResponse({"sum_text":""})

def update_user_info(request):
    if request.method == "POST":
        f_name = request.POST.get("firstname")
        l_name = request.POST.get("lastname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        uid = request.POST.get("uid")
        u = User.objects.get(id = uid)
        u.first_name = f_name
        u.last_name = l_name
        u.email = email
        try:
            sqliteConnection = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")

            # Deleting single record now
            sql_delete_query = "UPDATE 'MLnews_user_info' SET first_name = \'" + f_name + "\' , last_name=\'" + l_name + "\' , email = \'"+email+"\' , phone=\'" + phone + "\' , address=\'"+address+"\', username=\'"+str(uid)+"\'"
            cursor.execute(sql_delete_query)
            sqliteConnection.commit()
            cursor.close()
            if sqliteConnection:
                sqliteConnection.close()
            return JsonResponse({"error": None})
        except:
        #print(article_text)
            return JsonResponse({"error": "Something went wrong with database"})
    return render(request, 'update_info.html')

def get_user_info(request):
    if request.method == "POST":
        try:
            uid = request.POST.get("uid")
            sqliteConnection = sqlite3.connect(r"C:\Users\ACER\AI\sum_txt\MLnews\db.sqlite3")
            cursor = sqliteConnection.cursor()
            print("Connected to SQLite")
            print(uid)
            # Deleting single record now
            sql_delete_query = "SELECT * FROM 'MLnews_user_info' WHERE username=\'"+str(uid)+"\'"
            cursor.execute(sql_delete_query)
            rows = cursor.fetchall()
            sqliteConnection.commit()
            cursor.close()
            if sqliteConnection:
                sqliteConnection.close()
            return JsonResponse({"error": None,
                                 "data":rows})
        except:
        #print(article_text)
            return JsonResponse({"error": "Something went wrong with database"})
    return render(request, 'update_info.html')

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            print(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                return render(request, 'change_password.html', {'form': form}) 

    form = SetPasswordForm(user)
    return render(request, 'change_password.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        print(request.POST)
        try:
            user = User.objects.get(username=request.POST.get("username"))
        except:
            return render(request, 'reset_password.html', {'error': 'Not found this user'})
        else:
            try:
                password_validation.validate_password(request.POST.get('password'))
            except Exception as e:
                return render(request, 'reset_password.html', {'error': e})
            if (request.POST.get('password') == request.POST.get('confirmpassword')):
                user.set_password(request.POST.get("password"))
                user.save()
            else: 
                return render(request, 'reset_password.html', {'error': 'Mật khẩu không trùng khớp'})
        return redirect('login')
    return render(request, 'reset_password.html')

def modify_chatbot_json(request):
    print(request)
    if request.method == 'POST':
        print(request.POST['json_data'])
        try:
            string_json = json.loads(request.POST['json_data'])
            with open("MLnews\ChatbotCNN\intents_VN.json", "w", encoding='utf8') as outfile:
                outfile.write(json.dumps(string_json,indent=4, ensure_ascii=False))
            
                #print(json.loads(request.POST['json_data']))
        except:
            return JsonResponse({"error": "Có lỗi trong quá trình thay đổi chatbot"})
    return HttpResponse(open("MLnews\ChatbotCNN\intents_VN.json", "r", encoding='utf8'),content_type = 'application/json; charset=utf8')
        
def get_chatbot_json(request):
    return render(request, 'modify_chatbot.html')
        