__author__ = 'Tadej'
from django.forms import ModelForm
from app.models import *

class PaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'abstract']