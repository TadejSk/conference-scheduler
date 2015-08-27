import ast
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from app.models import Paper, Conference
from ..classes.clusterer import Clusterer
from ..classes.schedule_manager import schedule_manager_class
import time
import profile

__author__ = 'Tadej'

def setup_clustering(request):
    # initialize clustering
    papers = Paper.objects.filter(user=request.user, is_locked=False, conference=request.session['conf'])
    settings = Conference.objects.get(user = request.user, pk=request.session['conf']).settings_string
    settings = ast.literal_eval(settings)
    schedule_db = Conference.objects.get(user = request.user, pk=request.session['conf'] )
    schedule = ast.literal_eval(schedule_db.schedule_string)
    clusterer = Clusterer(papers=papers, schedule=schedule, schedule_settings=settings, func=request.POST.get('method', ""))
    num_cl = request.POST.get('num_clusters', False)
    print("clusters set to ", num_cl)
    if num_cl != False:
        if num_cl == '':
            clusterer.num_clusters = 10
        else:
            clusterer.num_clusters = int(num_cl)
    band = request.POST.get('band', False)
    if band != False and band != '':
        clusterer.bandwith_factor=int(band)
        print("BAND SET TO ", band)
    clusterer.set_cluster_function(request.POST.get('method', ""))
    if request.POST.get('useabstracts',False):
        clusterer.using_abstracts = True
    else:
        clusterer.using_abstracts = False
    if request.POST.get('usetitles',False):
        clusterer.using_titles = True
    else:
        clusterer.using_titles = False
    if request.POST.get('assign',False):
        clusterer.using_graph_data = True
    else:
        clusterer.graph_dataset = False
    vocab_string = request.POST.get('keywords', '')
    clusterer.set_custom_vocabulary(vocab_string)
    clusterer.add_graph(schedule_db.paper_graph_string)
    clusterer.create_dataset()
    return clusterer

@login_required
def basic_clustering(request):
    # Select papers for clustering
    papers = Paper.objects.filter(user=request.user, is_locked=False, conference=request.session['conf'])
    schedule = Conference.objects.get(user = request.user, pk=request.session['conf'] ).schedule_string
    schedule = ast.literal_eval(schedule)
    settings = Conference.objects.get(user = request.user, pk=request.session['conf']).settings_string
    settings = ast.literal_eval(settings)
    # Before clustering, every non-locked paper must be removed from schedule, since the clustering algorithm currently
    # only works with empty slots.
    ids_to_remove = []
    for day in schedule:
        for row in day:
            for col in row:
                print("GOT COL: ", col)
                for id in col:
                    paper = Paper.objects.get(pk=id)
                    print("ID ", id)
                    if not paper.is_locked:
                        ids_to_remove.append(id)
                        print("REMOVED ", id, "COL IS NOW ", col)
    schedule_db = Conference.objects.get(user = request.user, pk=request.session['conf'] )
    schedule_manager = schedule_manager_class()
    schedule_manager.import_paper_schedule(schedule_db.schedule_string)
    for id in ids_to_remove:
        print(schedule_manager.papers)
        schedule_manager.remove_paper(id)
    print(schedule_manager.papers)
    schedule_db.schedule_string = str(schedule_manager.papers)
    schedule_db.save()
    # Begin clustering, after reloading new schedule data
    schedule = Conference.objects.get(user = request.user, pk=request.session['conf'] ).schedule_string
    schedule = ast.literal_eval(schedule)
    print(schedule)
    #clusterer = Clusterer(papers=papers, schedule=schedule, schedule_settings=settings)
    #clusterer.add_graph(schedule_db.paper_graph_string)
    times = []

    for i in range(1, 2):
        start_time = time.time()
        clusterer = setup_clustering(request)
        clusterer.create_dataset()
        clusterer.basic_clustering()
        clusterer.fit_to_schedule2()
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        print("T: ", elapsed_time)
        print(i)
    print("TIME: ", sum(times)/len(times))
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
    return redirect('/app/clustering/results/all')

def clustering_results(request):
    # This one shows all clusters, even if they were not assigned to a schedule slot as a result of automatic scheduling
    # Get paper info for displaying papers on the result page
    num_papers = Paper.objects.filter(user=request.user,simple_cluster__gte=1, conference=request.session['conf']).count()
    papers = Paper.objects.filter(user=request.user, simple_cluster__gte=1, conference=request.session['conf']).order_by('cluster')
    paper_titles = []
    paper_ids = []
    paper_clusters = []
    paper_coords_x = []
    paper_coords_y = []
    for paper in papers:
        paper_titles.append(paper.title)
        paper_ids.append(paper.pk)
        paper_clusters.append(paper.simple_cluster)
        paper_coords_x.append(paper.simple_visual_x)
        paper_coords_y.append(paper.simple_visual_y)
    return render(request, 'app/clustering_results.html',
                  {'num_papers':num_papers, 'paper_titles':paper_titles,
                   'paper_ids':paper_ids, 'paper_clusters':paper_clusters,
                   'paper_coords_x':paper_coords_x,
                   'paper_coords_y':paper_coords_y, 'all':True})

def clustering_results_assigned(request):
    # This one only shows clusters that were actually assigned to a schedule slot during automatic clustering
    num_papers = Paper.objects.filter(user=request.user,cluster__gte=1, conference=request.session['conf']).count()
    papers = Paper.objects.filter(user=request.user, cluster__gte=1, conference=request.session['conf']).order_by('cluster')
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
                   'paper_coords_y':paper_coords_y, 'all':False})

def clustering_settings(request):
    # Check if assignment data is avaivable
    conf = Conference.objects.get(pk=request.session['conf'], user=request.user)
    if conf.paper_graph_string == '[]':
        has_assignment_data = False
    else:
        has_assignment_data = True
    return render(request, 'app/clustering_settings.html', {'has_assignment_data':has_assignment_data})
