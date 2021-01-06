from django.contrib import admin
from .models import BankParam
# Register your models here.
@admin.register(BankParam)
class BankParamAdmin(admin.ModelAdmin):
    list_display = ['id', 'ifsc', 'bank_name', 'state']
