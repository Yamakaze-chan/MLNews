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
from MLnews.views import home, bot_response, finance, chatbot, changecurr, changegold, changestock, user_login, user_signup, user_logout, watch_later

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
    path('login/', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('watch_later/', watch_later, name='watch_later')
]
