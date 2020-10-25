import json, requests

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
            return submit(request, essay)
    else:
        form = EssayForm()
    return render(request, 'english/index.html', {'form': form})

def submit(request, essay):
    def grammarbot(essay_text):
        url = "https://grammarbot.p.rapidapi.com/check"
        payload = "language=en-US&text=" + essay_text
        headers = {
            'x-rapidapi-host': "grammarbot.p.rapidapi.com",
            'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
            'content-type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return response.text

    essay_text = essay.essay_text.replace(" ", "%20")
    response = grammarbot(essay_text)
    essay.essay_correction_string = response
    essay.save()

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
    price = 0.5 + characters / 400
    return round(float(price), 1)
