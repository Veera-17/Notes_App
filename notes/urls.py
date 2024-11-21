from django.contrib import admin
from notes import views
from django.urls import path

urlpatterns = [
    path('', views.landing_page, name='home'),
    path('notebook/list', views.NotebookListView.as_view(), name='notebook_list'),
    path('note/list/', views.note_list_view, name='note_list'),
    path('note/list/<int:pk>/', views.note_list_view, name='note_list_filtered'),
    path('note/<int:pk>/', views.note_detail, name='note_detail'),
    path('note/<int:pk>/<slug:tag_slug>/', views.note_detail, name='similar_note'),
    path('notebook/add/', views.notebook_create, name='notebook_create'),
    path('notebook/<int:pk>/update/', views.NotebookUpdateView.as_view(), name='notebook_update'),
    path('notebook/<int:pk>/delete/', views.NotebookDeleteView.as_view(), name='notebook_delete'),
    path('note/create/', views.note_create, name='note_create'),
    path('note/update/<int:pk>/', views.note_update, name='note_update'),
    path('note/delete/<int:pk>/', views.note_delete, name='note_delete'),
]
