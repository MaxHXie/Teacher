import json, requests, re

from django.http import JsonResponse
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import truncatechars
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .forms import EssayForm, AnswerForm, CustomLoginForm
from .models import Essay, Answer, Profile, UserAction
from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from datetime import datetime

#notification system
from notifications.models import Notification

flags = {'math': 'MATH', 'no': 'Natural Science', 'so': 'Social Science', 'other': 'Other', 'en-US' : 'US', 'es' : 'ES', 'fr' : 'FR', 'de' : 'DE', 'it' : 'IT', 'pt' : 'PT', 'sv' : 'SE'}
subjects = {'math': 'Mathematics', 'no': 'Natural Science', 'so': 'Social Science', 'other': 'Other', 'en-US' : 'English', 'es' : 'Español', 'fr' : 'Français', 'de' : 'Deutsch', 'it' : 'Italiano', 'pt' : 'Português', 'sv' : 'Svenska'}

from allauth.account.signals import user_logged_in, user_logged_out, user_signed_up, password_changed, password_reset, email_confirmed, user_signed_up

@receiver(user_logged_in)
def user_logged_in(sender, request, user, **kwargs):
    user_action = UserAction.objects.create(user=user, action="user_logged_in")

@receiver(user_logged_out)
def user_logged_out(sender, request, user, **kwargs):
    user_action = UserAction.objects.create(user=user, action="user_logged_out")

@receiver(user_signed_up)
def user_signed_up(sender, request, user, **kwargs):
    user_action = UserAction.objects.create(user=user, action="user_signed_up")
    profile = Profile.objects.create(user=user)

@receiver(password_changed)
def password_changed(sender, request, user, **kwargs):
    user_action = UserAction.objects.create(user=user, action="password_changed")

@receiver(password_reset)
def password_reset(sender, request, user, **kwargs):
    user_action = UserAction.objects.create(user=user, action="password_reset")

@receiver(email_confirmed)
def email_confirmed(sender, request, user, **kwargs):
    user_action = UserAction.objects.create(user=user, action="email_confirmed")

def get_notifications(request):
    user = request.user
    if request.user.is_anonymous:
        return [], False
    else:
        notifications = Notification.objects.filter(recipient=user).order_by('-timestamp')
        has_unread_notifications = False
        #remove items where the actor = recipient
        notifications = [n for n in notifications if not n.actor == request.user]
        for notification in notifications:
            notification.time_ago = get_date(notification.timestamp)
            if notification.unread == True:
                has_unread_notifications = True

        return notifications, has_unread_notifications

def get_date(timestamp):
    time = datetime.now()
    if timestamp.day == time.day:
        if timestamp.hour == time.hour or abs(timestamp.hour - time.hour) == 1:
            time_ago = time.minute - timestamp.minute
            if time_ago == 1:
                return str(time_ago) + " minute ago"
            else:
                return str(time_ago) + " minutes ago"
        else:
            time_ago = time.hour - timestamp.hour
            if time_ago == 1:
                return str(time_ago) + " hour ago"
            else:
                return str(time_ago) + " hours ago"

    else:
        if timestamp.month == time.month:
            time_ago = time.day - timestamp.day
            if time_ago == 1:
                return str(time_ago) + " day ago"
            else:
                return str(time_ago) + " days ago"
        else:
            if timestamp.year == time.year:
                time_ago = time.month - timestamp.month
                if time_ago == 1:
                    return str(time_ago) + " month ago"
                else:
                    return str(time_ago) + " months ago"
    return timestamp

def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

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


def read_notifications(request):
    #Update all notifications of user to unread=False, this happens when the user reads their notifications
    data = {'user': request.user}
    if request.method == "GET":
        username = request.GET.get('username')
        if username == request.user.username:
            notifications = Notification.objects.filter(recipient=request.user, unread=True).update(unread=False)
    return JsonResponse(data)

def index(request):
    #notification system

    notifications, has_unread_notifications = get_notifications(request)

    try:
        lang_id = request.GET['lang_id']
        selected_lang = {'flag' : flags[lang_id], 'lang' : subjects[lang_id], 'lang_id' : lang_id}
    except:
        selected_lang = {'flag' : 'none', 'lang' : 'none', 'lang_id': 'none'}

    if request.method == 'POST':
        if request.user.is_anonymous is True:
            return(redirect('/accounts/signup'))
        bounty = request.POST.get('bounty')
        lang_id = selected_lang['lang_id']
        form = EssayForm(request.POST)
        if lang_id == "none":
            return render(request, 'english/index.html', {'form': form, 'selected_lang': selected_lang, 'page_error': 'select_subject', 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})
        elif bounty.isnumeric() is False:
            return render(request, 'english/index.html', {'form': form, 'selected_lang': selected_lang, 'page_error': 'enter_bounty', 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})
        elif int(bounty) < 1:
            return render(request, 'english/index.html', {'form': form, 'selected_lang': selected_lang, 'page_error': 'bounty_too_small', 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})
        else:
            if form.is_valid():
                essay = form.save()
                essay.is_valid = False
                essay.author = request.user
                essay.essay_text = cleanhtml(essay.essay_text)
                essay.characters = len(essay.essay_text)
                essay.language = lang_id
                essay.subject = subjects[lang_id]
                essay.bounty = bounty
                if essay.title == "":
                    essay.title = truncatechars(essay.essay_text, 32)
                else:
                    essay.title = cleanhtml(essay.title)

                author_coins = essay.author.profile.coins
                if int(bounty) > author_coins:
                    return render(request, 'english/index.html', {'form': form, 'selected_lang': selected_lang, 'page_error': 'insufficient_coins', 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})
                else:
                    essay.author.profile.coins -= int(bounty)

                essay.author.profile.save()
                essay.is_valid = True
                essay.save()
                if lang_id != "math" and lang_id != "no" and lang_id != "so" and lang_id != "other":
                    return submit(request, essay, lang_id)
                else:
                    if len(Essay.objects.filter(author=request.user)) == 1:
                        return redirect('/correction?essay_id=' + str(essay.essay_id) + '&first_question=true')
                    else:
                        return redirect('/correction?essay_id=' + str(essay.essay_id))

    else:
        form = EssayForm()
    return render(request, 'english/index.html', {'form': form, 'selected_lang': selected_lang, 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})

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

    if len(Essay.objects.filter(author=request.user)) == 1:
        return redirect('/correction?essay_id=' + str(essay.essay_id) + '&first_question=true')
    else:
        return redirect('/correction?essay_id=' + str(essay.essay_id))

def correction(request):

    notifications, has_unread_notifications = get_notifications(request)

    if request.method == "GET":
        essay_id = request.GET.get('essay_id')
        scroll_section_id = request.GET.get('scroll')
        try:
            essay = Essay.objects.get(pk=essay_id)
            essay_text = essay.essay_text
            try:
                essay_errors = json.loads(essay.errors)['content']
                essay_html, error_types = config_errors(essay_text, essay_errors)
            except:
                essay_errors = ""
                essay_html = essay_text
                error_types = ""
            answer_list = Answer.objects.all().filter(essay=essay).order_by('-upload_datetime')
            has_ended = essay.has_ended
            answer_form = AnswerForm()
            essay.views += 1
            essay.save()
            return render(request, 'english/correction.html', {'essay': essay, 'answer_list': answer_list, 'has_ended': has_ended, 'scroll_section_id': scroll_section_id, 'answer_form': answer_form, 'error_types': error_types, 'essay_html': essay_html, 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})
        except (ValidationError, Essay.DoesNotExist) as e:
            return redirect('/')
    else:
        return redirect('/')

def market(request):

    notifications, has_unread_notifications = get_notifications(request)

    essay_list = Essay.objects.all().order_by('-upload_datetime')
    return render(request, 'english/market.html', {'essay_list': essay_list, 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})


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

def profile(request):

    notifications, has_unread_notifications = get_notifications(request)

    if request.method == "GET":
        username = request.GET.get('username')
        try:
            this_user = User.objects.get(username=username)
            essay_list = Essay.objects.filter(author=this_user).order_by('-upload_datetime')
            answer_list = Answer.objects.filter(author=this_user).order_by('-upload_datetime')
            return render(request, 'english/profile.html', {'essay_list': essay_list, 'answer_list': answer_list, 'this_user': this_user, 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})
        except (ValidationError, User.DoesNotExist) as e:
            pass

    if request.user.is_anonymous:
        return index(request)
    else:
        try:
            essay_list = Essay.objects.filter(author=request.user).order_by('-upload_datetime')
            answer_list = Answer.objects.filter(author=request.user).order_by('-upload_datetime')
            return render(request, 'english/profile.html', {'essay_list': essay_list, 'answer_list': answer_list, 'this_user': request.user, 'notifications': notifications, 'has_unread_notifications': has_unread_notifications})
        except (ValidationError, Essay.DoesNotExist) as e:
            return redirect('/')

def post_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            if request.user.is_anonymous is True:
                return index(request)
            else:
                #Make sure that the essay the answer is referring to exists
                try:
                    essay_id = request.POST.get('essay_id')
                    essay = Essay.objects.get(essay_id=essay_id)
                except:
                    return index(request)

                answer = form.save(commit=False)
                answer.author = request.user
                answer.answer_text = cleanhtml(answer.answer_text)
                answer.essay = essay
                answer.save()
                return redirect('/correction?essay_id=' + str(essay_id) + '&scroll=section-answers')

    return redirect('/correction?essay_id=' + str(essay_id) + '&scroll=section-answers')

def winner(request):
    if request.user.is_anonymous:
        return index(request)
    elif request.method == "GET":
        essay_id = request.GET.get('essay_id')
        answer_id = request.GET.get('answer_id')

        #Check that both the essay and question exist
        try:
            essay = Essay.objects.get(essay_id=essay_id)
        except Answer.DoesNotExist:
            return index(request)

        #When we know that the essay exists, we can load some variables
        answer_list = Answer.objects.all().filter(essay=essay).order_by('-upload_datetime')
        essay_text = essay.essay_text
        try:
            essay_errors = json.loads(essay.errors)['content']
            essay_html, error_types = config_errors(essay_text, essay_errors)
        except:
            essay_errors = ""
            essay_html = essay_text
            error_types = ""

        try:
            answer = Answer.objects.get(answer_id=answer_id)
        except Answer.DoesNotExist:
            return redirect('/correction?essay_id=' + str(essay_id) + '&scroll=section-answers')

        #Check that the current user is the author of the question
        if request.user != essay.author:
            return redirect('/correction?essay_id=' + str(essay_id) + '&scroll=section-answers')

        #Check that the answerer and questionmaker is not the same user
        if request.user == answer.author:
            return redirect('/correction?essay_id=' + str(essay_id) + '&scroll=section-answers')

        #Check if this question already has a winner
        else:
            for answer2 in Answer.objects.all().filter(essay=essay):
                if answer2.winner == True:
                    return redirect('/correction?essay_id=' + str(essay_id) + '&scroll=section-answers')

            answer.winner = True
            answer.save(update_fields=['winner'])

            essay.has_ended = True
            essay.save(update_fields=['has_ended'])

            answer.author.profile.coins += essay.bounty
            answer.author.profile.save()

            #Load original variables here
            return redirect('/correction?essay_id=' + str(essay_id) + '&scroll=section-answers')

    else:
        return index(request)

def get_coins(request):
    notifications, has_unread_notifications = get_notifications(request)

    return HttpResponse('Coming soon!')

def terms_of_service(request):
    return render(request, 'english/terms_of_service.html')
