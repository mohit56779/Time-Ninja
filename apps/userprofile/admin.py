# import django
from django.contrib import admin

# import models
from .models import Userprofile

# register 
admin.site.register(Userprofile)