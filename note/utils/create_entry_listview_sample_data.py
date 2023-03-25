"""
ListView の Pagination を学ぶためのサンプルです。

Tag, Entry をすべて削除してから、Tag は 3 つ、Entry は 100 件を作成します。

Django Console で以下を実行してください。

>>> from note.utils.create_entry_listview_sample_data import create_entry_listview_sample_data
>>> create_entry_listview_sample_data()
"""
import random

from django.contrib.auth import get_user_model

from note.models import Tag, Entry, Comment

User = get_user_model()


def create_entry_listview_sample_data():
    """
    Tag, Entry をすべて削除してから、Tag は 3 つ、Entry は 100 件を作成します。
    Entry には、CommentがEntryごとに1-5件ついています。
    """
    Tag.objects.all().delete()
    Entry.objects.all().delete()
    Comment.objects.all().delete()

    tag1 = Tag.objects.create(id=1, name='tag1', slug='tag1')
    tag2 = Tag.objects.create(id=2, name='tag2', slug='tag2')
    tag3 = Tag.objects.create(id=3, name='tag3', slug='tag3')

    user = User.objects.last()

    k = 1
    for i in range(1, 101):
        entry = Entry.objects.create(
            id=i,
            title='title{}'.format(i),
            body='entry_body{}'.format(i),
            user=user,
        )
        if i % 3 == 0:
            entry.tags.set([tag1, ])
        elif i % 3 == 1:
            entry.tags.set([tag2, ])
        else:
            entry.tags.set([tag3, ])
        for j in range(random.randint(1, 5)):
            Comment.objects.create(
                id=k,
                entry=entry,
                body='comment_body{}'.format(k),
                user=user,
            )
            k += 1

    print('Tag, Entry をすべて削除してから、Tag は 3 つ、Entry は 100 件を作成しました。')
