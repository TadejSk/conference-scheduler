from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from app.models import Paper
from ..classes.clusterer import Clusterer
__author__ = 'Tadej'

@login_required
def basic_clustering(request):
    papers = Paper.objects.filter(user=request.user, is_locked=False)
    clusterer = Clusterer()
    clusterer.add_papers(papers)
    clusterer.create_dataset()
    clusterer.basic_clustering()
    return redirect("/app/index")
