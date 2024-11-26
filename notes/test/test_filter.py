from django.test import TestCase
from django.contrib.auth.models import User
from notes.models import Note, Notebook
from taggit.models import Tag
from django.urls import reverse
from datetime import datetime
from notes.filters import NotebookFilter, NoteFilter
from django.utils import timezone

class NoteFilterTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.notebook1 = Notebook.objects.create(author=self.user, title='Notebook 1', slug='notebook-1')
        self.notebook2 = Notebook.objects.create(author=self.user, title='Notebook 2', slug='notebook-2')
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')
        self.note1 = Note.objects.create(author=self.user, notebook=self.notebook1, title='Note 1', slug='note-one', content='Content 1')
        self.note1.tags.add(self.tag1)
        self.note2 = Note.objects.create(author=self.user, notebook=self.notebook2, title='Note 2', slug='note-two', content='Content 2')
        self.note2.tags.add(self.tag2)
        self.note1.created = timezone.make_aware(datetime(2023, 1, 1))
        self.note1.modified = timezone.make_aware(datetime(2023, 1, 2))
        self.note2.created = timezone.make_aware(datetime(2023, 2, 1))
        self.note2.modified = timezone.make_aware(datetime(2023, 2, 2))
        self.note1.save()
        self.note2.save()

    def test_filter_by_notebook(self):
        filter_data = {'notebook': self.notebook1.id}
        note_filter = NoteFilter(filter_data, queryset=Note.objects.all())
        filtered_notes = note_filter.qs
        self.assertEqual(filtered_notes.count(), 2)
        self.assertEqual(filtered_notes[0], self.note1)

    def test_filter_by_tag(self):
        filter_data = {'tags': 'Tag1'}
        note_filter = NoteFilter(filter_data, queryset=Note.objects.all())
        filtered_notes = note_filter.qs
        self.assertEqual(filtered_notes.count(), 1)
        self.assertEqual(filtered_notes[0], self.note1)

    def test_sort_by_created(self):
        filter_data = {'sort_by_created': 'created'}
        note_filter = NoteFilter(filter_data, queryset=Note.objects.all())
        filtered_notes = note_filter.qs
        self.assertEqual(filtered_notes[0], self.note1)
        self.assertEqual(filtered_notes[1], self.note2)

    def test_sort_by_modified(self):
        filter_data = {'sort_by_modified': 'modified'}
        note_filter = NoteFilter(filter_data, queryset=Note.objects.all())
        filtered_notes = note_filter.qs
        self.assertEqual(filtered_notes[0], self.note1)
        self.assertEqual(filtered_notes[1], self.note2)

    def test_filter_by_created_after(self):
        filter_data = {'created_after': '2023-01-15'}
        note_filter = NoteFilter(filter_data, queryset=Note.objects.all())
        filtered_notes = note_filter.qs
        self.assertEqual(filtered_notes.count(), 1)
        self.assertEqual(filtered_notes[0], self.note2)

    def test_filter_by_modified_before(self):
        filter_data = {'modified_before': '2023-02-01'}
        note_filter = NoteFilter(filter_data, queryset=Note.objects.all())
        filtered_notes = note_filter.qs
        self.assertEqual(filtered_notes.count(), 0)


class NotebookFilterTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.notebook1 = Notebook.objects.create(author=self.user, title='Notebook 1', slug='notebook-1')
        self.notebook2 = Notebook.objects.create(author=self.user, title='Notebook 2', slug='notebook-2')
        self.notebook1.created = timezone.make_aware(datetime(2023, 1, 1))
        self.notebook2.created = timezone.make_aware(datetime(2023, 2, 1))
        self.notebook1.save()
        self.notebook2.save()

    def test_filter_by_title(self):
        filter_data = {'title': 'Notebook 1'}
        notebook_filter = NotebookFilter(filter_data, queryset=Notebook.objects.all())
        filtered_notebooks = notebook_filter.qs
        self.assertEqual(filtered_notebooks.count(), 1)
        self.assertEqual(filtered_notebooks[0], self.notebook1)

    def test_sort_by_created(self):
        filter_data = {'sort_by_created': 'created'}
        notebook_filter = NotebookFilter(filter_data, queryset=Notebook.objects.all())
        filtered_notebooks = notebook_filter.qs
        self.assertEqual(filtered_notebooks[0], self.notebook1)
        self.assertEqual(filtered_notebooks[1], self.notebook2)

    def test_sort_by_modified(self):
        filter_data = {'sort_by_modified': 'modified'}
        notebook_filter = NotebookFilter(filter_data, queryset=Notebook.objects.all())
        filtered_notebooks = notebook_filter.qs
        self.assertEqual(filtered_notebooks[0], self.notebook1)
        self.assertEqual(filtered_notebooks[1], self.notebook2)

    def test_filter_by_created_after(self):
        filter_data = {'created_after': '2023-01-15'}
        notebook_filter = NotebookFilter(filter_data, queryset=Notebook.objects.all())
        filtered_notebooks = notebook_filter.qs
        self.assertEqual(filtered_notebooks.count(), 1)
        self.assertEqual(filtered_notebooks[0], self.notebook2)

    def test_filter_by_modified_before(self):
        filter_data = {'modified_before': '2023-02-01'}
        notebook_filter = NotebookFilter(filter_data, queryset=Notebook.objects.all())
        filtered_notebooks = notebook_filter.qs
        self.assertEqual(filtered_notebooks.count(), 0)
