import ast
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from app.models import Paper, Conference
from ..classes.clusterer import Clusterer
from ..classes.schedule_manager import schedule_manager_class

__author__ = 'Tadej'

@login_required
def basic_clustering(request):
    # Select papers for clustering
    papers = Paper.objects.filter(user=request.user, is_locked=False)
    schedule = Conference.objects.get(user = request.user, pk=request.session['conf'] ).schedule_string
    schedule = ast.literal_eval(schedule)
    settings = Conference.objects.get(user = request.user, pk=request.session['conf']).settings_string
    settings = ast.literal_eval(settings)
    clusterer = Clusterer(papers=papers, schedule=schedule, schedule_settings=settings)
    clusterer.create_dataset()
    clusterer.basic_clustering()
    clusterer.fit_to_schedule()
    # Add papers to schedule
    schedule = Conference.objects.get(user = request.user, pk=request.session['conf']).schedule_string
    settings = Conference.objects.get(user = request.user, pk=request.session['conf']).settings_string
    schedule_manager = schedule_manager_class()
    schedule_manager.import_paper_schedule(schedule)
    schedule_manager.set_settings(settings)
    for paper in papers:
        if (paper.add_to_day != -1) and (paper.add_to_row != -1) and (paper.add_to_col != -1):
            schedule_manager.assign_paper(paper.pk, paper.add_to_day, paper.add_to_row, paper.add_to_col)
    schedule_settings = Conference.objects.get(user = request.user, pk=request.session['conf'])
    schedule_settings.schedule_string = schedule_manager.papers
    schedule_settings.save()
    return redirect('/app/clustering/results')

def clustering_results(request):
    # Get paper info for displaying papers on the result page
    num_papers = Paper.objects.filter(user=request.user,cluster__gte=1).count()
    papers = Paper.objects.filter(user=request.user, cluster__gte=1).order_by('cluster')
    paper_titles = []
    paper_ids = []
    paper_clusters = []
    paper_coords_x = []
    paper_coords_y = []
    for paper in papers:
        paper_titles.append(paper.title)
        paper_ids.append(paper.pk)
        paper_clusters.append(paper.cluster)
        paper_coords_x.append(paper.visual_x)
        paper_coords_y.append(paper.visual_y)
    return render(request, 'app/clustering_results.html',
                  {'num_papers':num_papers, 'paper_titles':paper_titles,
                   'paper_ids':paper_ids, 'paper_clusters':paper_clusters,
                   'paper_coords_x':paper_coords_x,
                   'paper_coords_y':paper_coords_y})
