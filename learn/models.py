from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Language(models.Model):
    NameEng = models.CharField(max_length=20, unique=True)
    Code = models.CharField(max_length=7, unique=True)

class User(models.Model):
    LoginName = models.CharField(max_length=20, unique=True)
    Password = models.CharField(max_length=20, unique=True)
    Email = models.CharField(max_length=20)
    #A voir si ça ne va pas poser souci dans la modif de langue
    LangDisplay = models.ForeignKey(Language, on_delete=models.CASCADE)

class Word(models.Model):
    NameEng = models.CharField(max_length=20, unique=True)
    Phonetics = models.CharField(max_length=20)
    IsEnabled = models.BooleanField(max_length=20, default=True)

class Wordjp(models.Model):
    NameHira = models.CharField(max_length=20)
    NameKata = models.CharField(max_length=20)
    NameKanji = models.CharField(max_length=20)
    NameRoma = models.CharField(max_length=20)
    NameEng = models.ForeignKey(Word, on_delete=models.CASCADE)


class Progression(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    LangId = models.ForeignKey(Language, on_delete=models.CASCADE)
    Level = models.PositiveSmallIntegerField()
    Points = models.PositiveIntegerField()
    WordsLearnt = ArrayField(models.PositiveSmallIntegerField())
    Exelearnt = ArrayField(models.PositiveSmallIntegerField())
    FunFacts = ArrayField(models.PositiveSmallIntegerField())




