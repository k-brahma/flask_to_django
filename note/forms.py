from django import forms

from note.models import Entry, Comment


class EntryForm(forms.ModelForm):
    confirm = forms.BooleanField(  # モデルにないフィールド
        label='利用規約に同意します',
        required=True,
        error_messages={'required': '利用規約に同意してもらえないと受け付けられません', }
    )

    class Meta:
        model = Entry
        fields = ('title', 'body', 'tags',)

        widgets = {  # 出力される HTML をカスタマイズ
            'title': forms.TextInput(attrs={'size': 80, 'placeholder': 'タイトルを入力してください', 'class': 'color-lightgreen'}),
            'body': forms.Textarea(attrs={'cols': 80, 'rows': 15, 'placeholder': '何文字書いてもらっても構いません'}),
        }

        labels = {  # 出力される HTML のラベル部分をカスタマイズ
            'title': 'タイトル',
            'body': '投稿本文',
            'tags': 'タグ',
        }

        help_texts = {  # 出力される HTML の help text をカスタマイズ
            'title': '簡潔に書いてください',
            'body': '読む人が疲れない程度の分量にとどめてください。',
            'tags': 'タグをつけてもらうと、分類しやすいので助かります！',
        }

        error_messages = {  # バリデーションエラー時のメッセージをカスタマイズ
            'title': {'max_length': 'タイトルがの長さが非常識極まりないです！', },
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
