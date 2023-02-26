"""
Tag モデルの追加/更新サンプル

最初の実行時に、 Tag モデルをすべて削除します。
それから、 Tag モデルのインスタンスを追加し、そして、更新します。

(Tag モデルのインスタンスがすべて削除されるので、Entry モデルのインスタンスのタグもすべて削除されます)

django console から、以下のコマンドで実行してください。

from note.utils.tag_samples import delete_create_update_tags
delete_create_update_tags()
"""

from note.models import Tag


def delete_create_update_tags():
    tags = Tag.objects.all()
    print(tags.count())  # 既存インスタンスの数

    Tag.objects.all().delete()

    tags = Tag.objects.all()
    print(tags.count())  # 0

    # objects.create() は、インスタンスを作成して保存する
    tag1 = Tag.objects.create(name='パイソン', slug='python')
    print(tag1.id, tag1.name, tag1.slug)  # 数値, パイソン, python

    # models.Model クラスのインスタンスを初期化。
    # その後、save() メソッドで保存する
    tag2 = Tag(name='ジャンゴ', slug='django')
    print(tag2.id, tag2.name, tag2.slug)  # None, ジャンゴ, djangos

    tag2.save()
    print(tag2.id, tag2.name, tag2.slug)  # 数値, ジャンゴ, django

    tag1.name = 'エクセルVBA'
    tag1.slug = 'excel-vba'
    tag1.save()
    print(tag1.id, tag1.name, tag1.slug)  # 数値, エクセルVBA, excel-vba

    tags = Tag.objects.all()
    print(tags.count())  # 2

    for tag in tags:
        print(tag.id, tag.name, tag.slug)
