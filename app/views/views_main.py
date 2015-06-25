from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.classes import *

__author__ = 'Tadej'

@login_required
def index(request):
    print(request.user.username)
    return render(request, 'app/index.html')

def import_data(request):
    path = request.POST.get('file_path',None)
    if not path :
        return redirect('/app/index')
    if path[len(path)-1] != '/':
        path += '/'
    accepted_path = path + 'accepted.xls'
    assignments_path = path + 'assignments.csv'
    raw_data(accepted_path,assignments_path)
    request.session['accepted_path'] = accepted_path
    request.session['assignments_path'] = assignments_path
    return redirect('/app/index')
