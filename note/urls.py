from django.urls import path

from . import views

app_name = 'note'
urlpatterns = [
    path('', views.EntryListView.as_view(), name='index'),
    path('create/', views.EntryCreateView.as_view(), name='entry_create'),
    path('tag/<slug:tag>/', views.EntryTagListView.as_view(), name='tag'),
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),
    path('updte/<int:pk>/', views.EntryUpdateView.as_view(), name='entry_update'),
    path('delete/<int:pk>/', views.EntryDeleteView.as_view(), name='entry_delete'),
]
