from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import cache_page
from django.http import JsonResponse,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BankAppSerializer
from collections import defaultdict
from .models import BankParam
import json

# Create your views here.

total = len(BankParam.objects.all())


def Pagination(page):
   if page == None:
       return 0
   return int(page)

def Next(val):
    if val + 1 < total/10:
       val = val + 1
    else:
       val = total//10
    return val

def Previous(val):
    if not val - 1 < 0:
        val = val - 1
    return val


def LimitOffsetwithBank(request):
    q = request.GET.get("q")
    if q != None:
        result = list(BankParam.objects.filter(ifsc__icontains=q)) + list(BankParam.objects.filter(bank_id__icontains=q)) + list(BankParam.objects.filter(branch__icontains=q)) + list(BankParam.objects.filter(address__icontains=q)) + list(BankParam.objects.filter(city__icontains=q)) + list(BankParam.objects.filter(district__icontains=q)) + list(BankParam.objects.filter(state__icontains=q)) + list(BankParam.objects.filter(bank_name__icontains=q))
        return result[:10]
    else:
        return BankParam.objects.filter(bank_name__icontains="a")

def AutoSuggest(request):
    searchIt = request.GET.get("term")
    searchedResult = BankParam.objects.filter(branch__icontains = searchIt)
    result = [i.branch for i in searchedResult[:100]]
    return JsonResponse(result, safe=False)

@api_view(['GET'])
def BankTable(request):
    page = Pagination(request.GET.get("page"))
    if page > total:
        return Response('No page available!')
    list = BankParam.objects.all()[page*10:page*10+10]
    next = Next(page)
    previous = Previous(page)
    serializer = BankAppSerializer(list, many = True)
    dataJSON = json.dumps(serializer.data)
    context = {
     'data' : dataJSON,
     'list' : list,
     'next' : next,
     'previous' :previous,
    }
    return render(request, 'BankApp/banktable.html', context)


@api_view(['GET'])
@cache_page(60 * 60)
def Home(request):
    context = {
     'Welcome' : 'Welcome to the Home Page of API application. Down below are the end points for this app',
    'To search the bank detail by any of the fields' : '/branch/',
    'To search with branch name autosuggestion' : '/branch/autocomplete/',
    'To see all the bank list' : '/banktable/',
    'To directly see the bank detail (if you have a bank id)' : '/bankdetail/bankID/'
    }
    return Response(context)

@api_view(['GET'])
def Branch(request):
    display = []
    limit = request.GET.get("limit")
    offset = request.GET.get("offset")
    branch = LimitOffsetwithBank(request)
    if (limit == offset == None) or (limit == offset == ''):
        limit, offset = 10, 1
    elif (limit == None or limit == '') and (offset != None or offset != ''):
        limit = 1
    elif (limit != None or limit != '') and (offset == None or offset == ''):
        offset = 1
    for item in branch[int(offset)-1:int(offset)+int(limit)-1]:
        display.append(item)
    if request.GET.get("q") == None:
        return render(request, "BankApp/display.html")
    else:
        serializer = BankAppSerializer(display, many = True)
        return Response(serializer.data)


def AutoComplete(request):
    return render(request, "BankApp/autocomplete.html")

@cache_page(60 * 60)
@api_view(['GET'])
def BankDetail(request, pk):
    if pk > total:
        return Response('No branch available for this ID')
    bank = get_object_or_404(BankParam, pk=pk)
    return render(request, 'BankApp/bankdetail.html', {'detail' : bank})
