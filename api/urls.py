from django.urls import path
from . import views

app_name = 'BankApp'

urlpatterns = [
   path('', views.Home, name = 'home'),
   path('branch/autocomplete/', views.AutoComplete, name= 'autocomplete'),
   path('branch/', views.Branch, name = 'branch'),
   path('autosuggest/', views.AutoSuggest, name = 'autosuggest'),
   path('banktable/', views.BankTable, name = 'banktable'),
   path('bankdetail/<int:pk>/', views.BankDetail, name='detail')

]
