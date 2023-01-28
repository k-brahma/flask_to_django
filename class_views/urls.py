from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'class'

urlpatterns = [
    path('', TemplateView.as_view(template_name='class_views/index.html'), name='top'),
    path('index/', views.IndexView.as_view(), name='index'),
    path('context/', views.TemplateViewWithContext.as_view(), name='with_context'),
    path('method1/', views.TemplateViewMethod1.as_view(), name='get_template_names1'),
    path('method2/', views.TemplateViewMethod2.as_view(), name='get_template_names2'),

    path('authed/', TemplateView.as_view(template_name='class_views/authenticated.html'), name='authed'),
    path('anonymous/', TemplateView.as_view(template_name='class_views/anonymous.html'), name='anonymous'),

    path('r1/', views.RedirectSample1.as_view(), name='r1'),
    path('r2/', views.RedirectSample2.as_view(), name='r2'),
    path('r3/', views.RedirectSample3.as_view(), name='r3'),

    path('list1/', views.ItemListView1.as_view(), name='list1'),
    path('list2/', views.ItemListView2.as_view(), name='list2'),
    path('list3/', views.ItemListView3.as_view(), name='list3'),
    path('list4/', views.ItemListView4.as_view(), name='list4'),

    path('detail1/<int:pk>/', views.ItemDetailView1.as_view(), name='detail1'),
    path('detail2/<int:pk>/', views.ItemDetailView2.as_view(), name='detail2'),
    path('detail3/<int:pk>/', views.ItemDetailView3.as_view(), name='detail3'),
    path('detail4/<int:pk>/', views.ItemDetailView4.as_view(), name='detail4'),
]
