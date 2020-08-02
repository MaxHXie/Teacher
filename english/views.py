from django.views import generic
from django.shortcuts import render
from .forms import UploadFileForm

# Create your views here.
class IndexView(generic.edit.FormView):
    form_class = UploadFileForm
    template_name = 'english/index.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                print("received file")
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
