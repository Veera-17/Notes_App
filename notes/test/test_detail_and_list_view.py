from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Notebook, Note
from taggit.models import Tag

class NotebookViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.notebook = Notebook.objects.create(author=self.user, title="Test Notebook", slug="test-notebook")

    def test_notebook_list_view(self):
        response = self.client.get(reverse('note:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/notebook_list.html')
        self.assertContains(response, 'Test Notebook')

    def test_notebook_detail_view(self):
        response = self.client.get(reverse('note:notebook_detail', args=[self.notebook.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html') 
        self.assertContains(response, 'Test Notebook')


class NoteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.notebook = Notebook.objects.create(author=self.user, title="Test Notebook", slug="test-notebook")
        self.note = Note.objects.create(author=self.user, notebook=self.notebook, title="Test Note", slug="test-note", content="This is a test note.")

    def test_note_list_view(self):
        response = self.client.get(reverse('note:notebook_detail', args=[self.notebook.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertContains(response, 'Test Note')

    def test_note_detail_view(self):
        response = self.client.get(reverse('note:note_detail', args=[self.note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertContains(response, 'Test Note')

    def test_note_detail_view_with_tag(self):
        tag = Tag.objects.create(name="test-tag")
        self.note.tags.add(tag)
        response = self.client.get(reverse('note:similar_note', args=[self.note.pk, tag.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')

    def test_note_detail_view_no_similar_notes(self):
        response = self.client.get(reverse('note:similar_note', args=[self.note.pk, 'nonexistent-tag']))
        self.assertEqual(response.status_code, 404)