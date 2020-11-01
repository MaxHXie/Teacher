import json, requests, re

from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from .forms import EssayForm
from .models import Essay

def index(request):
    flags = {'en-US' : 'US', 'es' : 'ES', 'fr' : 'FR', 'de' : 'DE', 'it' : 'IT', 'pt' : 'PT', 'sv' : 'SE'}
    languages = {'en-US' : 'English', 'es' : 'Español', 'fr' : 'Français', 'de' : 'Deutsch', 'it' : 'Italiano', 'pt' : 'Português', 'sv' : 'svenska'}

    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    try:
        lang_id = request.GET['lang_id']
        selected_lang = {'flag' : flags[lang_id], 'lang' : languages[lang_id], 'lang_id' : lang_id}
    except:
        selected_lang = {'flag' : 'US', 'lang' : 'English(US)', 'lang_id': 'en-US'}

    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save()
            essay.essay_text = cleanhtml(essay.essay_text)
            essay.characters = len(essay.essay_text)
            lang_id = selected_lang['lang_id']
            essay.language = lang_id
            essay.save()
            return submit(request, essay, lang_id)

    else:
        form = EssayForm()
    return render(request, 'english/index.html', {'form': form, 'selected_lang': selected_lang})

def submit(request, essay, lang_id):

    # submit as many APIs as you want
    # format api responses to be in this format

    def azure_spellcheck(essay_text, lang_id):
        api_key = "48603fa402a041f9926e5962fbc3fd80"

        endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck"
        data = {'text': essay_text}
        params = {
            'mkt':lang_id,
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
                    "api" : "azure",
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

    def grammarbot(essay_text, lang_id):
        essay_text = essay_text.replace(" ", "%20")
        url = "https://grammarbot.p.rapidapi.com/check"
        payload = ("language=" + lang_id + "&text=" + essay_text).encode("utf-8")
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
                    "api" : "grammarbot",
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

    def language_tool(essay_text, lang_id):
        essay_text = essay_text.replace(" ", "%20")
        url = "https://api.languagetoolplus.com/v2/check"
        payload = ("text=" + essay_text + "&language=" + lang_id + "&username=maxhxie%40gmail.com&apiKey=7bb0788f2887ee3d&enabledOnly=false").encode("utf-8")
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'accept': "application/json"
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
                    "api" : "language_tool",
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

    all_errors = []
    for api in [language_tool]:
        all_errors = all_errors + api(essay.essay_text, lang_id)

    essay.errors = {"content": []}
    #make sure the same offset doesn't repeat

    # String adding function
    offsets = []
    for error in all_errors:
        if error['offset'] not in offsets:
            offsets.append(error['offset'])
            # To offer support for multiple correction suggestions we need to store them as a dictionary

            essay.errors["content"].append({
                "api" : error['api'],
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

    def config_errors(original, errors):
        parts = []
        start = 0

        errors = sorted(errors, key = lambda i: i['offset'])
        error_types = {'total' : 0, 'style' : 0, 'grammar' : 0, 'typographical' : 0, 'misspelling' : 0, 'formatting' : 0, 'duplication' : 0, 'whitespace': 0, 'register': 0, 'uncategorized': 0, 'non_conformance': 0}

        for error in errors:
            # count the number of errors
            error_types[error['type'].replace('-', '_')] += 1
            error_types['total'] += 1
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
            if error['message'] != '':
                popover_header = error['message']
            else:
                popover_header = error['type']
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
        return ''.join(parts), error_types

    if request.method == "GET":
        essay_id = request.GET.get('essay_id')
        try:
            essay = Essay.objects.get(pk=essay_id)
            essay_text = essay.essay_text
            essay_errors = json.loads(essay.errors)['content']
            essay_html, error_types = config_errors(essay_text, essay_errors)
            words = len(essay.essay_text.split())
            return render(request, 'english/correction.html', {'essay': essay, 'error_types': error_types, 'essay_html': essay_html, 'words': words})
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
