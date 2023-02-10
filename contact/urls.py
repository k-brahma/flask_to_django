from django.urls import path

from . import views

app_name = 'contact'
urlpatterns = [
    path('', views.ContactTopView.as_view(), name='top'),
    path('div/', views.ContactFormAsDivView.as_view(), name='as_div'),
    path('p/', views.ContactFormAsParagraphView.as_view(), name='as_p'),
    path('table/', views.ContactFormAsTableView.as_view(), name='as_table'),
    path('ul/', views.ContactFormAsUnorderedListView.as_view(), name='as_ul'),

    path('bound/', views.ContactFormWithDataView.as_view(), name='with_data'),
    path('post/', views.ContactFormWithPost.as_view(), name='post'),
    path('method/', views.ContactFormWithPostMethod.as_view(), name='method'),
    path('form_view/', views.ContactFormView.as_view(), name='form_view'),
]
