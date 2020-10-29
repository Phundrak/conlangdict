from django.contrib import admin

from .models import Category, Gender, Language, Word, Wordclass

admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Gender)
admin.site.register(Word)
admin.site.register(Wordclass)
