from pprint import pprint

from contact.forms import ContactForm


def my_form_tester_valid():
    """
    受け取ったすべての値に問題がない場合
    """
    data = {
        'score': '50',
        'name': 'test',
        'email': 'foo@bar.com',
        'message': '良い本で感激しましたが、梱包が雑です。',
        'dt': '2023-02-10 22:02',
    }

    form = ContactForm(data=data)

    result = form.is_valid()
    print(result)
    print(form.errors)
    print(form.cleaned_data)
    pprint(form.cleaned_data)  # 数値や日付は適切な型に変換されていることに注意！


def my_form_tester_invalid():
    """
    scoreが100を超えている
    emailが不正
    日付を受け取っていない
    """
    data = {
        'score': '123',
        'name': 'test',
        'email': 'foo_bar_com',
        'message': '良い本で感激しましたが、梱包が雑です。',
    }

    form = ContactForm(data=data)

    result = form.is_valid()
    print(result)
    print(form.errors)
    print(form.cleaned_data)
