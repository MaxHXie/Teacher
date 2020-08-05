from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import EssayForm
from .models import Essay

def index(request):
    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save()
            essay.price = calc_price(essay.words)
            essay.save()
            return payment(request, essay)
    else:
        form = EssayForm()
    return render(request, 'english/index.html', {'form': form})

def payment(request, essay):
    return payment_success(request, essay)
    #return render(request, 'english/payment.html', {'essay': essay})

def payment_success(request, essay):
    return render(request, 'english/payment_success.html')

def payment_fail(request):
    pass

def calc_price(words):
    price = words / 10
    return float(price)
