from django.http import HttpResponse
from django.views import View


class SimpleView(View):
    """
    正常系
    """

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     return super().dispatch(request, *args, **kwargs)
        # else:
        #     return HttpResponse('<h1>ログインしてください！</h1>')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>SimpleViewに呼ばれました！</h1>')


class MethodNowImplementedView(View):
    """
    get メソッド が実装されていない。
    405 Method Not Allowed が返る
    """

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     return HttpResponse('<h1>MethodNowImplementedViewに呼ばれました！</h1>')


class MethoNotAllowedView(View):
    """
    http_method_names を上書きして、 get メソッドだけを無効にする
    この場合も、 405 Method Not Allowed が返る
    """
    http_method_names = ['post', 'put', 'patch', 'delete', 'head', 'options', 'trace']  # 'get' がない

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>MethoNotAllowedViewに呼ばれました！</h1>')
