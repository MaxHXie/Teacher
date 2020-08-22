import json

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
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
    essay_limit = 10
    incomplete_essay_list = Essay.objects.filter(paid=True, completed=False)
    if len(incomplete_essay_list) >= essay_limit:
        form = EssayForm(request.POST)
        essay.were_limited = True
        essay.save()
        return render(request, 'english/index.html', {'essay_limit': essay_limit, 'form': form})
    else:
        return redirect('/checkout?essay_id=' + str(essay.essay_id))

def checkout(request):
    if request.method == "GET":
        essay_id = request.GET.get('essay_id')
        try:
            essay = Essay.objects.get(pk=essay_id)
            if essay.paid == True:
                form = EssayForm()
                return render(request, 'english/index.html', {'already_paid': True, 'form': form})
            else:
                words = len(essay.essay_text.split())
                return render(request, 'english/checkout.html', {'essay': essay, 'words': words})
        except (ValidationError, Essay.DoesNotExist) as e:
            return redirect('/')
    else:
        return redirect('/')

def payment_success_backend(request):
    body = json.loads(request.body)
    print("BODY", body)
    essay = get_object_or_404(Essay, pk=body['essay_id'])
    essay.paid = True
    essay.save()
    return JsonResponse('Payment completed!', safe=False)

def payment_result(request):
    if request.method == "GET":
        essay_id = request.GET.get('essay_id')
        try:
            essay = Essay.objects.get(pk=essay_id)
            if essay.paid == True:
                return render(request, 'english/payment_success.html', {'essay': essay})
            else:
                return redirect('/checkout?essay_id=' + str(essay.essay_id))
        except (ValidationError, Essay.DoesNotExist) as e:
            return redirect('/')

def terms_of_service(request):
    return render(request, 'english/terms_of_service.html')

def calc_price(characters):
    price = 1 + characters / 250
    return round(float(price), 1)
