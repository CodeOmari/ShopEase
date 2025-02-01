from django.contrib import admin
from django.contrib.auth.models import User

from main_app.models import Customer, Transaction

# Register your models here.

admin.site.site_header = 'ShopEase Administration'

admin.site.site_title = 'ShopEase Administration'

admin.site.register(Customer)
admin.site.register(Transaction)