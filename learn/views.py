import tkinter as tk

import os, sys, random

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from PIL import Image, ImageTk

from .models import Usercustom, Language, Word, Wordjp, Wordfr, Wordru, Progression, Theme, Quizz

from .forms import RegisterForm

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
    return render(request, 'learn/register_html.html', context)


def submit_form(request):

    """Unused. Too complicated because of the hidden field 'lang' !"""

    create_user = request.POST.get('create-user')
    lang = request.POST.get('lang')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    lang_dis = "English"

    form = RegisterForm(request.POST)

    if form.is_valid():
        pass


    if create_user:
        new_user = User.objects.create_user(username, email, password)
        language = Language.objects.get(NameEng=lang_dis)
        customu = Usercustom.objects.create(user=new_user, LangDisplay=language)
        #Create a progression in the selected language
        new_progression = Progression.objects.create(
            UserId=customu,
            LangId =language,
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



def submit_form_html(request):
    create_user = request.POST.get('create-user')
    lang = request.POST.get('lang')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    lang_dis = request.POST.get('lang-display')

    if create_user:
        new_user = User.objects.create_user(username, email, password)
        if lang == 'jp':
            language = Language.objects.get(NameEng='Japanese')
        elif lang == 'fr':
            language = Language.objects.get(NameEng='French')
        elif lang == 'ru':
            language = Language.objects.get(NameEng='Russian')

        #language = Language.objects.get(NameEng=lang)
        language_dis = Language.objects.get(NameEng=lang_dis)
        customu = Usercustom.objects.create(user=new_user, LangDisplay=language_dis)
        #Create a progression in the selected language
        new_progression = Progression.objects.create(
            UserId=customu,
            LangId =language,
            Level=0,
            Points=0,
            WordsLearnt=[0],
            Exelearnt=[0],
            FunFacts=[0]
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
    switch = request.POST.get('switch')
    prog_id = request.POST.get('progid')

    user = request.user
    custom_user = Usercustom.objects.get(user=user)

    if switch:
        old_progression = Progression.objects.get(UserId=custom_user, IsActive=True)
        if prog_id:
            new_progression = Progression.objects.get(id=prog_id)
            new_progression.IsActive = True
            new_progression.save()
        else:
            language = Language.objects.get(NameEng=lang)
            new_progression = Progression.objects.create(
                UserId=custom_user,
                LangId=language,
                Level=0,
                Points=0,
                WordsLearnt=[0],
                Exelearnt=[0],
                FunFacts=[0]
            )
        old_progression.IsActive = False
        old_progression.save()

    context = {
        'lang':lang,
    }
    return render(request, 'learn/home.html', context)




@login_required(login_url='/learn/')
def stats(request):
    user = request.user
    custom_user = Usercustom.objects.get(user=user)

    print('Recherche des prog pour user.Username, avec id:{0}'.format(custom_user.id))
    progressions = Progression.objects.filter(UserId=custom_user.id).order_by('IsActive').reverse()
    progressions_list = [prog for prog in progressions]

    languages = Language.objects.all()
    for language in languages:
        if language not in [prog.LangId for prog in progressions]:
            no_progression = {'LangId':language.NameEng,
                              }
            progressions_list.append(no_progression)

    for prog in progressions:
        print('Info sur la progression:')
        print(prog)
        print(prog.id)
        print(prog.UserId)

    context={
        'progressions':progressions_list
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

    lang_id = progression.LangId.id
    if lang_id == 1:
        lang = "jp"
    elif lang_id == 3:
        lang = "fr"
    elif lang_id == 4:
        lang = "ru"
    else:
        message ="Error. No language selected"


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
            elif lang == 'fr':
                try:
                    wrdfr = Wordfr.objects.filter(NameEng = wrd.id).get()
                    words_sublist.append(wrdfr)
                except:
                    print('The word {0} has no correspondant in {1}'.format(wrd,lang))
            elif lang == 'ru':
                try:
                    wrdru = Wordru.objects.filter(NameEng = wrd.id).get()
                    words_sublist.append(wrdru)
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


@login_required(login_url='/learn/')
def quizz(request):
    user = request.user
    custom_user = Usercustom.objects.get(user=user)
    progression = Progression.objects.get(UserId=custom_user, IsActive=True)
    langid = progression.LangId.id


    started = request.POST.get('started')
    launch = request.POST.get('launch')
    check = request.POST.get('check')

    if not started:
        context = {
            'lang': progression.LangId
        }
        return render(request, 'learn/quizz.html', context)

    #Check if a quizz is already started for the current progression

    if check:
        cur_word = request.POST.get('cur_word')
        response = request.POST.get('response')

        quizz = Quizz.objects.get(Progression=progression, State=1)

        if response == cur_word:
            message = 'Nice one !'
            quizz.Score +=10
        else:
            message = 'OOps, wrong answer.'

        quizz.save()

        context = {
            'lang': progression.LangId,
            'score': quizz.Score,
            'total': quizz.Total,
            'mode': quizz.Mode,
            'word_list': quizz.WordList,
            'cur_word': cur_word,
            #'responses': responses,
            'button': 'Next',
            'message': message
        }
        return render(request, 'learn/launch_quizz.html', context)

    #Start a quizz
    if launch :
        total = request.POST.get('number')
        if total:
            total = int(total)
        mode = request.POST.get('mode')

        if langid == 1 :
            word_list_total = [word for word in Wordjp.objects.all()]

        if langid == 3:
            word_list_total = [word for word in Wordfr.objects.all()]

        if langid == 4:
            word_list_total = [word for word in Wordru.objects.all()]

        word_list = []
        # word_list = random.choice(word_list, total)
        for i in range(0, total):
            ind = random.randint(0, len(word_list_total) - 1)
            word_list.append(word_list_total[ind])
            word_list_total.pop(ind)


        print('Inital word list :')
        print(word_list)

        quizz = Quizz.objects.create(
            Progression=progression,
            Score =0,
            WordList=[word.id for word in word_list],
            Total=total,
            Difficulty=1,
            Mode=mode,
            State=1
            )
        quizz.save()

    else:
        quizz = Quizz.objects.get(Progression=progression, State=1)

        #if langid == 1:
        #    word_list_total = [word for word in Wordjp.objects.all()]

        if langid == 3:
            word_list_total = [word for word in Wordfr.objects.all()]

        if langid == 4:
            word_list_total = [word for word in Wordru.objects.all()]

    if len(quizz.WordList) < 1:
        if quizz.Score >= quizz.Total*0.7:
            message = 'The quizz is completed. You scored {0}. Congratulations'.format(quizz.Score)
            progression.Points += 15
            progression.save()
        else:
            message = "The quizz is completed. You scored {0}. Keep practising and don't give up !".format(quizz.Score)
        quizz.State = 0
        quizz.save()

        context = {
            'lang': progression.LangId,
            'score': quizz.Score,
            'total': quizz.Total,
            'mode': quizz.Mode,
            'word_list': quizz.WordList,
            'message': message,
        }


    else:
        cur_word_id = quizz.WordList.pop(random.randint(0, len(quizz.WordList) - 1))
        if langid == 1:
            cur_word = Wordjp.objects.get(id=cur_word_id)
            word_list_total = [word for word in Wordjp.objects.exclude(id=cur_word_id)]

        if langid == 3:
            cur_word = Wordfr.objects.get(id=cur_word_id)

        if langid == 4:
            cur_word = Wordru.objects.get(id=cur_word_id)

        #word_list_total.pop(cur_word)


        responses = []
        for i in range(0, 3):
            # responses.append(cur_word)
            ind = random.randint(0, len(word_list_total) - 1)
            responses.append(word_list_total[ind])
        ind = random.randint(0, len(responses))
        responses.insert(ind, cur_word)

        if langid == 'French':
            responses = [word for word in Wordfr.objects.all()]
            responses.append(cur_word)
            responses = random.choice(word_list, 4)
        if langid == 'Russian':
            responses = [word for word in Wordru.objects.all()]
            responses.append(cur_word)
            responses = random.choice(word_list, 4)

        quizz.save()

        context = {
            'lang': progression.LangId,
            'score': quizz.Score,
            'total': quizz.Total,
            'mode': quizz.Mode,
            'word_list': quizz.WordList,
            'responses': responses,
            'button': 'Confirm',
            'cur_word': cur_word
        }

    return render(request, 'learn/launch_quizz.html', context)




"""
@login_required(login_url='/learn/')
def quizz(request):
    user = request.user
    custom_user = Usercustom.objects.get(user=user)
    progression = Progression.objects.get(UserId=custom_user, IsActive=True)
    lang = progression.LangId.NameEng

    started = request.POST.get('started')

    if not started:
        context = {
            'lang': lang
        }
        return render(request, 'learn/quizz.html', context)
    
    


    launch = request.POST.get('launch')
    check = request.POST.get('check')
    score = request.POST.get('score')
    total = request.POST.get('number')
    if total:
        total = int(total)
    end = request.POST.get('end')
    mode = request.POST.get('mode')
    word_list = request.POST.get('word_list')
    if word_list:
        word_list = word_list.split(',')
    responses = request.POST.get('responses')

    print('Nouvelle liste récupéreé')
    print(word_list)

    print('En mode liste')
    print(word_list)

    if check:
        cur_word = request.POST.get('cur_word')
        response = request.POST.get('response')


        if response == cur_word:
            message = 'Nice one !'
        else:
            message = 'OOps, wrong answer.'

        context = {
            'lang': lang,
            'score': score,
            'total': total,
            'mode': mode,
            'word_list': word_list,
            'cur_word': cur_word,
            'responses': responses,
            'button' : 'Next',
            'message' : message
        }
        return render(request, 'learn/launch_quizz.html', context)

    if end:
        user = request.user
        custom_user = Usercustom.objects.get(user=user)
        progression = Progression.objects.get(UserId=custom_user, IsActive=True)

        return render(request, 'learn/home.html')


    if launch:
        #num = request.POST.get('number')
        #mode = request.POST.get('mode')

    #Don't know what to do with this...
        class Quizz():

            def __init__(self, lg, md, nb):
                self.lg = lg
                self.md = md
                self.nb = nb
                self.score = 0
                self.word_list = []

                if lg == 'Japanese':
                    word_list = [word for word in Wordjp.objects.all()]
                    word_list = random.choice(word_list, self.nb)
                if lg == 'French':
                    word_list = [word for word in Wordfr.objects.all()]
                    word_list = random.choice(word_list, self.nb)
                if lg == 'Russian':
                    word_list = [word for word in Wordru.objects.all()]
                    word_list = random.choice(word_list, self.nb)

            def check_answer(self):
                return 'checked'
            def next_word(self):
                self.nb += 1
                return self.word_list[self.nb]
        
        new_quizz = Quizz(lang, mode, num)
        
    
        score = 0
        if lang == 'Japanese':
            word_list_total = [word for word in Wordjp.objects.all()]
            word_list = []
            #word_list = random.choice(word_list, total)
            for i in range(0,total):
                ind = random.randint(0,len(word_list_total)-1)
                word_list.append(word_list_total[ind])
                word_list_total.pop(ind)

        if lang == 'French':
            word_list = [word for word in Wordfr.objects.all()]
            word_list = random.choice(word_list, total)
        if lang == 'Russian':
            word_list = [word for word in Wordru.objects.all()]
            word_list = random.choice(word_list, total)
        print('Inital word list :')
        print(word_list)




    cur_word = word_list.pop(random.randint(0,total-1))



    if lang == 'Japanese':
        responses_total = word_list
        responses = []
        for i in range(0,3):
            #responses.append(cur_word)
            ind = random.randint(0,len(word_list)-1)
            responses.append(word_list[ind])
        ind = random.randint(0,len(responses))
        responses.insert(ind, cur_word)

    if lang == 'French':
        responses = [word for word in Wordfr.objects.all()]
        responses.append(cur_word)
        responses = random.choice(word_list, 4)
    if lang == 'Russian':
        responses = [word for word in Wordru.objects.all()]
        responses.append(cur_word)
        responses = random.choice(word_list, 4)

    print('Responses :')
    print(responses)


    context = {
        'lang': lang,
        'score': score,
        'total': total,
        'mode': mode,
        'word_list': word_list,
        'responses': responses,
        'button' : 'Confirm',
        'cur_word':cur_word
    }
    return render(request, 'learn/launch_quizz.html', context)
    """




