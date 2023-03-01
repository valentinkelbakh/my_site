from django.contrib import admin

# Register your models here.
from .models import Entry, Category,Topic,Comment,Booking

for each in (Entry, Category,Topic,Comment,Booking):
    admin.site.register(each)
