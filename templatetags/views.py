from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.shortcuts import render


# Create your views here.
class MarkdownPreview(View):
    template_name = "markdown_preview.html"

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {'body': request.POST['md'].strip()})


# Create your views here.
class MarkdownPreviewSafe(View):
    template_name = "markdown_preview_safe.html"

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {'body': request.POST['md'].strip()})
