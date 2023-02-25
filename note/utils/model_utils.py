"""
モデルの更新をサポートする関数群

models.py に置くほどではないが、あると便利なものを置く。
あるいは、一時的に利用するために作り込むが、あとで破棄したいものを置いたりもする
"""

import csv
import pathlib

from django.conf import settings
from django.contrib.auth import get_user_model

from note.models import Entry


def update_etnries_from_csv(csv_file_path):
    """
    csvファイルから、エントリーを更新する

    使用例:
    >>> from note.utils.model_utils import update_etnries_from_csv
    >>> update_etnries_from_csv('note/fixtures/entry.csv')

    :param csv_file: csvファイルのパス
    :return: None
    """

    with pathlib.Path(settings.BASE_DIR / csv_file_path).open(mode='r', encoding='utf-8', newline='') as file:
        user = get_user_model().objects.first()  # このサンプルデータでは、面倒なので、最初のユーザーを使う
        reader = csv.DictReader(file, )
        for row in reader:
            Entry.objects.create(
                title=row['title'],
                body=row['body'],
                user=user,
            )
