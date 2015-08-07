from django.http import Http404
from django.shortcuts import render, redirect
from ..models import Conference
from ..classes import schedule_settings_class, schedule_manager_class
import ast
__author__ = 'Tadej'

def schedule_settings(request):
    error = request.session['parallel_error']
    settings = Conference.objects.get(user=request.user, pk=request.session['conf'])
    num_days = None
    base_time = None
    if settings is not None:
        num_days = settings.num_days
        base_time = settings.slot_length
    day = int(request.GET.get('day',0))
    if day >= num_days and num_days >=1:
        raise Http404('The selected day is too high')
    settings_list = ast.literal_eval(settings.settings_string)[int(request.GET.get('day',0))]
    return render(request, 'app/settings/schedule.html', {'num_days':num_days, 'base_time':base_time, 'day':day,
                                                          'settings_list':settings_list, 'error':error})

def save_simple_schedule_settings(request):
    num_days = request.POST.get('num_days',None)
    base_time = request.POST.get('base_time',None)
    if not Conference.objects.filter(user=request.user, pk=request.session['conf']).exists():
        settings=Conference()
        settings.num_days=num_days
        settings.slot_length=base_time
        settings.user=request.user
        settings.save()
    else:
        settings=Conference.objects.get(user=request.user, pk=request.session['conf'])
        settings.num_days=num_days
        settings.slot_length=base_time
        # Update settings string
        s = schedule_settings_class(settings.settings_string, int(settings.num_days))
        settings.settings_string = str(s)
        # Update schedule string
        schedule = ast.literal_eval(settings.schedule_string)

        if len(schedule) < int(num_days):
            for i in range(int(num_days)-len(schedule)):
                    schedule.append([])
        if len(schedule) > int(num_days):
            schedule = schedule[:int(num_days)]
        settings.schedule_string = str(schedule)
        # If we added extra days, the settings string needs to be updated
        settings.save()
    return redirect('/app/settings/schedule/')

def schedule_add_slot(request):
    settings_model = Conference.objects.get(user=request.user, pk=request.session['conf'])
    schedule = schedule_manager_class()
    if settings_model.schedule_string == "[]":
        schedule.set_settings(settings_model.settings_string)
        schedule.create_empty_list_from_settings()
    else:
        schedule.import_paper_schedule(settings_model.schedule_string)
    settings = schedule_settings_class(settings_model.settings_string, settings_model.num_days)
    settings.add_slot_to_day(int(request.POST.get('day')), settings_model.slot_length)
    settings_model.settings_string = str(settings)
    schedule.add_slot_to_day(int(request.POST.get('day')))
    settings_model.schedule_string = schedule.papers
    settings_model.save()
    return redirect('/app/settings/schedule/?day='+request.POST.get('day'))

def schedule_add_parallel_slots(request):
    request.session['parallel_error']=""
    if not request.POST.get('num_slots').isdigit():
        request.session['parallel_error'] = "Enter a valid integer"
        return redirect('/app/settings/schedule/?day='+request.POST.get('day'))
    settings_model = Conference.objects.get(user=request.user, pk=request.session['conf'])
    settings = schedule_settings_class(settings_model.settings_string, settings_model.num_days)
    settings.add_parallel_slots_to_day(int(request.POST.get('day')), settings_model.slot_length,
                                       int(request.POST.get('num_slots')))
    settings_model.settings_string = str(settings)
    schedule = schedule_manager_class()
    schedule.set_settings(settings_model.settings_string)
    if settings_model.schedule_string == "[]":
        schedule.set_settings(settings_model.settings_string)
        schedule.create_empty_list_from_settings()
    else:
        schedule.import_paper_schedule(settings_model.schedule_string)
    schedule.add_parallel_slots_to_day(int(request.POST.get('day')),int(request.POST.get('num_slots')))
    settings_model.schedule_string = schedule.papers
    settings_model.save()
    return redirect('/app/settings/schedule/?day='+request.POST.get('day'))

def schedule_change_slot_time(request):
    settings_model = Conference.objects.get(user=request.user, pk=request.session['conf'])
    settings = schedule_settings_class(settings_model.settings_string, settings_model.num_days)
    settings.change_slot_time(day=int(request.POST.get('day')), row=int(request.POST.get('row')),
                              col=int(request.POST.get('col')),new_len=int(request.POST.get('len')))
    settings_model.settings_string = str(settings)
    settings_model.save()
    return redirect('/app/settings/schedule/?day='+request.POST.get('day'))

def delete_slot(request):
    day = int(request.POST.get('day'))
    row = int(request.POST.get('row'))
    col = int(request.POST.get('col'))
    settings_model = Conference.objects.get(user=request.user, pk=request.session['conf'])
    settings = schedule_settings_class(settings_model.settings_string, settings_model.num_days)
    schedule = schedule_manager_class()
    schedule.import_paper_schedule(settings_model.schedule_string)
    settings.delete_slot(day,row,col)
    schedule.delete_slot(day,row,col)
    settings_model.settings_string = str(settings)
    settings_model.schedule_string = str(schedule)
    settings_model.save()
    return redirect('/app/settings/schedule/?day='+request.POST.get('day'))