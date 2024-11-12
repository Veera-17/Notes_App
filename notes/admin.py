from django.contrib import admin
from .models import Note, Notebook

@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created', 'modified')
    search_fields = ('title', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'created', 'modified', 'notebook')
    search_fields = ('title', 'author__username', 'content')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created',)