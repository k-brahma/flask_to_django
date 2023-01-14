from django.http import HttpResponse
from django.views.generic import View, TemplateView


class SampleClass31(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h1>SampleClass21に呼ばれました！</h1>')


func_31 = SampleClass31.as_view()


class SampleClass32(TemplateView):
    template_name = "sample_without_context.html"


func_32 = SampleClass32.as_view()


class SampleClass33(TemplateView):
    template_name = "sample_with_context.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'メッセージです'
        return context


func_33 = SampleClass33.as_view()
