from django.contrib import admin
from notes import views
from django.urls import path

app_name = 'note'
urlpatterns = [
    path('', views.NotebookListView.as_view(), name='home'),
    path('notebooks/<int:pk>/', views.NoteListView.as_view(), name='notebook_detail'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/<int:pk>/<slug:tag_slug>/', views.note_detail, name='similar_note'),
]
