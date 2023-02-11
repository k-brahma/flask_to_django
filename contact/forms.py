from django.forms import (
    forms,
    IntegerField,
    EmailField,
    Textarea,
    CharField,
    DateTimeField,
    BooleanField,
    FileField,
    ChoiceField,
    ValidationError, HiddenInput
)
from django.utils import timezone


class ContactForm(forms.Form):
    """ 様々なタイプのフィールドを紹介します """
    score = IntegerField(label='スコア', min_value=0, max_value=100, help_text='0点から100点のどこですか。')
    name = CharField(label='お名前', max_length=10, help_text='10文字以内で入力してください。')
    email = EmailField(label='メールアドレス', help_text='必須ではありません', required=False)
    message = CharField(label='メッセージ', widget=Textarea, help_text='言いたいことを思う存分書いてください。')
    dt = DateTimeField(label='日時', help_text='日時を入力してください。', initial='2023-02-12 09:15:12')
    is_claim = BooleanField(label='クレーム', required=False, help_text='クレームですか？')
    contact_reason = ChoiceField(label='お問い合わせの理由', choices=[('1', '質問'), ('2', '感想'), ('3', 'その他')])

    # clean_foo というメソッドを定義すると、 foo フィールドのバリデーションを行うことができます。
    def clean_email(self):
        email = self.cleaned_data['email']
        if email == 'info@pc5bai.com':
            raise ValidationError('このメールアドレスは使用できません。')
        return email

    def clean_dt(self):
        dt = self.cleaned_data['dt']
        if dt > timezone.now():
            raise ValidationError('未来の日付は入力できません。')
        return dt

    # clean メソッドを定義すると、全フィールドのバリデーションを行うことができます。
    # 実行のタイミングは、各フィールドのバリデーションが終わった後です。
    def clean(self):
        cleaned_data = super().clean()
        is_claim = cleaned_data.get('is_claim')
        email = cleaned_data.get('email')
        contact_reason = cleaned_data.get('contact_reason')

        if is_claim and not email:
            raise ValidationError('クレームの場合はメールアドレスを入力してください。')

        if is_claim and not contact_reason == '2':
            raise ValidationError('クレームの場合は「感想」を選択してください。')

        return cleaned_data


class FileForm(forms.Form):
    """ いちばん最後のフィールドは、 HiddenInput にしています """
    file = FileField(label='ファイル', help_text='ファイルを選択してください。')
    name = CharField(label='お名前', max_length=10, help_text='10文字以内で入力してください。')
    email = EmailField(label='メールアドレス', help_text='必須です', )
    reason = CharField(label='投稿した理由', help_text='理由を入力してください。')
    hidden = DateTimeField(label='隠しフィールド', widget=HiddenInput, required=False, initial=timezone.now())
