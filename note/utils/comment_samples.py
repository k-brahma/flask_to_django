"""
Comment モデルの追加/更新サンプル

最初の実行時に、 Entry モデルをすべて削除します。
Comment モデルでは、
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE) としています。
ですので、Entry オブジェクト削除時に、関連する Comment オブジェクトも削除されます。

django console から、以下のコマンドで実行してください。

from note.utils.comment_samples import delete_create_update_comments
delete_create_update_comments()
"""

from django.contrib.auth import get_user_model
from note.models import Entry, Comment


def delete_create_update_comments():
    """
    Comment モデルの追加/更新サンプル

    User モデルのインスタンスが最低ひとつあるという前提
    """
    comments = Comment.objects.all()
    print(comments.count())  # 既存インスタンスの数

    entries = Entry.objects.all()
    print(entries.count())  # 既存インスタンスの数

    Entry.objects.all().delete()

    comments = Comment.objects.all()
    print(comments.count())  # 0

    entries = Entry.objects.all()
    print(entries.count())  # 0

    user = get_user_model().objects.first()

    # Entry オブジェクトを2つ作る
    entry1 = Entry.objects.create(user=user, title='タイトル1', body='本文1')
    entry2 = Entry.objects.create(user=user, title='タイトル2', body='本文2')

    # Comment オブジェクトを2つ作る
    comment1 = Comment.objects.create(user=user, entry=entry1, body='コメント1本文')
    print(comment1.id, comment1.user, comment1.entry, comment1.body)  # 数値, ユーザーインスタンス, エントリインスタンス, コメント本文

    comment2 = Comment(user=user, entry=entry1, body='コメント2本文')
    print(comment2.id, comment2.user, comment2.entry.title, comment2.body)  # None, ユーザーインスタンス, エントリインスタンス, コメント本文

    # save() メソッドで保存する
    comment2.save()
    print(comment2.id, comment2.user, comment2.entry.title, comment2.body)  # 数値, ユーザーインスタンス, エントリインスタンス, コメント本文

    # Comment オブジェクトを1つ更新する
    comment1.body = '更新されたコメント1本文'
    comment1.save()
    print(comment1.id, comment1.user, comment1.entry.title, comment1.body)  # 数値, ユーザーインスタンス, エントリインスタンス, コメント本文

    # Comment オブジェクトに関連付けられた Entry オブジェクトを変更する
    comment1.entry = entry2
    comment1.save()
    print(comment1.id, comment1.user, comment1.entry.title, comment1.body)  # 数値, ユーザーインスタンス, エントリインスタンス, コメント本文

    # Comment オブジェクトをすべて取得する
    comments = Comment.objects.all()
    print(comments.count())  # 2

    for comment in comments:
        # 数値, ユーザーインスタンス, エントリインスタンス, コメント本文
        print(comment.id, comment.user, comment.entry.title, comment.body)
