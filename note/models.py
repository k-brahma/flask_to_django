from django.conf import settings
from django.db import models
from django.urls import reverse


class Tag(models.Model):
    """
    Entry につけられるタグ。

    ひとつの Entry に複数つけられる。
    また、同じタグを複数の Entry につけることができる。

    unique=True のものフィールドの値は、同一モデル内で重複できない
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    """
    投稿 モデル

    tags は ManyToManyField なので、複数のタグをつけられるし、ひとつもなくても良い。
    settings.AUTH_USER_MODEL は、settings.py で定義したユーザーモデルを指す。
    AbstractBaseUser クラスを継承したユーザモデルは、この方法で指定する。
    """

    class Meta:
        ordering = ('created_dt',)
        verbose_name_plural = 'Entries'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    tags = models.ManyToManyField(Tag, blank=True, verbose_name='タグ')
    title = models.CharField(max_length=20, verbose_name='タイトル')
    body = models.TextField(verbose_name='投稿本文')

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """
        models.Model の get_absolute_url メソッドをオーバーライドすると、以下の2つの点で便利

        1. テンプレートで object.get_absolute_url で呼び出せる
        2. 管理画面に、そのオブジェクトのウェフページ上の URL を表示するリンクが表示される
        """
        return reverse('note:entry_detail', args=[self.id])


class Comment(models.Model):
    """
    コメント モデル

    Entry に対するコメント。
    """

    class Meta:
        ordering = ('created_dt',)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    body = models.TextField(verbose_name='コメント本文')

    created_dt = models.DateTimeField(auto_now_add=True)
    updated_dt = models.DateTimeField(auto_now=True)
