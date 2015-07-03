from django.forms import modelformset_factory
from django.shortcuts import render
from app.models import Paper

__author__ = 'Tadej'

def view_paper(request):
    AuthorFormSet = modelformset_factory(Paper, fields=('title', 'abstract'))
    formset = AuthorFormSet(queryset=Paper.objects.filter(pk=-1))
    return render(request, 'app/view_paper.html', {'formset':formset})
