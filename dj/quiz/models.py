# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.postgres.fields import JSONField


# Create your models here.

# class Quiz(models.Model):


class Questions(models.Model):
    question = models.TextField(verbose_name=_(u"Вопрос"))
    answers = JSONField(verbose_name=_(u"Ответы"))  # {"answers": [<answers>], "correct": <correct answer number>}
