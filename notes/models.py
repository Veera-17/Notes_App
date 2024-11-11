from django.db import models
from django.utils.text import slugify
from markdown import markdown
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from model_utils.models import TimeStampedModel

class Notebook(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notebooks')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=False, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'slug'], name='unique_noteBook_slug')
        ]

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        pass

def get_default_notebook(author):
        notebook, created = Notebook.objects.get_or_create(
            author=author, title="Uncategorized",
            defaults={'slug': 'uncategorized'}
        )
        return notebook

class Note(TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    notebook = models.ForeignKey(Notebook, null=True, blank=True, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=False, blank=True)
    content = models.TextField()  
    tags = TaggableManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'slug'], name='unique_note_slug')
        ]

    def get_absolute_url(self):
        pass

    def get_message_as_markdown(self):
        """ Renders the Markdown content to HTML with escaped tags for safety """
        return mark_safe(markdown(self.content, safe_mode='escape'))

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.notebook is None:
            self.notebook = get_default_notebook(self.author)
        super().save(*args, **kwargs)
