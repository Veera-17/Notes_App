from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Notebook
from taggit.models import Tag
from django.views.generic import ListView, DetailView

class NotebookListView(ListView):
    model = Notebook
    context_object_name = 'notebook'
    template_name = 'notes/notebook_list.html'

class NoteListView(ListView):
    model = Note
    context_object_name = 'notes'
    template_name = 'notes/note_list.html'
    
    def get_queryset(self):
        self.notebook = get_object_or_404(Notebook, pk=self.kwargs['pk'])
        queryset = Note.objects.filter(notebook=self.notebook)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notebook'] = self.notebook
        return context
    
def note_detail(request, pk, tag_slug=None):
    note = get_object_or_404(Note, pk=pk)
    tag = None
    similar_note = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        similar_note = Note.objects.all().filter(tags__in=[tag]).exclude(pk=pk)
    
    return render(request, 'notes/note_detail.html', {'note': note, 'similar_note':similar_note, 'tag_slug':tag_slug})