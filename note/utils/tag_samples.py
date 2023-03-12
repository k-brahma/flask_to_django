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
    print(tag2.id, tag2.name, tag2.slug)  # None, ジャンゴ, django

    tag2.save()
    print(tag2.id, tag2.name, tag2.slug)  # 数値, ジャンゴ, django

    try:
        exvba_tag = Tag.objects.get(slug='pythonnnn')  # getは必ずあるという前提で使う。見つからないと例外が発生する
    except Tag.DoesNotExist as e:
        print('タグが見つからなかった場合はこの例外が発生する')
        raise e

    exvba_tag.name = 'エクセルVBA'
    exvba_tag.slug = 'excel-vba'
    exvba_tag.save()
    print(exvba_tag.id, exvba_tag.name, exvba_tag.slug)  # 数値, エクセルVBA, excel-vba
    print(tag1.id, tag1.name, tag1.slug)  # 変数 tag1 の中身は更新されていないので注意！

    tag1.refresh_from_db()
    print(tag1.id, tag1.name, tag1.slug)  # 変数 tag1 の中身は更新されていないので注意！

    tags = Tag.objects.all()
    print(tags.count())  # 2

    for tag in tags:
        print(tag.id, tag.name, tag.slug)
