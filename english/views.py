from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import EssayForm

def index(request):
    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            words = form.cleaned_data['words']
            price = words / 10
            form.save()
            return payment(request, price)
        else:
            print(form.errors)
    else:
        form = EssayForm()
    return render(request, 'english/index.html', {'form': form})

def payment(request, price):
    return render(request, 'english/payment.html')
