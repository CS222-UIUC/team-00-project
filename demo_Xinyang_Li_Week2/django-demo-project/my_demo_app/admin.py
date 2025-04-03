from django.contrib import admin
from .models import LoggedInUser, UserTextData

admin.site.register(LoggedInUser)
admin.site.register(UserTextData)
