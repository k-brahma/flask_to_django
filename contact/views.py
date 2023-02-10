import pathlib

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from contact.forms import ContactForm, FileForm


class ContactTopView(TemplateView):
    template_name = 'contact/contact_top.html'


class ContactFormAsParagraphView(TemplateView):
    template_name = 'contact/contact_form_as_paragraph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


class ContactFormAsDivView(TemplateView):
    template_name = 'contact/contact_form_as_div.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


class ContactFormAsTableView(TemplateView):
    template_name = 'contact/contact_form_as_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


class ContactFormAsUnorderedListView(TemplateView):
    template_name = 'contact/contact_form_as_unordered_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context


class ContactFormWithDataView(TemplateView):
    template_name = 'contact/contact_form_as_paragraph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = {'score': 50, 'name': 'John Doe', 'email': 'foo@bar.com', 'message': '良い本で感激しましたが、梱包が雑です。'}
        context['form'] = ContactForm(data=data)
        return context


class ContactFormWithPost(TemplateView):
    template_name = 'contact/contact_form_as_paragraph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ContactForm()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        print(data)

        return self.get(request, *args, **kwargs)


class ContactFormWithPostMethod(TemplateView):
    template_name = 'contact/contact_form_as_paragraph.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = ContactForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        data = request.POST

        form = ContactForm(data=data)
        if form.is_valid():
            email = form.cleaned_data['email']
            if email:
                send_mail(
                    'お問い合わせありがとうございます',
                    f'以下の問い合わせを受けつけました\n\n{form.cleaned_data["message"]}',
                    'info@flask.pc5bai.com',
                    [email, ],
                )
            messages.info(request, 'お問い合わせを受けつけました。')
            return redirect('main:index')
        else:
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)


class ContactFormView(FormView):
    template_name = 'contact/contact_form_as_paragraph.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:top')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if email:
            send_mail(
                'お問い合わせありがとうございます',
                f'以下の問い合わせを受けつけました\n\n{form.cleaned_data["message"]}',
                'info@flask.pc5bai.com',
                [email, ],
            )
        messages.info(self.request, 'お問い合わせを受けつけました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '入力内容にエラーがあります。')
        return super().form_invalid(form)


class FileFormView(FormView):
    """
    ファイルを受け取るViewでは、formでenctype="multipart/form-data"を指定する必要がある。
        multipart: 複数パートがある
        formdata : フォームデータ
        では、「複数のバート」とは？
            → request.POST, requst,FILES がある
    """

    template_name = 'contact/file_form.html'
    form_class = FileForm
    success_url = reverse_lazy('contact:top')

    def form_valid(self, form):
        """
        受信したファイルを、 /media/contact/ に保存する。
        """
        file = form.cleaned_data['file']
        file_name = file.name
        file_path = pathlib.Path(settings.MEDIA_ROOT) / 'contact' / file_name
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True)
        with open(file_path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)

        email = form.cleaned_data['email']
        send_mail(
            'お問い合わせありがとうございます',
            f'以下の問い合わせを受けつけました\n\n{form.cleaned_data["reason"]}',
            'info@pc5bai.com',
            [email, ],
        )
        messages.info(self.request, 'ファイルを受け取りました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '入力内容にエラーがあります。')
        return super().form_invalid(form)
