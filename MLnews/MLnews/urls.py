"""
URL configuration for MLnews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MLnews.views import home, bot_response, finance, chatbot, changecurr, changegold, changestock, user_login, user_signup, user_logout, watch_later, Show_watch_later, Remove_watch_later, get_all_user, dashboard, get_all_user_info, del_user, sum_txt,update_info, update_user_info, get_user_info, password_change, password_reset,weather_forecast, user_signup_admin, modify_chatbot_json,get_chatbot_json

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('home', home),
    path('finance', finance),
    path('chatbot', chatbot),
    path('bot_response', bot_response, name='bot_response'),
    path('Change_currency', changecurr, name='Change_currency'),
    path('Change_gold', changegold, name='Change_gold'),
    path('Change_stock', changestock, name='Change_stock'),
    path('login', user_login, name='login'),
    path('signup', user_signup, name='signup'),
    path('signup_admin', user_signup_admin, name='signup_admin'),
    path('logout', user_logout, name='logout'),
    path('watch_later', watch_later, name='watch_later'),
    path('show_watch_later', Show_watch_later, name='show_watch_later'),
    path('remove_watch_later', Remove_watch_later, name='remove_watch_later'),
    path('dashboard', dashboard, name='dashboard'),
    path('get_all_user_info', get_all_user_info, name='get_all_user_info'),
    path('get_user_admin', get_all_user, name='get_user_admin'),
    path('del_user', del_user, name='del_user'),
    path('sum_text', sum_txt, name='sum_text'),
    path('update_info', update_info, name='update_info'),
    path('update_user_info', update_user_info, name='update_user_info'),
    path('get_user_info', get_user_info, name='get_user_info'),
    path("password_change", password_change, name="password_change"),
    path("password_reset", password_reset, name="password_reset"),
    path("weather_forecast", weather_forecast, name="weather_forecast"),
    path("modify_chatbot_json", modify_chatbot_json, name="modify_chatbot_json"),
    path("get_chatbot_json", get_chatbot_json, name="get_chatbot_json"),
]
