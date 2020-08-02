from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

def index(request):
    if request.method == 'POST':
        print("POST")
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("YAS")
            # file is saved
            form.save()
            return HttpResponseRedirect(reverse('english:index'))
    else:
        form = UploadFileForm()
    return render(request, 'english/index.html', {'form': form})
