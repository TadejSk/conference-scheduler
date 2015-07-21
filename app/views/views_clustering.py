import ast
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from app.models import Paper, ScheduleSettings
from ..classes.clusterer import Clusterer

__author__ = 'Tadej'

@login_required
def basic_clustering(request):
    papers = Paper.objects.filter(user=request.user, is_locked=False)
    schedule = ScheduleSettings.objects.filter(user = request.user).first().schedule_string
    schedule = ast.literal_eval(schedule)
    settings = ScheduleSettings.objects.filter(user = request.user).first().settings_string
    settings = ast.literal_eval(settings)
    clusterer = Clusterer(papers=papers, schedule=schedule, schedule_settings=settings)
    clusterer.create_dataset()
    clusterer.basic_clustering()
    clusterer.fit_to_schedule()
    return redirect("/app/index")
