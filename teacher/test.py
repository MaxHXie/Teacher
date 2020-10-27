"""
import requests
import json

api_key = "48603fa402a041f9926e5962fbc3fd80"
example_text = "My name is liyan and im a 15 year old feamle and I live in Swedan, but I was born in Somalia. I escaped from somalia becous it was to dangerous, was just a little girl around two years old I think. I came to swedan with a plan. When we landed we met my cusin. They were already here. We waited until we got premission to live here, we got it a week after we came, and now I lived here since then. The first thing you need to know about me is that im muslim girl. I carry a hijab on me evreytime im outside and I'm not forced to it´s my choice, but some people around the world don´t get it. I have a big family we`re 9 people 7 kids, im the middel one I have 3 biger and 3 younger siblings. The house I live in is not that big but big enough to live in, I share room with two of my siblings one is younger and the other one is older, we always argument about who´s gonna clean and making the bed every singel morning. To have a big family is sometimes great, to talk to someone or hang out and other things but the bad to have a bige family is that you never get anything for yourself, sometimes they just take my things without my permission and it´s annoying, I have to clean after my younger siblings all the time. When my relatives come without to telling us" # the text to be spell-checked
endpoint = "https://api.cognitive.microsoft.com/bing/v7.0/SpellCheck"

data = {'text': example_text}

params = {
    'mkt':'en-us',
    'mode':'proof'
    }

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Ocp-Apim-Subscription-Key': api_key,
}

response = requests.post(endpoint, headers=headers, params=params, data=data)

json_response = response.json()
print(json.dumps(json_response, indent=4))



import requests

url = "https://dnaber-languagetool.p.rapidapi.com/v2/check"

payload = "text=This%20is%20a%20error.&language=en-US"
headers = {
    'x-rapidapi-host': "dnaber-languagetool.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)


import requests

url = "https://webspellchecker-webspellcheckernet.p.rapidapi.com/ssrv.cgi"

querystring = {"format":"xml","cmd":"grammar_check","text":"These are an examples of a sentences with two misspelled words and gramar problems. Just type text with mispelling to see how it works.","slang":"en_US"}

headers = {
    'x-rapidapi-host': "webspellchecker-webspellcheckernet.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

import requests, xmltodict

import requests

url = "https://webspellchecker-webspellcheckernet.p.rapidapi.com/ssrv.cgi"
querystring = {"format":"json","cmd":"grammar_check","text":"These are an examples of a sentences with two misspelled words and gramar problems. Just type text with mispelling to see how it works.","slang":"en_US"}

headers = {
    'x-rapidapi-host': "webspellchecker-webspellcheckernet.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)


import requests

url = "https://grammarbot.p.rapidapi.com/check"
payload = ("language=en-US&text=My name is liyan and im a 15 year old feamle and I live in Swedan, but I was born in Somalia. I escaped from somalia becous it was to dangerous, was just a little girl around two years old I think. I came to swedan with a plan. When we landed we met my cusin. They were already here. We waited until we got premission to live here, we got it a week after we came, and now I lived here since then. The first thing you need to know about me is that im muslim girl. I carry a hijab on me evreytime im outside and I'm not forced to it´s my choice, but some people around the world don´t get it. I have a big family we`re 9 people 7 kids, im the middel one I have 3 biger and 3 younger siblings. The house I live in is not that big but big enough to live in, I share room with two of my siblings one is younger and the other one is older, we always argument about who´s gonna clean and making the bed every singel morning. To have a big family is sometimes great, to talk to someone or hang out and other things but the bad to have a bige family is that you never get anything for yourself, sometimes they just take my things without my permission and it´s annoying, I have to clean after my younger siblings all the time. When my relatives come without to telling us").encode("utf-8")
headers = {
    'x-rapidapi-host': "grammarbot.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
    'content-type': "application/x-www-form-urlencoded"
    }
response = requests.request("POST", url, data=payload, headers=headers)
print(json.dumps(response, indent=4))


import requests, json

url = "https://webspellchecker-webspellcheckernet.p.rapidapi.com/ssrv.cgi"
querystring = {"format":"json","cmd":"grammar_check","text":"My name is liyan and im a 15 year old feamle and I live in Swedan, but I was born in Somalia. I escaped from somalia becous it was to dangerous, was just a little girl around two years old I think. I came to swedan with a plan. When we landed we met my cusin. They were already here. We waited until we got premission to live here, we got it a week after we came, and now I lived here since then. The first thing you need to know about me is that im muslim girl. I carry a hijab on me evreytime im outside and I'm not forced to it´s my choice, but some people around the world don´t get it. I have a big family we`re 9 people 7 kids, im the middel one I have 3 biger and 3 younger siblings. The house I live in is not that big but big enough to live in, I share room with two of my siblings one is younger and the other one is older, we always argument about who´s gonna clean and making the bed every singel morning. To have a big family is sometimes great, to talk to someone or hang out and other things but the bad to have a bige family is that".encode('utf-8'),"slang":"en_US"}
headers = {
    'x-rapidapi-host': "webspellchecker-webspellcheckernet.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870"
}

response = requests.request("GET", url, headers=headers, params=querystring).json()
print(json.dumps(response, indent=4))

"""

import requests, json

essay_text = "My name is liyan and im a 15 year old feamle and I live in Swedan, but I was born in Somalia. I escaped from somalia becous it was to dangerous, was just a little girl around two years old I think. I came to swedan with a plan. When we landed we met my cusin. They were already here. We waited until we got premission to live here, we got it a week after we came, and now I lived here since then. The first thing you need to know about me is that im muslim girl. I carry a hijab on me evreytime im outside and I'm not forced to it´s my choice, but some people around the world don´t get it. I have a big family we`re 9 people 7 kids, im the middel one I have 3 biger and 3 younger siblings. The house I live in is not that big but big enough to live in, I share room with two of my siblings one is younger and the other one is older, we always argument about who´s gonna clean and making the bed every singel morning. To have a big family is sometimes great, to talk to someone or hang out and other things but the bad to have a bige family is that"

url = "https://webspellchecker-webspellcheckernet.p.rapidapi.com/ssrv.cgi"

querystring = {"format":"json","cmd":"grammar_check","text":essay_text,"slang":"en_US"}

headers = {
    'x-rapidapi-host': "webspellchecker-webspellcheckernet.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(json.dumps(json.loads(requests.request("GET", url, headers=headers, params=querystring).text)[0], indent=4))
