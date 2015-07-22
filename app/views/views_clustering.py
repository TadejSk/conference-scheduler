import ast
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from app.models import Paper, ScheduleSettings
from ..classes.clusterer import Clusterer
from ..classes.schedule_manager import schedule_manager_class

__author__ = 'Tadej'

@login_required
def basic_clustering(request):
    # Select papers for clustering
    papers = Paper.objects.filter(user=request.user, is_locked=False)
    schedule = ScheduleSettings.objects.filter(user = request.user).first().schedule_string
    schedule = ast.literal_eval(schedule)
    settings = ScheduleSettings.objects.filter(user = request.user).first().settings_string
    settings = ast.literal_eval(settings)
    clusterer = Clusterer(papers=papers, schedule=schedule, schedule_settings=settings)
    clusterer.create_dataset()
    clusterer.basic_clustering()
    clusterer.fit_to_schedule()
    # Add papers to schedule
    schedule = ScheduleSettings.objects.filter(user = request.user).first().schedule_string
    settings = ScheduleSettings.objects.filter(user = request.user).first().settings_string
    schedule_manager = schedule_manager_class()
    schedule_manager.import_paper_schedule(schedule)
    schedule_manager.set_settings(settings)
    for paper in papers:
        if (paper.add_to_day != -1) and (paper.add_to_row != -1) and (paper.add_to_col != -1):
            schedule_manager.assign_paper(paper.pk, paper.add_to_day, paper.add_to_row, paper.add_to_col)
    schedule_settings = ScheduleSettings.objects.filter(user = request.user).first()
    schedule_settings.schedule_string = schedule_manager.papers
    schedule_settings.save()
    return redirect("/app/index")
