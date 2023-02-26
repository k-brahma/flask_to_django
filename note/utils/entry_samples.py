"""
Entry モデルの追加/更新サンプル

最初の実行時に、 Tag モデル, Entry モデルをすべて削除します。
Comment モデルでは、
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE) としています。
ですので、Entry オブジェクト削除時に、関連する Comment オブジェクトも削除されます。

django console から、以下のコマンドで実行してください。

from note.utils.entry_samples import delete_create_update_entries
delete_create_update_entries()
"""

from django.contrib.auth import get_user_model
from note.models import Tag, Entry


def delete_create_update_entries():
    """
    Entry モデルの追加/更新サンプル

    User モデルのインスタンスが最低ひとつあるという前提
    """
    Tag.objects.all().delete()
    Entry.objects.all().delete()

    user = get_user_model().objects.first()

    # Tag オブジェクトを5つ作る
    tag1 = Tag.objects.create(id=1, name='パイソン', slug='python')
    tag2 = Tag.objects.create(id=2, name='ジャンゴ', slug='django')
    tag3 = Tag.objects.create(id=3, name='エクセルVBA', slug='excel-vba')
    tag4 = Tag.objects.create(id=4, name='エイチティーエムエル', slug='html')
    tag5 = Tag.objects.create(id=5, name='シーエスエス', slug='css')

    # ManyToManyField の追加は、本体がデータベースに保存されるまではできない
    # 故に、以下はOK
    entry1 = Entry.objects.create(user=user, title='タイトル1', body='本文1')
    entry1.tags.set([tag1, tag2, ])

    tags = entry1.tags.all()
    for tag in tags:
        print(tag.id, tag.name, tag.slug)

    # 故に、以下はNG
    # entry3 = Entry(user=user, title='タイトル1', body='本文1', tags=[tag1, tag2])

    # 以下はOK(entry2 が保存されたあとだから)
    entry2 = Entry(user=user, title='タイトル2', body='本文2')
    entry2.save()
    entry2.tags.set([tag3, tag4, ])

    tags = entry1.tags.all()
    for tag in tags:
        print(tag.id, tag.name, tag.slug)

    # ManyToMany フィールドのメソッドは、以下の4つ
    # add, set, remove, clear
    # いずれも、実行直後に即座にデータベースは更新される。なので、 save() は不要。

    # add() メソッドは、すでに設定されているタグに、新しいタグを追加する
    # ただし、すでに設定されているのと同じタグを指定しても無視される
    # 以下では、tag3, tag4 が設定されていたところに、さらに、tag4, tag5 を追加しようとする
    # ただし、tag4 はすでに設定されているので、 tag3, tag4, tag5 となる
    entry2.tags.add(tag4, tag5, )

    tags = entry2.tags.all()
    for tag in tags:
        print(tag.id, tag.name, tag.slug)

    # set() メソッドは、すべてのタグを削除して、新しいタグを追加する
    # add の場合と異なり、引数はリスト等の iterable なので注意！
    # 以下では、すでに tag3, tag4, tag5 が設定されていたところ、 tag1, tag2, tag3 に変更する
    entry2.tags.set([tag1, tag2, tag3])

    tags = entry2.tags.all()
    for tag in tags:
        print(tag.id, tag.name, tag.slug)

    # remove() メソッドは、すでに設定されているタグから、指定したタグを削除する
    # 以下では、すでに tag1, tag2, tag3 が設定されていたところ、 tag1, tag5 を削除しようとする
    # ただし、 tag5 はもともと設定されていないので、 tag2, tag3 となる
    entry2.tags.remove(tag1, tag5, )

    tags = entry2.tags.all()
    for tag in tags:
        print(tag.id, tag.name, tag.slug)

    # clear() メソッドは、すべてのタグを削除する
    # 以下では、すでに tag1, tag2, tag3 が設定されていたところ、すべて削除する
    entry2.tags.clear()

    tags = entry2.tags.all()
    print(tags.count())
