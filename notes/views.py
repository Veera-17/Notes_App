from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Notebook
from taggit.models import Tag
from django.views.generic import ListView, DetailView
from django.http import HttpResponse

def landing_page(request):
    return render(request, 'notes/landing_page.html')

class NotebookListView(ListView):
    model = Notebook
    context_object_name = 'notebook'
    template_name = 'notes/notebook_list.html'

def note_list_view(request, pk=None):
    if pk:
        notebook = get_object_or_404(Notebook, pk=pk)
        notes = Note.objects.filter(notebook=notebook).order_by('-modified')
    else:
        notebook = None
        notes = Note.objects.all().order_by('-modified')

    context = {
        'notes': notes,
        'notebook': notebook,
    }
    return render(request, 'notes/note_list.html', context)
    
def note_detail(request, pk, tag_slug=None):
    note = get_object_or_404(Note, pk=pk)
    tag = None
    similar_note = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        similar_note = Note.objects.all().filter(tags__in=[tag]).exclude(pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note, 'similar_note':similar_note, 'tag_slug':tag_slug})