"""
path 生成時の第二引数は、カラブルでさえあればよい
(ただし、 __init__ メソッドは戻り値を返さないので使えないが)
"""
from django.http import HttpResponse


# クラスインスタンスでもOK
class SampleClass11:
    """
    call で実装してみた
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, request):
        return HttpResponse('<h1>SampleClass11に呼ばれました！</h1>')


# インスタンスメソッドでもOK
class SampleClass12:
    """
    my_method で実装してみた
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def my_method(self, request):
        return HttpResponse('<h1>SampleClass12に呼ばれました！</h1>')


class SampleClass13:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def my_method(cls, request):
        return HttpResponse('<h1>SampleClass13に呼ばれました！</h1>')

    @classmethod
    def hoge(cls):
        """
        このメソッドは、 my_method を返す(戻り値は callable であって、 my_method の戻り値ではないので注意！)
        """
        return cls.my_method


class SampleClass14:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def fuga(self):
        """
        このメソッドは、 内部で _inner_func という関数を作り、それを戻り値にする
        """

        def _inner_func(request):
            return HttpResponse('<h1>SampleClass14に呼ばれました！</h1>')

        return _inner_func


class SampleClass15:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @classmethod
    def as_view(self):
        """
        このメソッドは、 内部で _inner_func という関数を作り、それを戻り値にする
        """

        def _inner_func(request):
            return HttpResponse('<h1>SampleClass14に呼ばれました！</h1>')

        return _inner_func


# 以下は、本筋から逸れるが...いちおう紹介
class SampleClass16:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def my_method(self, request):
        return HttpResponse('<h1>SampleClass16に呼ばれました！</h1>')

    def fuga(self):
        """
        このメソッドは、 my_method を返す(戻り値は callable であって、 my_method の戻り値ではないので注意！)
        """
        return self.my_method


# モジュール内でここまで処理しても良い
sample16 = SampleClass16().fuga()
