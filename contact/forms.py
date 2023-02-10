from django.forms import forms, IntegerField, EmailField, Textarea, CharField, DateTimeField, BooleanField
from django.utils import timezone


class ContactForm(forms.Form):
    score = IntegerField(label='スコア', min_value=0, max_value=100, help_text='0点から100点のどこですか。')
    name = CharField(label='お名前', max_length=10, help_text='10文字以内で入力してください。')
    email = EmailField(label='メールアドレス', help_text='必須ではありません', required=False)
    message = CharField(label='メッセージ', widget=Textarea, help_text='言いたいことを思う存分書いてください。')
    dt = DateTimeField(label='日時', help_text='日時を入力してください。', initial='2023-02-12 09:15:12')
    is_claim = BooleanField(label='クレーム', required=False, help_text='クレームですか？')

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == 'info@pc5bai.com':
            raise forms.ValidationError('このメールアドレスは使用できません。')
        return email

    def clean_dt(self):
        dt = self.cleaned_data['dt']
        if dt > timezone.now():
            raise forms.ValidationError('未来の日付は入力できません。')
        return dt

    def clean(self):
        cleaned_data = super().clean()
        is_claim = cleaned_data.get('is_claim')
        email = cleaned_data.get('email')
        if is_claim and not email:
            raise forms.ValidationError('クレームの場合はメールアドレスを入力してください。')
        return cleaned_data
