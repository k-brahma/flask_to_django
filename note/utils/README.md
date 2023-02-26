# note.utils について

以下の順序で動作確認/学習してください。

| 順序 | ファイル名                 | 説明               | 詳細                          |
|:---:|:----------------------|:-----------------|-----------------------------|
| 1 | tag_samples.py        | tag の作成、更新、削除    | 外部キーがない場合の例です。              |
| 2 | comment_samples.py    | commentの作成、更新、削除 | ForeignKey フィールドがある場合の例です。  |
| 3 | entry_samples.py      | entry の作成、更新、削除  | ManyToMany フィールドがある場合の例です。  |
| 4 | csv_import_samples.py | データのインポート        | CSV ファイルから値を読み出してモデルに投入します。 |
