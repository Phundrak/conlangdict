from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'dictionary'

urlpatterns = [

    # choix du langage traduit et du langage de traduction
    # /dictionary/
    path('', views.IndexView.as_view(), name='index'),

    # renvoie à la liste des mots de la première initiale de <from_lang>
    # /search/<from_lang>/<to_lang>/
    # /search/HJP/FRA
    url(r'^search/(?P<natlang>\w+)/(?P<conlang>\w+)/*$',
        views.WordListView.as_view(),
        name='index_lang'),

    # renvoie à la liste des mots de la première initiale de <from_lang>
    # /search/<from_lang>/<to_lang>/<initial>
    # /search/HJP/FRA/a
    url(r'^search/(?P<natlang>\w+)/(?P<conlang>\w+)/(?P<initial>\w)/*$',
        views.InitialsListView.as_view(),
        name='index_initial'),

    # renvoie le détail de la traduction de `word` en `from_lang` vers
    # `to_lang`
    # /word/<from_lang>/<to_lang>/<slug>/
    # /word/HJP/FRA/hj-lp
    url(r'^word/(?P<from_lang>\w+)/(?P<to_lang>\w+)/(?P<slug>[-\w0-9]+)/*$',
        views.DetailView.as_view(),
        name='details'),

    # renvoie cinq mots de `from_lang` commençant par `word`
    # /guess/<from_lang>/<word>/
    # /guess/HJLP/hj
    url(r'^guess/(?P<from_lang>\w+)/(?P<word>[-\w0-9]+)/*$',
        views.guessword,
        name='guessword'),
]
