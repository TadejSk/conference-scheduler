from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from app.classes import *
from app.models import ScheduleSettings

__author__ = 'Tadej'

@login_required
def index(request):
    # Get the number of all authors and papers
    num_authors = Author.objects.filter(user=request.user).count()
    num_papers = Paper.objects.filter(user=request.user).count()
    # Get the data necessary to display the schedule
    settings = ScheduleSettings.objects.get(user=request.user)
    num_days = None
    if settings is not None:
        num_days = settings.num_days
    day = int(request.GET.get('day',0))
    if day >= num_days and num_days >=1:
        raise Http404('The selected day is too high')
    settings_list = ast.literal_eval(settings.settings_string)[int(request.GET.get('day',0))]
    # Create a list of all the papers that the user has imported/created
    papers = Paper.objects.filter(user=request.user)
    paper_titles = []
    paper_ids = []
    for paper in papers:
        paper_titles.append(paper.title)
        paper_ids.append(paper.pk)
    return render(request, 'app/index.html', {'num_authors':num_authors, 'num_papers':num_papers, 'num_days':num_days,
                                              'settings_list':settings_list,'paper_titles':paper_titles,
                                              'paper_ids':paper_ids})

def import_data(request):
    path = request.POST.get('file_path',None)
    if not path :
        return redirect('/app/index')
    if path[len(path)-1] != '/':
        path += '/'
    accepted_path = path + 'accepted.xls'
    assignments_path = path + 'assignments.csv'
    data = raw_data(accepted_path,assignments_path)
    p = data.parse_accepted()
    for paper in p.accepted_papers_list:
        if not Paper.objects.filter(title=paper.title, user=request.user).exists():
            db_paper = Paper()
            db_paper.title = paper.title
            db_paper.abstract = paper.abstract
            db_paper.user = request.user
            db_paper.save()
            #print(paper.authors)
            for author in paper.authors:
                if not Author.objects.filter(name=author, user=request.user ).exists():
                    db_author = Author()
                    db_author.name=author
                    db_author.user = request.user
                    db_author.save()
                    db_author.papers.add(db_paper)
                else:
                    db_author = Author.objects.get(name=author)
                    db_author.papers.add(db_paper)
    request.session['accepted_path'] = accepted_path
    request.session['assignments_path'] = assignments_path
    return redirect('/app/index')

