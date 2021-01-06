from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page


def Index(request):
    return render(request, 'index.html')


@cache_page(60 * 60)
@api_view(['GET'])
def Home(request):
    context = {
      'Welcome' : 'Welcome to the Home Page. Down below are the end points for this app',
      'API application' : '/api/',
      'To search the bank detail by any of the fields' : '/api/branch/',
      'To search with branch name autosuggestion' : '/api/branch/autocomplete/',
      'To see all the bank list' : '/api/banktable/',
      'To directly see the bank detail (if you have a bank id)' : '/api/bankdetail/bankID/'
    }
    return Response(context)
