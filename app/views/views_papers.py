from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from app.classes import PaperForm
from app.models import Paper

__author__ = 'Tadej'

def view_paper(request):
    id = request.GET.get('id',0)
    if id != 0:
        if Paper.objects.get(pk=id).user_id != request.user.pk:
            raise Http404("The selected view does not exist")
    PaperFormSet = modelformset_factory(Paper,extra=1,max_num=1, fields=('title', 'abstract'))
    paper_id = request.GET.get('id', 0)
    formset = PaperFormSet(queryset=Paper.objects.filter(pk=paper_id))
    return render(request, 'app/view_paper.html', {'formset':formset})

def update_paper(request):
    if request.method == "POST":
        PaperFormSet = modelformset_factory(Paper,extra=0, fields=('title', 'abstract'))
        formset = PaperFormSet(request.POST, request.FILES)
        objs = formset.save(commit=False)
        for obj in objs:
            if obj.user_id == None:
                obj.user_id = request.user.pk
            obj.save()
        return redirect('/app/index/')
    else:
        return Http404
