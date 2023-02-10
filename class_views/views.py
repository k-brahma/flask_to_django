from pprint import pprint

from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView, ListView, DetailView

from stock.models import Stock


class IndexView(TemplateView):
    template_name = 'class_views/index.html'


class TemplateViewWithContext(TemplateView):
    template_name = 'class_views/context.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'よろしくね！'

        my_dict = {'key1': 'hoge', 'key2': 'fuga', 'key3': 'piyo', }
        context['my_dict'] = my_dict

        my_list = ['foo', 'bar', 'baz', ]
        context['my_list'] = my_list

        return context


class TemplateViewMethod1(TemplateView):
    """
    属性で指定するほか、 get_foo というメソッドもたいてい実装されている。
    なんらかの事情で動的に値を決めたい場合には、メソッドを使うことになる。
    """

    def get_template_names(self):
        return ['class_views/context.html', ]


class TemplateViewMethod2(TemplateView):
    """
    属性で指定するほか、 get_foo というメソッドもたいてい実装されている。
    なんらかの事情で動的に値を決めたい場合には、メソッドを使うことになる。
    """

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['class_views/authenticated.html', ]
        else:
            return ['class_views/anonymous.html', ]


class RedirectSample1(RedirectView):
    # url の書き方 :
    # resolve_url : これを使うのがいちばん簡単
    # reverse     : 古い
    # reverse_lazy: 遅延読み込み(必要になるまで計算されない)
    url = reverse_lazy('class:top')


class RedirectSample2(RedirectView):
    # 301 リダイレクト: permanent
    # 302 リダイレクト: temporary
    url = reverse_lazy('class:top')
    permanent = True


class RedirectSample3(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse_lazy('class:authed')
        else:
            return reverse_lazy('class:anonymous')


class ItemListView1(ListView):
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ItemListView2(ListView):
    model = Stock
    template_name = 'class_views/item_list.html'


class ItemListView3(ListView):
    template_name = 'class_views/item_list.html'

    def get_queryset(self):
        """
        「一定の条件にマッチしないときは出力しない」とかいうときは、たいていこれ(頻出！)
        たとえば:
            投稿者しか見られない
            ログインユーザしか見られない
        """
        return Stock.objects.filter(sell__gte=150)


class ItemListView4(ListView):
    allow_empty = False  # 該当するものがない場合は404

    def get_queryset(self):
        return Stock.objects.filter(sell__gte=1500000)


class ItemDetailView1(DetailView):
    model = Stock

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ItemDetailView2(DetailView):
    model = Stock
    template_name = 'class_views/item_detail.html'


class ItemDetailView3(DetailView):
    template_name = 'class_views/item_detail.html'

    def get_queryset(self):
        """
        「一定の条件にマッチしないときは出力しない」とかいうときは、たいていこれ(頻出！)
        たとえば:
            投稿者しか見られない
            ログインユーザしか見られない
        """
        return Stock.objects.filter(sell__gte=150)


class ItemDetailView4(DetailView):
    def get_object(self, queryset=None):
        """
        以下では、常に、 pk=1 のオブジェクトを取得する(あまりよいサンプルではないです)
        """
        return Stock.objects.get(pk=1)
