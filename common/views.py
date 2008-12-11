from django.shortcuts import render_to_response, HttpResponse

def login(request):
    #login(request)
    return HttpResponseRedirect('/blog/')

def logout(request):
    #logout(request)
    return HttpResponseRedirect('/blog/')

