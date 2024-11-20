from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Notebook, Note

class NotebookCreateUpdateAndDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.notebook = Notebook.objects.create(author=self.user, title='Test Notebook', slug='test-notebook')

    def test_create_notebook(self):
        response = self.client.post(reverse('notebook_create'), {'title': 'New Notebook'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Notebook.objects.filter(title='New Notebook', author=self.user).exists())

    def test_update_notebook(self):
        update_url = reverse('notebook_update', kwargs={'pk': self.notebook.pk})
        response = self.client.post(update_url, {'title': 'Updated Notebook Title'})
        self.assertEqual(response.status_code, 302)
        self.notebook.refresh_from_db()
        self.assertEqual(self.notebook.title, 'Updated Notebook Title')

    def test_delete_notebook(self):
        delete_url = reverse('notebook_delete', kwargs={'pk': self.notebook.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Notebook.objects.filter(pk=self.notebook.pk).exists())


class NoteCreateUpdateAndDeleteViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.notebook = Notebook.objects.create(author=self.user, title='Test Notebook', slug='test-notebook')
        self.note = Note.objects.create(
            author=self.user, notebook=self.notebook, title='Test Note', slug='test-note', content='Sample content'
        )

    def test_create_note(self):
        create_url = reverse('note_create')
        response = self.client.post(create_url, {
            'title': 'New Note',
            'content': 'New note content',
            'notebook': self.notebook.pk,
            'tags': 'test, django'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Note.objects.filter(title='New Note', author=self.user).exists())

    def test_update_note(self):
        update_url = reverse('note_update', kwargs={'pk': self.note.pk})
        response = self.client.post(update_url, {
            'title': 'Updated Note Title',
            'content': 'Updated content',
            'notebook': self.notebook.pk,
            'tags': 'updated, test'
        })
        self.assertEqual(response.status_code, 302)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Updated Note Title')
        self.assertEqual(self.note.content, 'Updated content')

    def test_delete_note(self):
        delete_url = reverse('note_delete', kwargs={'pk': self.note.pk})
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
