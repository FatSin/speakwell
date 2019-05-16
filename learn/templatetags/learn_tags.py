import os
from django import template

register = template.Library()

MEDIA_DIR = 'learn/media/'

def get_type(word, lg):
    if os.path.exists(MEDIA_DIR+'learn/audio/'+lg+'/'+word+'-'+lg+'.mp3'):
        path = 'learn/audio/' + lg + '/' + word + '-'+lg+'.mp3'
    else:
        path = 'learn/audio/' + lg + '/' + word + '-'+lg+'.wav'
    return path

@register.simple_tag
def getfilejp(word):
    word = word.replace(" ?","")
    #return 'learn/audio/jp/{0}-jp.mp3'.format(word)
    #return 'learn/media/learn/audio/jp/{0}-jp.mp3'.format(word)
    return get_type(word, 'jp')

@register.simple_tag
def getfilefr(word):
    word = word.replace(" ?", "")
    #return 'learn/audio/fr/{0}-fr.wav'.format(word)
    #return 'learn/media/learn/audio/fr/{0}-fr.wav'.format(word)
    return get_type(word, 'fr')

@register.simple_tag
def getfileru(word):
    word = word.replace(" ?", "")
    #return 'learn/audio/ru/{0}-ru.mp3'.format(word)
    #return 'learn/media/learn/audio/ru/{0}-ru.wav'.format(word)
    return get_type(word, 'ru')