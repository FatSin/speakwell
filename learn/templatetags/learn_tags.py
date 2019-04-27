from django import template

register = template.Library()

@register.simple_tag
def getfilejp(word):
    word = word.replace(" ","")
    return 'learn/audio/jp/{0}-jp.mp3'.format(word)

@register.simple_tag
def getfilefr(word):
    word = word.replace(" ", "")
    return 'learn/audio/fr/{0}-fr.wav'.format(word)

@register.simple_tag
def getfileru(word):
    word = word.replace(" ", "")
    return 'learn/audio/ru/{0}-ru.mp3'.format(word)
