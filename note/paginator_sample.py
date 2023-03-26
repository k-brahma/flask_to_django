"""
Django Console で以下を実行してください。

>>> from note.paginator_sample import paginator_demo
>>> paginator_demo()
"""

from django.core.paginator import Paginator


def paginator_demo():
    """
    paginator は、以下のような属性を有するオブジェクトにしかすぎない
    paginator オブジェクトから page オブジェクトを取得できる
    """
    item_names = [f'item_{index}' for index in range(1, 101)]

    paginator = Paginator(item_names, 5)
    page = paginator.page(3)

    # page の属性を取得する
    print(page.object_list)
    print(page.has_other_pages())
    print(page.has_next())
    print(page.has_previous())
    print(page.next_page_number())
    print(page.previous_page_number())
    print(page.start_index())
    print(page.end_index())

    # paginator の属性を取得する
    print(page.paginator.object_list)
    print(page.paginator.per_page)
    print(page.paginator.count)
    print(page.paginator.num_pages)
    print(page.paginator.page_range)
    page_strs = page.paginator.get_elided_page_range(10, )
    for page_str in page_strs:
        print(page_str)
