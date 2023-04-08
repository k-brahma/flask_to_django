from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.urls import path
from django.views.generic import TemplateView

from main.views import base_views, sample_views, class_based_views, as_view_samples, error_views


def sample01_func(request):
    """
    views.py にある必要はない
    view 関数は、第一引数に request を取る。そして、 HttpResponse オブジェクトを返す。
    """
    # if request.user.is_anonymous:
    #     return HttpResponse('sample01_func はログインしていないと見れません。')
    # else:
    #     return HttpResponse('sample01_func はログインしていると見れます。')
    return HttpResponse('<h1>sample1_funcに呼ばれました！</h1>')


def sample02_func_redirect(request):
    """
    HttpResponse オブジェクトの一例として、 HttpResponseRedirect を紹介するl
    """
    messages.info(request, 'sample02_func からリダイレクトされてきました！')
    return HttpResponseRedirect(resolve_url('main:thanks'))


app_name = 'main'

urlpatterns = [
    path('', base_views.TopView.as_view(), name='index'),
    path('about/', base_views.AbountView.as_view(), name='about'),
    path('reference/', base_views.ReferenceView.as_view(), name='reference'),
    path('buy_thanks/', base_views.ThanksView.as_view(), name='thanks'),

    # 以下は、 view 関数についての解説用のサンプル
    # path は、以下の書式で記述する
    #   path(route, view, kwargs=None, name=None)
    #
    # 第二引数は、極論すれば、カラブルでさえあればよい。(引数として request を受け取るカラブルであればよい)

    ## urls.py に記述した関数
    path('sample01/', sample01_func, name='sample01'),
    path('sample02/', sample02_func_redirect, name='sample02_func_redirect'),

    ## class based view の話のための事前準備
    path('sample11/', sample_views.SampleClass11(), name='sample11'),
    path('sample12/', sample_views.SampleClass12().my_method, name='sample12'),
    path('sample13/', sample_views.SampleClass13.hoge(), name='sample13'),
    path('sample14/', sample_views.SampleClass14.fuga(), name='sample14'),

    path('sample15/', sample_views.SampleClass15().as_view(), name='sample15'),

    path('sample16/', sample_views.sample16, name='sample16'),

    ## class based view の各種挙動を確かめるためのサンプル
    path('sample21/', class_based_views.SimpleView.as_view(), name='sample21'),
    path('sample22/', class_based_views.MethodNowImplementedView.as_view(), name='sample22'),
    path('sample23/', class_based_views.MethoNotAllowedView.as_view(), name='sample23'),

    ## as_view() を view のモジュール内で呼び出してから、それを path に渡してもよい
    path('sample31/', as_view_samples.func_31, name='sample21'),
    path('sample32/', as_view_samples.func_32, name='sample22'),
    path('sample33/', as_view_samples.func_33, name='sample23'),

    ## エラーのハンドリング
    path('normal_403/', error_views.normal_403, name='normal_403'),
    path('normal_403_class/', error_views.normal_403_class, name='normal_403_class'),
    path('raise_403/', error_views.raise_403, name='raise_403'),

    path('normal_400/', error_views.normal_400, name='normal_400'),
    path('normal_400_class/', error_views.normal_400_class, name='normal_400_class'),
    path('raise_400/', error_views.raise_400, name='raise_400'),

    path('raise_500/', error_views.raise_500, name='raise_500'),

    path('auth_check/', TemplateView.as_view(template_name='auth_check.html'), name='authed'),
]
