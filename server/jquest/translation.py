# -*- coding: utf-8 -*-
from modeltranslation.translator import translator, TranslationOptions
from jquest.models import Post

class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'excerpt', 'content')    

translator.register(Post, PostTranslationOptions)