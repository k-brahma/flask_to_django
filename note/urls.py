from django.urls import path

from . import views

app_name = 'note'
urlpatterns = [
    # list views
    path('', views.EntryListView.as_view(), name='index'),
    path('tag/<slug:tag>/', views.EntryTagListView.as_view(), name='tag'),

    # entry list views with pagination
    path('page/', views.EntryListPaginationView.as_view(), name='page'),
    path('elided/', views.EntryListViewPaginationElidedView.as_view(), name='elided'),

    # detail views
    path('entry/<int:pk>/', views.EntryDetailView.as_view(), name='entry_detail'),

    # 様々な create views
    path('create_view/', views.CreateNormalView.as_view(), name='entry_create_view'),
    path('create_formview/', views.CreateFormView.as_view(), name='entry_create_formview'),
    path('create/', views.EntryCreateView.as_view(), name='entry_create'),

    # 様々な update views
    path('update_view/<int:pk>/', views.UpdateNormalView.as_view(), name='entry_update_view'),
    path('update_formview/<int:pk>/', views.UpdateFormView.as_view(), name='entry_update_formview'),
    path('update/<int:pk>/', views.EntryUpdateView.as_view(), name='entry_update'),

    # 様々な delete views
    path('delete_view/<int:pk>/', views.DeleteNormalView.as_view(), name='entry_delete_view'),
    path('delete/<int:pk>/', views.EntryDeleteView.as_view(), name='entry_delete'),

    # select_related, prefetch_related sample views
    path('comment/', views.CommentListView.as_view(), name='comment_list'),
    path('user/<int:pk>/', views.UserEntryListView.as_view(), name='user'),
]
