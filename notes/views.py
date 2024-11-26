from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Notebook
from taggit.models import Tag
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import CreateNotebookForm, CreateNoteForm
from django.utils.text import slugify
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def slug_convertor(field):
    return slugify(field)

def landing_page(request):
    return render(request, 'notes/landing_page.html')

class NotebookListView(LoginRequiredMixin, ListView):
    model = Notebook
    context_object_name = 'notebook'
    template_name = 'notes/notebook_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Notebook.objects.filter(author=self.request.user).order_by('-modified')

@login_required
def note_list_view(request, pk=None):
    if pk:
        notebook = get_object_or_404(Notebook, pk=pk)
        notes = Note.objects.filter(notebook=notebook, author=request.user).order_by('-modified')
    else:
        notebook = None
        notes = Note.objects.filter(author=request.user).order_by('-modified')

    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    notes_count = notes.count()
    try:
        paginated_notes = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_notes = paginator.page(1)
    except EmptyPage:
        paginated_notes = paginator.page(paginator.num_pages)
    context = {
        'notes': paginated_notes,
        'notebook': notebook,
        'notes_count':notes_count
    }
    return render(request, 'notes/note_list.html', context)
    
@login_required    
def note_detail(request, pk, tag_slug=None):
    note = get_object_or_404(Note, pk=pk)
    tag = None
    similar_note = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        similar_note = Note.objects.all().filter(tags__in=[tag], author=request.user).exclude(pk=pk).order_by('-modified')
        paginator = Paginator(similar_note, 3)
        page_number = request.GET.get('page')
        try:
            paginated_similar_notes = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_similar_notes = paginator.page(1)
        except EmptyPage:
            paginated_similar_notes = paginator.page(paginator.num_pages)
    else:
        paginated_similar_notes = None

        
    return render(request, 'notes/note_detail.html', {'note': note, 'similar_note':paginated_similar_notes, 'tag_slug':tag_slug})

@login_required
def notebook_create(request):
    if request.method == 'POST':
        form = CreateNotebookForm(request.POST)
        if form.is_valid():
            slug = slug_convertor(form.cleaned_data['title'])
            existing_notebook = Notebook.objects.filter(slug=slug, author=request.user).exists()
            if existing_notebook:
                messages.warning(request, 'A notebook with this title already exists. Please choose a different title.')
            else:
                notebook = form.save(commit=False)
                notebook.author = request.user
                notebook.slug = slug
                notebook.save()
                return redirect('note_list_filtered', pk=notebook.pk)
    else:
        form = CreateNotebookForm()
    return render(request, 'notes/notebook_create.html', {'form': form})

class NotebookUpdateView(LoginRequiredMixin, UpdateView):
    model = Notebook
    form_class = CreateNotebookForm
    template_name = 'notes/notebook_update.html'
    login_url = 'login'

    def get_queryset(self):
        return Notebook.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        new_slug = slug_convertor(form.instance.title)
        if Notebook.objects.filter(slug=new_slug, author=self.request.user).exclude(pk=self.object.pk).exists():
            messages.error(self.request, 'A notebook with this title already exists. Please choose a different title.')
            return redirect('notebook_update', pk=self.object.pk)
        form.instance.slug = new_slug
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('note_list_filtered', kwargs={'pk': self.object.pk})

class NotebookDeleteView(LoginRequiredMixin, DeleteView):
    model = Notebook
    login_url = 'login'
    context_object_name = 'notebook'

    def get_queryset(self):
        return Notebook.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('notebook_list')

@login_required
def note_create(request):
    if request.method == 'POST':
        form = CreateNoteForm(request.POST, user=request.user)
        if form.is_valid():
            slug = slugify(form.cleaned_data['title'])
            existing_note = Note.objects.filter(slug=slug, author=request.user).exists()
            if existing_note:
                messages.warning(request, 'A note with this title already exists. Please choose a different title.')
            else:
                note = form.save(commit=False) 
                note.author = request.user
                note.slug = slug
                note.save()
                tags = form.cleaned_data.get('tags', '')
                if tags:
                    note.tags.set(tags.split(','))
                note.save() 
                return redirect('note_list_filtered', pk=note.notebook.pk)
    else:
        form = CreateNoteForm(user=request.user)
    return render(request, 'notes/note_create.html', {'form': form,})

@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, author=request.user)
    if request.method == 'POST':
        form = CreateNoteForm(request.POST, instance=note, user=request.user)
        if form.is_valid():
            new_slug = slugify(form.cleaned_data['title'])
            if Note.objects.filter(slug=new_slug, author=request.user).exclude(pk=note.pk).exists():
                messages.error(request, 'A note with this title already exists. Please choose a different title.')
                return redirect('note_update', pk=note.pk)
            form.instance.slug = new_slug
            form.save()
            tags = form.cleaned_data.get('tags', '')
            tags = tags.strip('"').strip("'")
            tag_list = [tag.strip('"').strip("'").strip() for tag in tags.split(',')]
            if tags:
                note.tags.set(tag_list)
            note.save()
            return redirect('note_list_filtered', pk=note.notebook.pk)
    else:
        form = CreateNoteForm(instance=note, user=request.user)
    return render(request, 'notes/note_update.html', {'form': form, 'note': note})

@login_required
def note_delete(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)
        notebook = note.notebook
        note.delete()
        return redirect('note_list_filtered', pk=notebook.pk) 