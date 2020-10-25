"""

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

"""

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
