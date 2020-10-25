import json, requests, re

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .forms import EssayForm
from .models import Essay

def index(request):
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save()
            essay.essay_text = cleanhtml(essay.essay_text)
            essay.characters = len(essay.essay_text)
            essay.save()
            return submit(request, essay)
    else:
        form = EssayForm()
    return render(request, 'english/index.html', {'form': form})

def submit(request, essay):
    def grammarbot(essay_text):
        url = "https://grammarbot.p.rapidapi.com/check"
        payload = ("language=en-US&text=" + essay_text).encode("utf-8")
        headers = {
            'x-rapidapi-host': "grammarbot.p.rapidapi.com",
            'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
            'content-type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", url, data=payload, headers=headers)
        return response.text

    essay.essay_correction_json = grammarbot(essay.essay_text.replace(" ", "%20"))
    essay.errors = {"content": []}

    print(essay.essay_correction_json)

    # String adding function
    for error in json.loads(essay.essay_correction_json)['matches']:
        # To offer support for multiple correction suggestions we need to store them as a dictionary
        correction_dict = {"content": []}
        for correction in error['replacements']:
            correction_dict["content"].append(correction)
            print(correction)

        essay.errors["content"].append({
            "offset": error['offset'],
            "length": error['length'],
            "message": error['message'],
            "type": error['shortMessage'],
            "error": essay.essay_text[error['offset']:error['offset']+error['length']],
            "correction": json.dumps(correction_dict)
        })
    essay.errors = json.dumps(essay.errors)

    essay.save()

    return redirect('/correction?essay_id=' + str(essay.essay_id))

def correction(request):

    def add_strings(original, errors):
        parts = []
        start = 0
        for error in errors:
            corrections = json.loads(error['correction'])['content']
            correction_text = ""
            for i in range(len(corrections)):
                #If there is only 1 correction, surround it with quotation marks
                if len(corrections) == 1:
                    correction_text = corrections[i]['value']
                else:
                    #If there are several, separate them with commas, use the variable i to set a limit on how many corrections should  be displayed
                    if i == 0:
                        correction_text = "(" + corrections[i]['value'] + ", "
                    elif i != len(corrections) - 1 and i != 2:
                        correction_text = correction_text + corrections[i]['value'] + ', '
                    elif i == len(corrections) - 1 or i == 2:
                        correction_text = correction_text + corrections[i]['value'] + ")"
                        break
            if error['type'] != '':
                popover_header = error['type']
            else:
                popover_header = error['message']
            the_string = "<u><a href='#' data-toggle='popover' title='{}' data-placement='top'><mark class='error'>".format(popover_header)
            parts += original[start:error['offset']], the_string
            start = (error['offset'])
            if correction_text != "":
                correction_mark = "<mark class='correction'>{}</mark>".format(correction_text)
            else:
                correction_mark = ""
            parts += original[start:(error['offset']+error['length'])], "</mark></a></u>" + correction_mark
            start = (error['offset']+error['length'])
        parts += original[start:],
        return ''.join(parts)

    if request.method == "GET":
        essay_id = request.GET.get('essay_id')
        try:
            essay = Essay.objects.get(pk=essay_id)
            essay_text = essay.essay_text
            essay_errors = json.loads(essay.errors)['content']
            essay_html = add_strings(essay_text, essay_errors)
            words = len(essay.essay_text.split())
            return render(request, 'english/correction.html', {'essay': essay, 'essay_html': essay_html, 'words': words})
        except (ValidationError, Essay.DoesNotExist) as e:
            return redirect('/')
    else:
        return redirect('/')

def payment_success_backend(request):
    body = json.loads(request.body)
    print("BODY", body)
    essay = get_object_or_404(Essay, pk=body['essay_id'])
    essay.save()
    return JsonResponse('Payment completed!', safe=False)

def payment_result(request):
    if request.method == "GET":
        essay_id = request.GET.get('essay_id')
        try:
            essay = Essay.objects.get(pk=essay_id)
            return redirect('/correction?essay_id=' + str(essay.essay_id))
        except (ValidationError, Essay.DoesNotExist) as e:
            return redirect('/')

def terms_of_service(request):
    return render(request, 'english/terms_of_service.html')
