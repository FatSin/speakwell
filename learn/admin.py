from django.contrib import admin

from .models import Word, Wordjp, Wordfr, Wordru, Language, Theme, Usercustom, Progression

# Register your models here.
admin.site.register(Word)
admin.site.register(Wordjp)
admin.site.register(Wordfr)
admin.site.register(Wordru)
admin.site.register(Language)
admin.site.register(Theme)
admin.site.register(Usercustom)
admin.site.register(Progression)