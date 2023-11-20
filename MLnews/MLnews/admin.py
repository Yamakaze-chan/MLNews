from django.contrib import admin
from .models import User
from .forms import Watch_later_info

admin.site.register(User)
admin.site.register(Watch_later_info)