"""
Views for the dictionary
"""

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView, View

# from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import SelectLangForm
from .models import Language, Word


class IndexView(View):
    """
    View for the main page. Two drop-down boxes will give the choice between
    which languages to translate, one will be used to select a natural language,
    the other a conlang.

    View for /
    """
    form_class = SelectLangForm
    template_name = 'dictionary/index.html'
    error_message = ""

    def get(self, request):
        """
        Displays the index page
        """
        form = self.form_class(None)
        return render(
            request, self.template_name, {
                'form': form,
                'conlangs': Language.objects.filter(conlang=True),
                'natlangs': Language.objects.filter(conlang=False),
                'error_message': self.error_message
            })

    def post(self, request):
        """
        Processes the form and redirects to the correct bilingual word list page
        if the form is correct, or to the main page if not
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            natlang = form.cleaned_data['natlang']
            conlang = form.cleaned_data['conlang']
            return HttpResponseRedirect('/search/' + natlang.code + '/' +
                                        conlang.code)
        print(form.errors)
        self.error_message = form.errors
        return render(
            request, self.template_name, {
                'form': form,
                'conlangs': Language.objects.filter(conlang=True),
                'natlangs': Language.objects.filter(conlang=False),
                'error_message': self.error_message,
            })


class WordListView(ListView):
    """
    Will list all the words from the language `natlang` translated to the
    language `conlang` and vice-versa

    View for /search/from_lang/to_lang
    """

    template_name = 'dictionary/language.html'
    context_object_name = 'natwords'
    form_class = SelectLangForm
    error_message = ""

    def get_queryset(self):
        """
        Get initial values to display
        """
        return Word.objects.filter(
            language__code=self.kwargs['natlang'],
            translation__language__code=self.kwargs['conlang']).distinct()

    def get_context_data(self, **kwargs):
        """
        Get some additional values
        """
        context = super(WordListView, self).get_context_data(**kwargs)
        context['conwords'] = Word.objects.filter(
            language__code=self.kwargs['conlang'],
            translation__language__code=self.kwargs['natlang']).distinct()
        context['natlang'] = Language.objects.filter(conlang=False)
        context['conlang'] = Language.objects.filter(conlang=True)
        context['cur_natlang'] = Language.objects.get(
            code=self.kwargs['natlang'])
        context['cur_conlang'] = Language.objects.get(
            code=self.kwargs['conlang'])
        return context


class InitialsListView(ListView):
    """
    Displays all the words from both languages beginning with a specified
    initial letter
    """

    # TODO: create dedicated template
    template_name = 'dictionary/language.html'
    context_object_name = 'natwords'

    def get_queryset(self):
        """
        Get initial values to display
        """
        return Word.objects.filter(
            language__code=self.kwargs['natlang'],
            slug__startswith=self.kwargs['initial'],
            translation__language__code=self.kwargs['conlang'])

    def get_context_data(self, **kwargs):
        """
        Get some additional values
        """
        context = super(InitialsListView, self).get_context_data(**kwargs)
        context['conwords'] = Word.objects.filter(
            language__code=self.kwargs['conlang'],
            slug__startswith=self.kwargs['initial'],
            translation__language__code=self.kwargs['natlang'])
        context['natlang'] = Language.objects.get(code=self.kwargs['natlang'])
        context['conlang'] = Language.objects.get(code=self.kwargs['conlang'])
        return context


class DetailView(DetailView):
    """
    Displays the details about the word `word` from the language `from_lang` if
    this word is from a conlang and will display its translations to the
    language `to_lang`

    View for /word/from_lang/to_lang/slug
    """
    model = Word
    template_name = 'dictionary/details.html'
    context_object_name = 'word'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['translations'] = context['word'].translation.filter(
            language=self.kwargs['to_lang'])
        context['from_lang'] = Language.objects.get(
            code=self.kwargs['from_lang'])
        context['to_lang'] = Language.objects.get(code=self.kwargs['to_lang'])
        return context


def guessword(request, from_lang, word):
    """
    Is used to get five words from `from_lang` beginning with `word`. This will
    be used for word suggestion when using the search bar.

    View for /guess/from_lang/word
    """
    pass
