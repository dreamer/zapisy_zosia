from django.shortcuts import render_to_response, HttpResponse
from django.http import HttpResponseRedirect

def login(request):
    #login(request)
    return HttpResponseRedirect('/blog/')

def logout(request):
    #logout(request)
    return HttpResponseRedirect('/blog/')

