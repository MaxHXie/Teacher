import json

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from .forms import EssayForm
from .models import Essay

def index(request):
    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save()
            essay.characters = len(essay.essay_text)
            essay.price = calc_price(essay.characters)
            essay.save()
            return payment(request, essay)
    else:
        form = EssayForm()
    return render(request, 'english/index.html', {'form': form})

def payment(request, essay):
    return render(request, 'english/payment.html', {'essay': essay})

def payment_success_backend(request):
    body = json.loads(request.body)
    print("BODY", body)
    essay = get_object_or_404(Essay, pk=body['essay_id'])
    essay.paid = True
    essay.save()
    return JsonResponse('Payment completed!', safe=False)

def payment_result(request, essay_id):
    try:
        essay = Essay.objects.get(pk=essay_id)
    except Essay.DoesNotExist:
        essay = None
    if essay != None:
        return render(request, 'english/payment_success.html', {'essay': essay})
    else:
        return render(request, 'english/payment_fail.html')

def calc_price(characters):
    price = 1 + characters / 200
    return round(float(price), 1)
