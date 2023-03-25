"""
save_m2m メソッドについては、以下のドキュメントを参照。
https://docs.djangoproject.com/en/4.1/topics/forms/modelforms/#the-save-method
"""
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import resolve_url, redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView

from note.forms import EntryForm, CommentForm
from note.models import Entry, Tag, Comment

User = get_user_model()


class CommentListView(ListView):
    """
    Comment の一覧表示

    comment.entry.user は親の親だということに留意
    """
    model = Comment
    template_name = 'note/comment_list.html'

    def get_queryset(self):
        return Comment.objects.all().select_related('user', 'entry', 'entry__user', )


class UserEntryListView(ListView):
    """
    ユーザーが投稿した Entry の一覧表示
    """
    model = Entry
    template_name = 'note/user_entry_list.html'

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        qs = Entry.objects.filter(user=user)
        return qs.select_related('user', ).prefetch_related('tags', 'comment_set', 'comment_set__user', )


class EntryListPaginationView(ListView):
    """
    Entry の一覧表示。ページング機能つき。

    GETのパラメータとして、以下の2つを受けつける。
        tag: タグのスラッグ。指定されたタグがついた Entry のみを表示する。
        page: 表示するページ番号。指定されない場合は、1ページ目を表示する。
    """

    model = Entry
    paginate_by = 10
    template_name = 'note/entry_list_pagination.html'

    def get_queryset(self):
        qs = Entry.objects.all().select_related('user', ).prefetch_related('tags', 'comment_set', )

        # 初期値を '' にしておかないと、 /note/elided/ へのアクセスで form に None が入ってしまう。
        self.tag = self.request.GET.get('tag', '')
        if self.tag:
            qs = qs.filter(tags__slug=self.tag)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class EntryListViewPaginationElidedView(EntryListPaginationView):
    paginate_by = 5
    template_name = 'note/entry_list_pagination_elided.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']
        context['paginator_range_header'] = page_obj.paginator.get_elided_page_range(page_obj.number)
        context['paginator_range_footer'] = page_obj.paginator.get_elided_page_range(page_obj.number)
        return context


class EntryListView(ListView):
    model = Entry

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(resolve_url('account_login') + '?next=' + request.path)
        return super().dispatch(request, *args, **kwargs)

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
        form = CommentForm(request.POST)
        if form.is_valid():
            self.object = self.get_object()
            comment = form.save(commit=False)
            comment.entry = self.object
            comment.user = self.request.user  # 要ログイン。ログインユーザ以外によるコメントはここで 500 エラーになる
            comment.save()
            messages.info(self.request, 'コメントしました')
            return redirect(self.request.path)
        else:
            messages.info(self.request, 'コメント投稿に失敗しました')
            return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


# 様々な View での instance の生成
class CreateNormalView(LoginRequiredMixin, View):
    """
    通常の View での instance の生成/更新
    """

    def get(self, request, *args, **kwargs):
        form = EntryForm()
        return render(request, 'note/entry_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = self.request.user
            entry.save()
            form.save_m2m()  # form.save(commit=False) のあとは、これが必要
            messages.info(self.request, '投稿しました')
            return redirect('note:index')
        else:
            messages.info(self.request, '投稿に失敗しました')
            return render(request, 'note/entry_form.html', {'form': form})


class CreateFormView(LoginRequiredMixin, FormView):
    """
    FormView での instance の生成/更新

    BaseFormView -> ProcessFormView で、
    get, post での基本的な処理は記述済み。
    なので、 form.is_valid() の結果次第で呼び出される
    form_valid, form_invalid だけ書けばよい。
    """

    form_class = EntryForm
    template_name = 'note/entry_form.html'
    success_url = reverse_lazy('note:index')

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.user = self.request.user
        entry.save()
        form.save_m2m()  # form.save(commit=False) のあとは、これが必要
        messages.info(self.request, '投稿しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, '投稿に失敗しました')
        return super().form_invalid(form)


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
    #     form.save_m2m() # form.save(commit=False) のあとは、これが必要
    #     messages.info(self.request, '投稿しました')
    #     return super().form_valid(form)
    def form_invalid(self, form):
        messages.info(self.request, '投稿に失敗しました')
        return super().form_invalid(form)


# 様々な View での instance の更新
class UpdateNormalView(LoginRequiredMixin, View):
    """
    通常の View での instance の更新
    url から pk を取得して、更新すべき instance を見つけるための情報とする

    モデルの生成と異なり、更新時には、 form の生成時に instance を渡す。
    (違いはそのくらい)
    """

    def get(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=kwargs['pk'])
        form = EntryForm(instance=entry)
        return render(request, 'note/entry_form.html', {'form': form})

    def post(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry, pk=kwargs['pk'])
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = self.request.user
            entry.updated_at = timezone.now()
            entry.save()
            form.save_m2m()  # form.save(commit=False) のあとは、これが必要
            messages.info(self.request, '投稿を更新しました')
            return redirect('note:index')
        else:
            messages.info(self.request, '投稿更新に失敗しました')
            return render(request, 'note/entry_form.html', {'form': form})


class UpdateFormView(LoginRequiredMixin, FormView):
    """
    FormView での instance の更新

    BaseFormView -> ProcessFormView で、
    get, post での基本的な処理は記述済み。
    なので、 form.is_valid() の結果次第で呼び出される
    form_valid, form_invalid だけ書けばよい。
    """

    form_class = EntryForm
    template_name = 'note/entry_form.html'
    success_url = reverse_lazy('note:index')

    def get_initial(self):
        """
        初期値を設定する

        このメソッドは、 get で呼び出されたときに、
        form の初期値として使われる。
        """
        entry = get_object_or_404(Entry, pk=self.kwargs['pk'])
        return {
            'title': entry.title,
            'body': entry.body,
            'tags': entry.tags.all(),
        }

    def form_valid(self, form):
        entry = form.save(commit=False)
        entry.user = self.request.user
        entry.updated_at = timezone.now()
        entry.save()
        form.save_m2m()  # form.save(commit=False) のあとは、これが必要
        messages.info(self.request, '投稿を更新しました')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.info(self.request, '投稿更新に失敗しました')
        return super().form_invalid(form)


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
    #     form.save_m2m() # form.save(commit=False) のあとは、これが必要
    #     messages.info(self.request, '投稿を更新しました')
    #     return super().form_valid(form)


class DeleteNormalView(LoginRequiredMixin, View):
    """
    通常の View での instance の削除
    url から pk を取得して、削除すべき instance を見つけるための情報とする
    """

    def get(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry.objects.filter(user=self.request.user), pk=kwargs['pk'])
        return render(request, 'note/entry_confirm_delete.html', context={'object': entry})

    def post(self, request, *args, **kwargs):
        entry = get_object_or_404(Entry.objects.filter(user=self.request.user), pk=kwargs['pk'])
        entry.delete()
        messages.warning(self.request, '投稿を削除しました')
        return redirect('note:index')


# FormView を使ったサンプルはない(request body が空の POST 投稿をするので、 Form は必要ないから)

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry

    def get_queryset(self):
        """ 投稿者本人以外は削除できないようにする """
        return Entry.objects.filter(user=self.request.user)

    def get_success_url(self):
        messages.warning(self.request, '投稿を削除しました')
        return resolve_url('note:index')
