from django.shortcuts import render

from .models import User, Language, Word, Wordjp, Progression, Theme


from .record_streaming import main as rec

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
    #wordsen_list = []
    words_list = []
    #words_sublist = []

    #if lang == 'jp':
    #    words_list = [ wrd for wrd in Wordjp.objects.all() ]

    themes_list = [thm for thm in Theme.objects.all() ]


    for thm in themes_list:
        words_sublist = []
        for wrd in thm.words.all():
            if lang == 'jp':
                wrdjp = Wordjp.objects.filter(NameEng = wrd.id).get()
                words_sublist.append(wrdjp)
            #words_list = [thm.NameEng, words_sublist]
        words_list.append([thm.NameEng, words_sublist])


    #wordsen_list = [ wrd.NameEng.NameEng for wrd in words_list ]

        #for wordjp in words_list:
        #    word_en = wordjp.NameEng.NameEng
        #    wordsen_list.append(word_en)
        #worden_list = [NameEng

        #words_list = [wrd for wrd in ]


    context = {
        'lang':lang,
        'words_list':words_list,
        #'wordsen_list': wordsen_list
        'themes_list':themes_list
    }
    return render(request, 'learn/voc.html', context)


    #return render(request, 'learn/voc.html')


def record(request):
    data = rec()
    word_in = request.POST.get('word_in')

    if word_in in data[0]:
        message = "Congratulations, you pronounced {0} for {1} with a score of {2}".format(word_in, data[0], data[1])
    else:
        message = "Oops, you did not pronounce {0} well. Did you mean {1} ?".format(word_in, data[0])

    context = {
        #'word_result': data[0],
        #'word_in' : word_in,
        #'score': data[1],
        'message' : message,
    }

    #return render(request, 'learn/index.html')

    return render(request, 'learn/index.html', context)