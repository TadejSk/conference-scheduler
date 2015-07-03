from django.http import Http404
from django.shortcuts import render, redirect
from ..models import ScheduleSettings
from ..classes import schedule_settings_class
import ast
__author__ = 'Tadej'

def schedule_settings(request):
    settings = ScheduleSettings.objects.get(user=request.user)
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
                                                          'settings_list':settings_list})

def save_simple_schedule_settings(request):
    num_days = request.POST.get('num_days',None)
    base_time = request.POST.get('base_time',None)
    if not ScheduleSettings.objects.filter(user=request.user).exists():
        settings=ScheduleSettings()
        settings.num_days=num_days
        settings.slot_length=base_time
        settings.user=request.user
        settings.save()
    else:
        settings=ScheduleSettings.objects.get(user=request.user)
        settings.num_days=num_days
        settings.slot_length=base_time
        s = schedule_settings_class(settings.settings_string, int(settings.num_days))
        settings.settings_string = str(s)
        # If we added extra days, the settings string needs to be updated
        settings.save()
    return redirect('/app/settings/schedule/')

def schedule_add_slot(request):
    settings_model = ScheduleSettings.objects.get(user=request.user)
    settings = schedule_settings_class(settings_model.settings_string, settings_model.num_days)
    settings.add_slot_to_day(int(request.POST.get('day')), settings_model.slot_length)
    settings_model.settings_string = str(settings)
    settings_model.save()
    return redirect('/app/settings/schedule/?day='+request.POST.get('day'))

def schedule_add_parallel_slots(request):
    settings_model = ScheduleSettings.objects.get(user=request.user)
    settings = schedule_settings_class(settings_model.settings_string, settings_model.num_days)
    settings.add_parallel_slots_to_day(int(request.POST.get('day')), settings_model.slot_length,
                                       int(request.POST.get('num_slots')))
    settings_model.settings_string = str(settings)
    settings_model.save()
    return redirect('/app/settings/schedule/?day='+request.POST.get('day'))

def schedule_change_slot_time(request):
    print("bbb")
    settings_model = ScheduleSettings.objects.get(user=request.user)
    settings = schedule_settings_class(settings_model.settings_string, settings_model.num_days)
    settings.change_slot_time(day=int(request.POST.get('day')), row=int(request.POST.get('row')),
                              col=int(request.POST.get('col')),new_len=int(request.POST.get('len')))
    settings_model.settings_string = str(settings)
    settings_model.save()
    return redirect('/app/settings/schedule/?day='+request.POST.get('day'))