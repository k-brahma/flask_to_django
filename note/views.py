from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import resolve_url
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from note.forms import EntryForm, CommentForm
from note.models import Entry, Tag


class EntryListView(ListView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.all().select_related('user', ).prefetch_related('tags', 'comment_set', )


class EntryTagListView(EntryListView):
    model = Entry

    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs['tag'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = Tag.objects.get(slug=self.kwargs['tag'])
        return context


class EntryDetailView(DetailView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.all().select_related('user', ).prefetch_related('tags', 'comment_set', )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.entry = self.object
            comment.user = self.request.user
            comment.save()
            messages.info(self.request, 'コメントしました')
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class EntryCreateView(LoginRequiredMixin, CreateView):
    """
    EntryForm の新規追加

    EntryForm は、 user 情報を持たない。
    なので、更新時に user 情報を追加する必要がある。
    以下では、その方法を2つ示す。
    """
    model = Entry
    form_class = EntryForm

    def form_valid(self, form):
        """
        方法1:

        form.instance は、新規登録されるモデルオブジェクト
        これの属性を編集してから save する
        """
        form.instance.user = self.request.user
        messages.info(self.request, '投稿しました')
        return super().form_valid(form)

    # def form_valid(self, form):
    #     """
    #     方法2:
    #
    #     form.save(commit=False) で、新規登録されるモデルオブジェクトを取得
    #     この場合は、many-to-many のデータは、別途保存し直す必要がある。
    #     """
    #     instance = form.save(commit=False)
    #     instance.user = self.request.user
    #     instance.save()
    #     form.save_m2m()
    #     messages.info(self.request, '投稿しました')
    #     return super().form_valid(form)


class EntryUpdateView(LoginRequiredMixin, UpdateView):
    """
    EntryForm の更新

    EntryForm は、 user 情報を持たない。
    なので、更新時に user 情報を追加する必要がある。
    以下では、その方法を2つ示す。
    """
    model = Entry
    form_class = EntryForm

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        方法1:

        form.instance は、更新対象のモデルオブジェクト
        これの属性を編集してから save する
        """
        form.instance.user = self.request.user
        form.instance.updated_at = timezone.now()
        messages.info(self.request, '投稿を更新しました')
        return super().form_valid(form)

    # def form_valid(self, form):
    #     """
    #     方法2:
    #
    #     form.save(commit=False) で、更新対象のモデルオブジェクトを取得
    #     この場合は、many-to-many のデータは、別途保存し直す必要がある。
    #     """
    #     instance = form.save(commit=False)
    #
    #     instance.user = self.request.user
    #     instance.updated_at = timezone.now()
    #     instance.save()
    #     form.save_m2m()
    #     messages.info(self.request, '投稿を更新しました')
    #     return super().form_valid(form)


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)

    def get_success_url(self):
        messages.warning(self.request, '投稿を削除しました')
        return resolve_url('note:index')
