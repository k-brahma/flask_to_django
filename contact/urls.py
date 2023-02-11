from django.urls import path

from . import views

app_name = 'contact'
urlpatterns = [
    # 総合リンク
    path('', views.ContactTopView.as_view(), name='top'),

    # as_foo 系の出力
    path('div/', views.ContactFormAsDivView.as_view(), name='as_div'),
    path('p/', views.ContactFormAsParagraphView.as_view(), name='as_p'),
    path('table/', views.ContactFormAsTableView.as_view(), name='as_table'),
    path('ul/', views.ContactFormAsUnorderedListView.as_view(), name='as_ul'),

    # fields 系の出力
    path('iter/', views.ContactFieldsIterateView.as_view(), name='iter'),
    path('each/', views.ContactFieldsEachView.as_view(), name='each'),

    # フォームのバインド
    path('bound/', views.ContactFormWithDataView.as_view(), name='with_data'),

    # post の具体的な処理
    path('post/', views.ContactFormWithPost.as_view(), name='post'),
    path('method/', views.ContactFormWithPostMethod.as_view(), name='method'),
    path('form_view/', views.ContactFormView.as_view(), name='form_view'),

    # ファイルアップロードのサンプル
    path('file/', views.FileFormView.as_view(), name='file'),

    # csrf のサンプル
    path('csrf/', views.CSRFSampleView.as_view(), name='csrf'),
    path('csrf_script/', views.CSRFScriptSampleView.as_view(), name='csrf_script'),
]
