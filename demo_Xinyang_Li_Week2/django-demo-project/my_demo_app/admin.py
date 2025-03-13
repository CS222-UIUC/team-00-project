# filepath: e:\cs222\team-00-project\demo_Xinyang_Li_Week2\django-demo-project\my_demo_app\admin.py
from django.contrib import admin
from .models import LoggedInUser

admin.site.register(LoggedInUser)