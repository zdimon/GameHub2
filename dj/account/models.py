# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, verbose_name=u"Пользователь")
    wins = models.IntegerField(verbose_name=u"Выиграно")
    lose = models.IntegerField(verbose_name=u"Проиграно")
    leave = models.IntegerField(verbose_name=u"Покинуто")
    all = models.IntegerField(verbose_name=u"Всего")
    coins = models.IntegerField(verbose_name=u"Монеты")
