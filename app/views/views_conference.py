from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import Conference

__author__ = 'Tadej'

@login_required
def conference_list(request):
    conferences = Conference.objects.filter(user=request.user).order_by('id')
    form_data = [(c.title,c.id) for c in conferences]
    num_conferences = conferences.count()
    return render(request, 'app/conference_list.html', {'conferences':conferences, 'num_conferences':num_conferences,
                                                        'form_data':form_data})

@login_required
def create_conference(request):
    conference = Conference()
    conference.user = request.user
    conference.title = request.POST.get('title', 'Unnamed conference')
    if conference.title == '':
        conference.title = 'Unnamed conference'
    conference.save()
    return redirect('/app/conference/list')

@login_required
def delete_conference(request):
    conference = Conference.objects.get(pk=request.POST.get('conference', None), user=request.user)
    conference.delete()
    return redirect('/app/conference/list')