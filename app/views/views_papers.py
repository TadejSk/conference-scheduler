import ast
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from app.models import Paper, ScheduleSettings
from ..classes import schedule_manager_class


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
        raise Http404

@csrf_exempt
def add_paper_to_schedule(request):
    set = schedule_manager_class()
    settings=ScheduleSettings.objects.get(user=request.user)
    if settings.schedule_string == "[]":
        set.create_empty_list(settings.settings_string)
    else:
        set.import_paper_schedule(settings.schedule_string)
    row = request.POST.get('row')
    col = request.POST.get('col')
    id = request.POST.get('id')
    day = request.POST.get('day')
    set.assign_paper(int(id), int(day), int(row), int(col))
    settings.schedule_string = str(set.papers)
    settings.save()
    print(set.papers)
    return redirect('/app/index/')

@csrf_exempt
def remove_paper_from_schedule(request):
    set = schedule_manager_class()
    settings=ScheduleSettings.objects.get(user=request.user)
    if settings.schedule_string == "[]":
        set.create_empty_list(settings.settings_string)
    else:
        set.import_paper_schedule(settings.schedule_string)
    id = int(request.POST.get('id'))
    set.remove_paper(id)
    settings.schedule_string = str(set.papers)
    settings.save()
    return redirect('/app/index')