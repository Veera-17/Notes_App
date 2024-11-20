from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Notebook, Note
from taggit.models import Tag

class NotebookViewTests(TestCase):
    
    def setUp(self):
        """Setup test user and notebooks"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.notebook1 = Notebook.objects.create(author=self.user, title='Notebook 1', slug='notebook-1')
        self.notebook2 = Notebook.objects.create(author=self.user, title='Notebook 2', slug='notebook-2')

    def test_notebook_list_view(self):
        """Test the NotebookListView returns the correct context and requires login"""
        url = reverse('notebook_list')
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=' + url)
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/notebook_list.html')
        self.assertIn(self.notebook1.title, str(response.content))
        self.assertIn(self.notebook2.title, str(response.content))

class NoteViewTests(TestCase):
    
    def setUp(self):
        """Setup test user, notebooks, notes, and tags"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.notebook1 = Notebook.objects.create(author=self.user, title='Notebook 1', slug='notebook-1')
        self.notebook2 = Notebook.objects.create(author=self.user, title='Notebook 2', slug='notebook-2')
        self.note1 = Note.objects.create(
            author=self.user,
            title='Note 1',
            slug='note-1',
            content='Content of note 1',
            notebook=self.notebook1
        )
        self.note2 = Note.objects.create(
            author=self.user,
            title='Note 2',
            slug='note-2',
            content='Content of note 2',
            notebook=self.notebook2
        )
        self.tag = Tag.objects.create(name='Tag1')
        self.note1.tags.add(self.tag)
        self.note2.tags.add(self.tag)
        
    def test_note_list_view(self):
        """Test that notes are listed correctly on the note list page"""
        url = reverse('note_list')
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=' + url)
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertIn(self.note1.title, str(response.content))
        self.assertIn(self.note2.title, str(response.content))

    def test_note_list_filtered_view(self):
        """Test that notes are filtered by notebook"""
        url = reverse('note_list_filtered', args=[self.notebook1.pk])
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=' + url)
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertIn(self.note1.title, str(response.content))
        self.assertNotIn(self.note2.title, str(response.content))

    def test_note_detail_view(self):
        """Test that note detail page renders correctly"""
        url = reverse('note_detail', args=[self.note1.pk])
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=' + url)
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertIn(self.note1.title, str(response.content))
        self.assertIn(self.note1.content, str(response.content))

    def test_note_detail_view_with_tag(self):
        """Test that note detail page shows similar notes when tag is present"""
        url = reverse('similar_note', args=[self.note1.pk, self.tag.slug])
        response = self.client.get(url)
        self.assertRedirects(response, '/account/login/?next=' + url)
        self.client.login(username='testuser', password='password')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertIn(self.note1.title, str(response.content))
        self.assertIn(self.note2.title, str(response.content))

class NoteTagViewTests(TestCase):
    
    def setUp(self):
        """Setup test user, notebooks, notes, tags, and login"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.notebook1 = Notebook.objects.create(author=self.user, title='Notebook 1', slug='notebook-1')
        self.notebook2 = Notebook.objects.create(author=self.user, title='Notebook 2', slug='notebook-2')
        self.note1 = Note.objects.create(
            author=self.user,
            title='Note 1',
            slug='note-1',
            content='Content of note 1',
            notebook=self.notebook1
        )
        self.note2 = Note.objects.create(
            author=self.user,
            title='Note 2',
            slug='note-2',
            content='Content of note 2',
            notebook=self.notebook2
        )
        self.tag1 = Tag.objects.create(name='Tag1')
        self.tag2 = Tag.objects.create(name='Tag2')
        self.note1.tags.add(self.tag1)
        self.note2.tags.add(self.tag2)
        self.client.login(username='testuser', password='password')

    def test_note_has_tag(self):
        """Test that notes are correctly tagged"""
        self.assertIn(self.tag1, self.note1.tags.all())
        self.assertIn(self.tag2, self.note2.tags.all())

    def test_note_list_view_with_tag_filter(self):
        """Test that the note list view filters notes by tag"""
        self.note1.tags.add(self.tag1)
        self.note2.tags.add(self.tag1)
        url = reverse('note_list') + f'?tag={self.tag1.slug}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_list.html')
        self.assertIn(self.note1.title, str(response.content))
        self.assertIn(self.note2.title, str(response.content))

    def test_note_detail_view_with_tag(self):
        """Test that the note detail page shows similar notes based on the tag"""
        self.note1.tags.add(self.tag1)
        self.note2.tags.add(self.tag1)
        url = reverse('similar_note', args=[self.note1.pk, self.tag1.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/note_detail.html')
        self.assertIn(self.note1.title, str(response.content))
        self.assertIn(self.note2.title, str(response.content))
