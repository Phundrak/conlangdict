"""
Models for the database of the dictionary. This dictionary is thought of as a
bilingual dictionary capable of translating back and forth between natlangs
and the conlangs of https://langue.phundrak.fr
"""
from django.db import models
from django.utils.text import slugify


class Language(models.Model):
    """
    A general class to refer to languages, with its code and its name
    """
    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128)
    conlang = models.BooleanField(default=True)

    def __str__(self):
        return "{0.name} ({0.code})".format(self)

    class Meta:
        """
        Meta sub-class for ordering the languages
        """
        ordering = ('code', )


class Gender(models.Model):
    """
    Contains all possible gender in the languages supported by the
    dictionary, be it from natlangs or conlangs
    """
    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return "{0.name} ({0.code})".format(self)

    class Meta:
        """
        Meta sub-class for ordering the genders
        """
        ordering = ('name', )


class Wordclass(models.Model):
    """Contains all the word classes available in the supported languages"""
    code = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return "{0.name} ({0.code})".format(self)

    class Meta:
        """
        Meta sub-class for ordering the word classes
        """
        ordering = ('code', )


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    def save(self, *arg, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(arg, kwargs)

    class Meta:
        ordering = ('name', )


class Word(models.Model):
    """
    Represents any word from any language. It has a self-representation with
    "word", a reference to which language it belongs to with "language", a list
    of words "translation" that can be its translation (duh), a reference to
    its gender with "gender" (duh2), its word class with "wordclass", some
    "details" about the word (no more than 5000 chars), its "etymology" (no
    more than 5000 chars) and a list of words that can be its etymological
    "roots"
    """
    word = models.CharField(max_length=128)
    slug = models.CharField(max_length=128, blank=True, editable=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    translation = models.ManyToManyField("self", blank=True)
    gender = models.ForeignKey(Gender,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True)
    wordclass = models.ManyToManyField(Wordclass, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    roots = models.ManyToManyField("self", blank=True)
    details = models.TextField(max_length=8192, blank=True, null=True)
    etymology = models.TextField(max_length=8192, blank=True, null=True)

    def __str__(self):
        return self.word

    def save(self, *args, **kwargs):
        if self.word:
            self.slug = self.language.code + "-" + slugify(self.word)

        super(Word, self).save(args, kwargs)

    class Meta:
        """
        Meta sub-class for ordering words
        """
        ordering = ('slug', )
