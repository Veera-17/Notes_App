from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Notebook, Note
from django.utils.text import slugify
from django.db import IntegrityError
import time
from django.core.exceptions import ValidationError

class NotebookModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.title = "Test Title" 
        self.slug = slugify(self.title)  
        self.notebook = Notebook.objects.create(author=self.user, title=self.title, slug=self.slug)

    def test_notebook_slug_equals_title_slugified(self):
        title = self.notebook.title
        slug = slugify(title)
        self.assertEqual(slug, 'test-title')

    def test_unique_notebook_title_for_same_user(self):
        self.title = "Duplicate Title"
        self.slug = slugify(self.title)
        Notebook.objects.create(author=self.user, title=self.title, slug=self.slug)

        with self.assertRaises(IntegrityError):
            Notebook.objects.create(author=self.user, title=self.title, slug=self.slug)

    def test_duplicate_notebook_title_for_different_users(self):
        notebook1 = Notebook.objects.create(author=self.user, title='Common Title')
        user2 = User.objects.create_user(username='anotheruser', password='password')
        notebook2 = Notebook.objects.create(author=user2, title='Common Title')
        self.assertEqual(notebook2.title, notebook1.title)

    def test_modified_field_updates_on_save(self):
        original_modified_time = self.notebook.modified
        time.sleep(1) 
        self.notebook.title = "Updated Test Notebook"
        self.notebook.save()
        self.assertNotEqual(self.notebook.modified, original_modified_time)
        self.assertGreater(self.notebook.modified, original_modified_time)

    def test_author_field_is_required(self):
        notebook = Notebook(title="Test Notebook", slug="test-notebook")
        try:
            notebook.full_clean() 
            self.fail("ValidationError not raised") 
        except ValidationError as e:
            self.assertIn('author', e.message_dict)


class NoteModelTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.notebook_title = "Test Notebook"
        self.notebook_slug = slugify(self.notebook_title)
        self.notebook = Notebook.objects.create(author=self.user, title=self.notebook_title, slug=self.notebook_slug)
        self.note_title = "Test Note"
        self.note_slug = slugify(self.note_title)
        self.note = Note.objects.create(
            author=self.user, 
            notebook=self.notebook, 
            title=self.note_title, 
            slug=self.note_slug,
            content="This is a test note."
        )
    
    def test_note_slug_equals_title_slugified(self):
        title = self.note.title
        slug = slugify(title)
        self.assertEqual(self.note.slug, slug)

    def test_note_author_is_required(self):
        note_without_author = Note(notebook=self.notebook, title="Test Note Without Author", slug="test-note-without-author", content="Content")
        try:
            note_without_author.full_clean()
            self.fail("ValidationError not raised")
        except ValidationError as e:
            self.assertIn('author', e.message_dict)

    def test_unique_note_title_for_same_user(self):
        Note.objects.create(
            author=self.user, 
            notebook=self.notebook, 
            title="Unique Title", 
            slug="unique-title", 
            content="Test content"
        )

        with self.assertRaises(IntegrityError):
            Note.objects.create(
                author=self.user, 
                notebook=self.notebook, 
                title="Unique Title", 
                slug="unique-title", 
                content="Test content"
            )

    def test_duplicate_note_title_for_different_users(self):
        notebook = Notebook.objects.create(author=self.user, title="Common Title", slug=slugify("Common Title"))
        note1 = Note.objects.create(author=self.user, notebook=notebook, title="Common Title", slug=slugify("Common Title"), content="Note 1 content")
        user2 = User.objects.create_user(username="anotheruser", password="password")
        notebook2 = Notebook.objects.create(author=user2, title="Common Title", slug=slugify("Common Title"))
        note2 = Note.objects.create(author=user2, notebook=notebook2, title="Common Title", slug=slugify("Common Title"), content="Note 2 content")
        self.assertEqual(note1.title, note2.title) 
        self.assertNotEqual(note1.author, note2.author)

    def test_note_modified_field_updates_on_save(self):
        original_modified_time = self.note.modified
        time.sleep(1) 
        self.note.content = "Updated test note content."
        self.note.save()
        self.assertNotEqual(self.note.modified, original_modified_time)
        self.assertGreater(self.note.modified, original_modified_time)

    def test_note_with_default_notebook(self):
        new_note = Note.objects.create(author=self.user, title="Test Note With Default Notebook", slug="test-note-default", content="Test content")
        self.assertEqual(new_note.notebook.title, "Uncategorized")