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

    # submit as many APIs as you want
    # format api responses to be in this format
    """
    {
        "errors" :
        [
            {
                "offset": 353,
                "length": 12,
                "message": "This word is a possibel misspelling",
                "type": "Misspelling"
                "error": "flexibly",
                "correction": [
                    "flexible",
                    "flexibility",
                    "flexibale"
                ]
            }
        ],
        [
            {
                "offset": 353,
                "length": 12,
                "message": "This word is a possibel misspelling",
                "type": "Misspelling"
                "error": "flexibly",
                "correction": [
                    "flexible",
                    "flexibility",
                    "flexibale"
                ]
            }
        ]
    }
    """
    def azure_spellcheck(essay_text):
        api_key = "48603fa402a041f9926e5962fbc3fd80"

        endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck"
        data = {'text': essay_text}
        params = {
            'mkt':'en-us',
            'mode':'proof'
            }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Ocp-Apim-Subscription-Key': api_key,
        }

        response = requests.post(endpoint, headers=headers, params=params, data=data).json()

        #Make sure all errors from all APIs get the same format

        response_formatted = []
        try:
            for error in response['flaggedTokens']:
                if error["type"] == "UnknownToken":
                    error_type = "Mispelled word"
                else:
                    error_type = "Unknown error type"

                corrections = []
                for i in error["suggestions"]:
                    corrections.append(i["suggestion"])

                error_dict = {
                    "offset" : error["offset"],
                    "length" : len(error["token"]),
                    "message" : error_type,
                    "type" : error_type,
                    "error" : error["token"],
                    "corrections" : corrections
                }

                response_formatted.append(error_dict)

        except KeyError:
            print('[ERROR] Azure Spellcheck API call')
            print(json.dumps(response, indent=4))

        return response_formatted

    def grammarbot(essay_text):
        essay_text = essay_text.replace(" ", "%20")
        url = "https://grammarbot.p.rapidapi.com/check"
        payload = ("language=en-US&text=" + essay_text).encode("utf-8")
        headers = {
            'x-rapidapi-host': "grammarbot.p.rapidapi.com",
            'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
            'content-type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", url, data=payload, headers=headers).json()

        #Make sure all errors from all APIs get the same format

        response_formatted = []
        try:
            for error in response['matches']:
                corrections = []
                for i in error["replacements"]:
                    corrections.append(i["value"])

                error_dict = {
                    "offset" : error["offset"],
                    "length" : error["length"],
                    "message" : error["shortMessage"],
                    "type" : error["rule"]["issueType"],
                    "error" : essay_text[error["offset"]:error["offset"]+error["length"]],
                    "corrections" : corrections
                }

                response_formatted.append(error_dict)

        except KeyError:
            print('[ERROR] Grammarbot API call')
            print(json.dumps(response, indent=4))

        return response_formatted

    def language_tool(essay_text):
        essay_text = essay_text.replace(" ", "%20")
        url = "https://dnaber-languagetool.p.rapidapi.com/v2/check"
        payload = ("text=" + essay_text + "&language=en-US").encode("utf-8")
        headers = {
            'x-rapidapi-host': "dnaber-languagetool.p.rapidapi.com",
            'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
            'content-type': "application/x-www-form-urlencoded"
            }
        response = requests.request("POST", url, data=payload, headers=headers).json()

        #Make sure all errors from all APIs get the same format

        response_formatted = []
        try:
            for error in response['matches']:
                corrections = []
                for i in error["replacements"]:
                    corrections.append(i["value"])

                error_dict = {
                    "offset" : error["offset"],
                    "length" : error["length"],
                    "message" : error["shortMessage"],
                    "type" : error["rule"]["issueType"],
                    "error" : essay_text[error["offset"]:error["offset"]+error["length"]],
                    "corrections" : corrections
                }

                response_formatted.append(error_dict)

        except KeyError:
            print('[ERROR] Language Tool API call')
            print(json.dumps(response, indent=4))

        return response_formatted

    def web_spell_checker(essay_text):
        url = "https://webspellchecker-webspellcheckernet.p.rapidapi.com/ssrv.cgi"
        querystring = {"format":"json","cmd":"grammar_check","text":essay_text.encode('utf-8'),"slang":"en_US"}
        headers = {
            'x-rapidapi-host': "webspellchecker-webspellcheckernet.p.rapidapi.com",
            'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870"
        }

        response = json.loads(requests.request("GET", url, headers=headers, params=querystring).text)[0]

        #Make sure all errors from all APIs get the same format

        response_formatted = []
        try:
            for error in response['matches']:
                corrections = []
                for correction in error["suggestions"]:
                    corrections.append(correction)

                error_dict = {
                    "offset" : error["offset"],
                    "length" : error["length"],
                    "message" : error["message"],
                    "type" : error["rule"]["category"],
                    "error" : essay_text[error["offset"]:error["offset"]+error["length"]],
                    "corrections" : corrections
                }

            response_formatted.append(error_dict)

        except KeyError:
            print('[ERROR] Web Spell Checker API call')
            print(json.dumps(response, indent=4))

        return response_formatted

    all_errors = []
    for api in [azure_spellcheck, grammarbot, language_tool, web_spell_checker]:
        all_errors = all_errors + api(essay.essay_text)

    essay.errors = {"content": []}
    #make sure the same offset doesn't repeat

    # String adding function
    offsets = []
    for error in all_errors:
        if error['offset'] not in offsets:
            offsets.append(error['offset'])
            # To offer support for multiple correction suggestions we need to store them as a dictionary

            essay.errors["content"].append({
                "offset": error['offset'],
                "length": error['length'],
                "message": error['message'],
                "type": error['type'],
                "error": error['error'],
                "corrections": error['corrections']
            })
        else:
            pass

    essay.errors = json.dumps(essay.errors)

    essay.save()

    return redirect('/correction?essay_id=' + str(essay.essay_id))

def correction(request):

    def add_strings(original, errors):
        parts = []
        start = 0

        errors = sorted(errors, key = lambda i: i['offset'])

        for error in errors:
            print(error['offset'])
            corrections = error['corrections']
            correction_text = ""
            for i in range(len(corrections)):
                #If there is only 1 correction, don't surround it with parenthesis
                placeholder = corrections[i]
                if len(corrections) == 1:
                    correction_text = placeholder
                else:
                    #If there are several, separate them with commas, use the variable i to set a limit on how many corrections should  be displayed
                    if i == 0:
                        correction_text = "(" + placeholder + ", "
                    elif i != len(corrections) - 1 and i != 2:
                        correction_text = correction_text + placeholder + ', '
                    elif i == len(corrections) - 1 or i == 2:
                        correction_text = correction_text + placeholder + ")"
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
