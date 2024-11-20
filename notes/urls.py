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
]
