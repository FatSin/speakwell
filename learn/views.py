import os, sys, random, json

from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

#from PIL import Image, ImageTk

from .models import Usercustom, Language, Word, Wordjp, Wordfr, Wordru, Progression, Theme, Quizz

from .forms import RegisterForm

from .record_streaming import main as rec
from .record_streaming import recognition_from_file as recfile
from .record_streaming import print_from_mp3

# Create your views here.
def testaudiojs(request):
    return render(request, 'learn/testaudiojs.html')



def index(request):
    user = request.user
    if user.is_authenticated:
        return home(request)
    return render(request, 'learn/index.html')

def register(request):
    lang = request.POST.get('lang')
    context = {
        'lang': lang
    }
    return render(request, 'learn/register_html.html', context)

"""
def submit_form(request):

    #Unused. Too complicated because of the hidden field 'lang' !

    create_user = request.POST.get('create-user')
    lang = request.POST.get('lang')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    lang_dis = "English"

    if lang:
        if lang == 'jp':
            lang = 'Japanese'
        if lang == 'fr':
            lang = 'French'
        if lang == 'ru':
            lang = 'Russian'


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
"""


def submit_form_html(request):
    create_user = request.POST.get('create-user')
    lang = request.POST.get('lang')
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    lang_dis = request.POST.get('lang-display')

    if create_user:
        check_user = User.objects.filter(username=username).count()
        if check_user > 0:
            message = "User {0} already exists.".format(username)
            context = {
                'message': message
            }
            return render(request, 'learn/index.html', context)
        else:
            new_user = User.objects.create_user(username, email, password)
            language = Language.objects.get(NameEng=lang)

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
            'lang': lang
        }

        return home(request)

    else:
        message = "Authentication failed, please retry"
        context = {
            'message' : message
        }
        return render (request, 'learn/index.html', context)

def log_out(request):
    logout(request)
    return render(request, 'learn/index.html')
    #return index(request)

@login_required(login_url='/learn/')
def home(request):

    #lang = request.POST.get('lang')
    switch = request.POST.get('switch')
    prog_id = request.POST.get('progid')

    user = request.user
    custom_user = Usercustom.objects.get(user=user)

    old_progression = Progression.objects.get(UserId=custom_user.id, IsActive=True)
    lang = old_progression.LangId
    message = ''

    if switch:
        #old_progression = Progression.objects.get(UserId=custom_user, IsActive=True)
        if prog_id:
            new_progression = Progression.objects.get(id=prog_id)
            new_progression.IsActive = True
            new_progression.save()
            old_progression.IsActive = False
            old_progression.save()
        else:
            #Rule : Level 2 for 2 progressions, level 5 for 3 progressions
            nb_prog = Progression.objects.filter(UserId=custom_user.id).count()
            if (nb_prog == 1 and old_progression.Level < 2) or (nb_prog > 1 and old_progression.Level < 5):
                message = "Oops, yu can't do that ! You must reach level 2 to activate a second language, and level 5 to activate a third language."
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
        'message':message
    }
    return render(request, 'learn/home.html', context)




@login_required(login_url='/learn/')
def stats(request):
    user = request.user
    custom_user = Usercustom.objects.get(user=user)
    progression=Progression.objects.get(UserId=custom_user, IsActive=True)
    lang=progression.LangId

    print('Recherche des prog pour user.Username, avec id:{0}'.format(custom_user.id))
    progressions = Progression.objects.filter(UserId=custom_user.id).order_by('IsActive').reverse()
    progressions_list = [prog for prog in progressions]

    languages = Language.objects.exclude(NameEng="English")
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
        'progressions':progressions_list,
        'lang':lang
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
        lang = "Japanese"
    elif lang_id == 3:
        lang = "French"
    elif lang_id == 4:
        lang = "Russian"
    else:
        message ="Error. No language selected"


    #wordsen_list = []
    words_list = []
    #words_sublist = []

    #if lang == 'jp':
    #    words_list = [ wrd for wrd in Wordjp.objects.all() ]

    themes_list = [thm for thm in Theme.objects.filter(IsEnabled=True)]


    for thm in themes_list:
        words_sublist = []
        for wrd in thm.words.all():
            if lang == 'Japanese':
                try:
                    wrdjp = Wordjp.objects.filter(NameEng = wrd.id).get()
                    words_sublist.append(wrdjp)
                except:
                    print('The word {0} has no correspondant in {1}'.format(wrd,lang))
            elif lang == 'French':
                try:
                    wrdfr = Wordfr.objects.filter(NameEng = wrd.id).get()
                    words_sublist.append(wrdfr)
                except:
                    print('The word {0} has no correspondant in {1}'.format(wrd,lang))
            elif lang == 'Russian':
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
    print(str(request.body))
    resp = request.body.decode().split(',')
    print(resp)
    word_eng = resp[0]
    lang = resp[1]

    #lang = request.POST.get('lang')
    #word_eng = request.POST.get('word_eng')
    #word_hira = request.POST.get('word_hira')
    #word_kanji = request.POST.get('word_kanji')

    print(lang)
    print(word_eng)
    print(user)
    print(request.POST)
    print(request.body)



    filename = "learn/media/learn/fig/"+lang+"/"+word_eng+"-"+lang+".png"
    audio_file = "learn/media/learn/audio/user.mp3"

    if not os.path.exists(filename):
        print('Graph not found for this audio file. Creating it')
        print_from_mp3(word_eng, lang, False)

    print_from_mp3(word_eng, lang, True)

    if lang == 'jp':
        lang_code = Language.objects.get(NameEng='Japanese').Code
    if lang == 'fr':
        lang_code = Language.objects.get(NameEng='French').Code
    if lang == 'ru':
        lang_code = Language.objects.get(NameEng='Russian').Code

    data = recfile(audio_file, lang_code)
    print(data)
    #data = rec()
    if data is None:
        html_response = """
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Title</title>
                </head>
                <body>
                <br><br><br>
                <p style="text-align:center;font-size:x-large;color:black;">Oops, I could not hear you.</p>
                <br>
                <p style="text-align:center;font-size:x-large;">
                    <a href="/learn/voc/" style="color:black;">Back</a>
                </p>
                </body>
                </html>
                """
    else:
        score = data[1][:2]

        if lang == 'jp':
            word_hira = resp[2]
            word_kanji = resp[3]
            if (word_hira in data[0]) or (word_kanji in data[0]):
            #data[1] = 81 #Test
            #if word_in: #Test
                message = "Congratulations, you pronounced {0} with a score of {1}%".format(word_hira, score)
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

        if lang == 'fr':
            word_fr = resp[2]
            if (word_fr in data[0]):
                message = "Congratulations, you pronounced {0} with a score of {1}%".format(word_fr, score)
                if int(score) >= 80:
                    word_id = Wordfr.objects.get(Name=word_fr).id
                    progression = Progression.objects.get(UserId=custom_user.id, LangId=3)

                    if word_id not in progression.WordsLearnt:
                        progression.WordsLearnt.append(word_id)
                        progression.Points+=10
                        progression.Level = progression.Points //100
                        progression.save()

                    print("ajout de l'id {0} à la liste. On obtient :".format(word_id))
                    print(progression.WordsLearnt)
                elif int(score) >= 65:
                    message = "You pronounced the word {0} with a score of {1}. You're almost there, Try again !".format(word_fr, score)
                else:
                    message = "You pronounced the word {0} with a score of {1}. Don't beat yourself up and keep on listening the word.".format(word_fr, score)
            else:
                message = "Oops, you did not pronounce {0} well. Did you mean {1} ?".format(word_fr, data[0])

        if lang == 'ru':
            word_ru = resp[2]
            word_roma = resp[3]
            if (word_ru in data[0]) or (word_roma in data[0]):
            #data[1] = 81 #Test
            #if word_in: #Test
                message = "Congratulations, you pronounced {0} with a score of {1}%".format(word_ru,score)
                if int(score) >= 80:
                    word_id = Wordru.objects.get(NameRu=word_ru).id
                    progression = Progression.objects.get(UserId=custom_user.id, LangId=4)

                    if word_id not in progression.WordsLearnt:
                        progression.WordsLearnt.append(word_id)
                        progression.Points+=10
                        progression.Level = progression.Points //100
                        progression.save()

                    print("ajout de l'id {0} à la liste. On obtient :".format(word_id))
                    print(progression.WordsLearnt)
                elif int(score) >= 65:
                    message = "You pronounced the word {0} with a score of {1}. You're almost there, Try again !".format(word_ru, score)
                else:
                    message = "You pronounced the word {0} with a score of {1}. Don't beat yourself up and keep on listening the word.".format(word_ru, score)
            else:
                message = "Oops, you did not pronounce {0} well. Did you mean {1} ?".format(word_ru, data[0])


        #img_ref_link = "learn/fig/"+lang+"/"+word_eng+"-"+lang+".png"
        #img_user_link = "learn/static/learn/fig/user.png"
        img_ref_link = "/learn/media/learn/fig/" + lang + "/" + word_eng + "-" + lang + ".png"
        img_user_link = "/learn/media/learn/fig/user.png"


        """"
        context = {
            'message' : message,
            'img_ref_link': img_ref_link,
            'img_user_link': img_user_link
        }
        return render(request, 'learn/evaluate.html', context)
        """

        """
        with open("learn/templates/evaluate.html", 'r+') as f:
            #print(request.body)
            html_response= ""
            for line in f:
                html_response = html_response + line
    
        """
        html_response = """
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Title</title>
            </head>
            <body>
            
            <p style="text-align:center;font-size:x-large;">"""+message+"""
            </p>
            <p style="text-align:center;font-size:x-large;">
            <a href="/learn/voc/" style="color:black;">Back</a>
            </p>
            <div>
            <img src='
            """+img_ref_link+"""
            ' style="width: 35%;height: 75%;">
            <img src='
            """+img_user_link+"""
            ' style="width: 35%;height: 75%;">
            </div>
            
            
            
            </body>
            </html>
            """
    return HttpResponse(html_response)

@login_required(login_url='/learn/')
def storeaudio(request):
    #1) Record stream data from the mic, 2)evaluate it with Google Speech-to-text score and 3) graph it
    print('writing the file')
    with open("learn/media/learn/audio/user.mp3", 'wb') as f:
        #print(request.body)
        f.write(request.body)


    html_response = "<html><b>you made a file</p></html>"
    return HttpResponse(html_response)
    #return HttpResponse(json.dumps(html_response))
    #return JsonResponse(html_response)


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
            quizz.Score +=1
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
        Quizz.objects.filter(Progression=progression, State=1).delete()

        total = request.POST.get('number')
        total = int(total)

        #mode = request.POST.get('mode')
        mode = "rec"


        if langid == 1 :
            word_list_total = [word for word in Wordjp.objects.all()]

        if langid == 3:
            word_list_total = [word for word in Wordfr.objects.all()]

        if langid == 4:
            word_list_total = [word for word in Wordru.objects.all()]

        if total > len(word_list_total):
            total = len(word_list_total)

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
            'end': True
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


@login_required(login_url='/learn/')
def credits(request):
    user = request.user
    custom_user = Usercustom.objects.get(user=user)
    progression = Progression.objects.get(UserId=custom_user.id, IsActive=True)
    lang = progression.LangId
    context = {
        'lang': lang,
    }
    return render(request, 'learn/credits.html', context)