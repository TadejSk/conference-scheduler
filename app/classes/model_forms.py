__author__ = 'Tadej'
from django.forms import ModelForm
from django import forms
from app.models import *

class PaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'abstract']

class FileForm(forms.Form):
    file = forms.FileField(label='Papers',
                           help_text='The file must be an EasyChair generated .xls file '
                                     'containing papers (ussually titled accepted.xls)')
class AssignmentsFileForm(forms.Form):
    file = forms.FileField(label='Assignments',
                           help_text='The file must be an EasyChair generated .csv file '
                                     'containing assignments (ussually titled assignments.csv)')