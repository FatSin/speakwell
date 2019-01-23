from django.contrib import admin

from .models import Word, Wordjp, Language

# Register your models here.
admin.site.register(Word)
admin.site.register(Wordjp)
admin.site.register(Language)
