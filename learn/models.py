from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Language(models.Model):
    NameEng = models.CharField(max_length=20, unique=True)
    Code = models.CharField(max_length=7, unique=True)

    def __str__(self):
        return '{0}'.format(self.NameEng)

class Usercustom(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #LoginName = models.CharField(max_length=20, unique=True)
    #Password = models.CharField(max_length=20, unique=True)
    #Email = models.CharField(max_length=20)
    #A voir si ça ne va pas poser souci dans la modif de langue
    LangDisplay = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.user)


class Word(models.Model):
    NameEng = models.CharField(max_length=40, unique=True)
    IsEnabled = models.BooleanField(max_length=20, default=True)

    def __str__(self):
        return '{0}'.format(self.NameEng)

class Wordjp(models.Model):
    Phonetics = models.CharField(max_length=40)
    NameHira = models.CharField(max_length=40)
    NameKata = models.CharField(max_length=40)
    NameKanji = models.CharField(max_length=40)
    NameRoma = models.CharField(max_length=40)
    NameEng = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.NameRoma)

class Wordfr(models.Model):
    Phonetics = models.CharField(max_length=40)
    Name = models.CharField(max_length=40)
    NameEng = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.Name)


class Wordru(models.Model):
    Phonetics = models.CharField(max_length=40)
    NameRu = models.CharField(max_length=40)
    NameRoma = models.CharField(max_length=40)
    NameEng = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return '{0}'.format(self.NameRoma)


class Progression(models.Model):
    UserId = models.ForeignKey(Usercustom, on_delete=models.CASCADE)
    LangId = models.ForeignKey(Language, on_delete=models.CASCADE)
    Level = models.PositiveSmallIntegerField()
    Points = models.PositiveIntegerField()
    WordsLearnt = ArrayField(models.PositiveSmallIntegerField())
    Exelearnt = ArrayField(models.PositiveSmallIntegerField())
    FunFacts = ArrayField(models.PositiveSmallIntegerField())
    IsActive = models.BooleanField(max_length=20, default=True)

    def __str__(self):
        return '{0} {1}'.format(self.UserId, self.LangId)


class Theme(models.Model):
    NameEng = models.CharField(max_length=20)
    NameFr = models.CharField(max_length=20)
    IsEnabled = models.BooleanField(max_length=20, default=True)
    #Word = models.ForeignKey(Word, on_delete=models.CASCADE)
    words = models.ManyToManyField(Word, related_name='themes', blank=True)

    def __str__(self):
        return '{0}'.format(self.NameEng)


class Quizz(models.Model):
    Progression = models.ForeignKey(Progression, on_delete=models.CASCADE)
    Score = models.PositiveIntegerField()
    WordList = ArrayField(models.PositiveSmallIntegerField())
    Total = models.PositiveIntegerField()
    Difficulty = models.PositiveIntegerField()
    Mode = models.CharField(max_length=20)
    State = models.PositiveIntegerField()