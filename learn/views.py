import tkinter as tk

import os, sys

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageTk

from .models import Usercustom, Language, Word, Wordjp, Progression, Theme

from .record_streaming import main as rec
from .record_streaming import print_from_mp3

# Create your views here.

def index(request):
    return render(request, 'learn/index.html')

def register(request):
    lang = request.POST.get('lang')
    context = {
        'lang': lang
    }
    return render(request, 'learn/register.html', context)

def submit_form(request):
    create_user = request.POST.get('create-user')
    lang = request.POST.get('lang')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    lang_dis = "English"

    if create_user:
        new_user = User.objects.create_user(username, email, password)
        language = Language.objects.get(NameEng=lang_dis)
        customu = Usercustom.objects.create(user=new_user, LangDisplay=language)
        #Create a progression in the selected language
        new_progression = Progression.objects.create(
            UserId=customu.id,
            LangId =lang,
            Level=0,
            Points=0,
            WordsLearnt=0,
            Exelearnt=0,
            FunFacts=0
            )


    user = authenticate(username=username, password=password)

    if user is not None:
        message = "Authentication successful for user {0}".format(username)
        print(message)

        login(request, user)

        context = {
            'lang': lang,
            'message': message
        }

        return render(request, 'learn/home.html', context)

    else:
        message = "Authentication failed, please retry"
        context = {
            'message' : message
        }
        return render (request, 'learn/index.html', context)

def log_out(request):
    logout(request)
    return render(request, 'learn/index.html')

@login_required(login_url='/learn/')
def home(request):

    lang = request.POST.get('lang')
    context = {
        'lang':lang
    }
    return render(request, 'learn/home.html', context)

@login_required(login_url='/learn/')
def stats(request):
    user = request.user
    custom_user = Usercustom.objects.get(user=user)

    print('Recherche des prog pour user.Username, avec id:{0}'.format(custom_user.id))
    progressions = Progression.objects.filter(UserId=custom_user.id).all()

    for prog in progressions:
        print('Info sur la progression:')
        print(prog)
        print(prog.id)
        print(prog.UserId)

    context={
        'progressions':progressions
    }
    return render(request, 'learn/stats.html', context)

@login_required(login_url='/learn/')
def voc(request):
    lang = request.POST.get('lang')

    user = request.user
    custom_user = Usercustom.objects.get(user=user)

    message=''

    progression = Progression.objects.get(UserId=custom_user.id, IsActive=True)
    words_done = progression.WordsLearnt
    print('Liste des words acquis:')
    print(words_done)

    if lang is None:
        lang_id = progression.LangId.id
        if lang_id == 1:
            lang = "jp"
        else:
            message ="No language selected"


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
                try:
                    wrdjp = Wordjp.objects.filter(NameEng = wrd.id).get()
                    words_sublist.append(wrdjp)
                except:
                    print('The word {0} has no correspondant in {1}'.format(wrd,lang))
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
        'words_done': words_done,
        #'wordsen_list': wordsen_list
        'themes_list':themes_list,
        'message':message
    }
    return render(request, 'learn/voc.html', context)


    #return render(request, 'learn/voc.html')

@login_required(login_url='/learn/')
def record(request):
    #1) Record stream data from the mic, 2)evaluate it with Google Speech-to-text score and 3) graph it

    user = request.user
    custom_user = Usercustom.objects.get(user=user)
    lang = request.POST.get('lang')
    word_eng = request.POST.get('word_eng')
    word_hira = request.POST.get('word_hira')
    word_kanji = request.POST.get('word_kanji')

    filename = "learn/static/learn/fig/"+lang+"/"+word_eng+"-"+lang+".png"

    if not os.path.exists(filename):
        print('Graph not found for this audio file. Creating it')
        print_from_mp3(word_eng, lang)


    data = rec()


    score = data[1][:2]

    if (word_hira in data[0]) or (word_kanji in data[0]):
    #data[1] = 81 #Test
    #if word_in: #Test
        message = "Congratulations, you pronounced {0} for {1} with a score of {2}".format(word_hira, data[0], score)
        if int(score) >= 80:
            word_id = Wordjp.objects.get(NameHira=word_hira).id
            progression = Progression.objects.get(UserId=custom_user.id, LangId=1)

            if word_id not in progression.WordsLearnt:
                progression.WordsLearnt.append(word_id)
                progression.Points+=10
                progression.Level = progression.Points //100
                progression.save()

            print("ajout de l'id {0} à la liste. On obtient :".format(word_id))
            print(progression.WordsLearnt)
        elif int(score) >= 65:
            message = "You pronounced the word {0} with a score of {1}. You're almost there, Try again !".format(word_hira, score)
        else:
            message = "You pronounced the word {0} with a score of {1}. Don't beat yourself up and keep on listening the word.".format(word_hira, score)
    else:
        message = "Oops, you did not pronounce {0} well. Did you mean {1} ?".format(word_hira, data[0])



    class Winconfig:
        def __init__(self, wind):
            frame = tk.Frame(wind)
            frame.pack()

            fig_ref = Image.open("learn/static/learn/fig/"+lang+"/"+word_eng+"-"+lang+".png")
            fig_mic = Image.open("learn/static/learn/fig/testcloud.png")
            self.photo_ref = ImageTk.PhotoImage(fig_ref, master=wind)
            self.photo_mic = ImageTk.PhotoImage(fig_mic, master=wind)

            msg = tk.Message(wind, text=message)
            msg.pack()

            self.button = tk.Button(frame, text="OK", command=frame.quit)
            self.button.pack(side=tk.BOTTOM)

            canvas = tk.Canvas(wind, width=fig_ref.size[0]*2, height=fig_ref.size[1])
            canvas.create_image(0,0, anchor=tk.NW, image=self.photo_ref)
            canvas.create_image(fig_ref.size[0],0, anchor=tk.NW, image=self.photo_mic)
            #canvas.create_image(0, 0, image=self.photo_ref)
            canvas.pack()



    window = tk.Tk()
    launch_window = Winconfig(window)
    window.mainloop()
    window.destroy()

    # retry_butn = tk.button('Retry', 'target')
    # conf_butn = tk.button('OK', 'target')
    # window.flip()


    context = {
        #'word_result': data[0],
        #'word_in' : word_in,
        #'score': data[1],
        'message' : message,
    }

    #return render(request, 'learn/index.html')

    #return render(request, 'learn/voc.html', context)
    return voc(request)