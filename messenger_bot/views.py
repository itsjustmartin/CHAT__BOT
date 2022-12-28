from django.shortcuts import render
from django.http.response import HttpResponse

def firstPage(request) :
    return HttpResponse('sorry..    try /bot')