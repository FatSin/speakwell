from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'learn/index.html')

def home(request):

    lang = request.POST.get('lang')
    context = {
        'lang':lang
    }
    return render(request, 'learn/home.html', context)

def voc(request):

    lang = request.POST.get('lang')
    context = {
        'lang':lang
    }
    return render(request, 'learn/voc.html', context)