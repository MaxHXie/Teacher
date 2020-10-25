import requests

url = "https://grammarbot.p.rapidapi.com/check"

payload = "language=en-US&text=I%20didn%E2%80%99t%20realise%20that%20I%20was%20alone%20every%20weekend%20and%20every%20day%20after%20school.%20I%20just%20kept%20following%20them%20wherever%20they%20went%20in%20school%20and%20if%20they%20were%20planning%20on%20hanging%20out%20right%20after%20school%20I%20tried%20my%20best%20to%20get%20in%20on%20the%20plans%2C%20because%20they%20weren't%20mean%20to%20me%20like%20that%2C%20they%20never%20said%20I%20couldn't%20come%20or%20that%20I%20had%20to%20go.%20They%20just%20didn't%20invite%20me%20and%20tried%20their%20best%20to%20avoid%20me."
headers = {
    'x-rapidapi-host': "grammarbot.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)

"""

{
"software":{
    "name":"GrammarBot","
    version":"4.3.1","
    apiVersion":1,
    "premium":true,
    "premiumHint":"Thanks for supporting GrammarBot!",
    "status":""
},
"warnings":{
    "incompleteResults":false
},
"language":{
    "name":"English (US)",
    "code":"en-US",
    "detectedLanguage":{
        "name":"English (US)",
        "code":"en-US"
    }
},
"matches":[
    {
        "message":"The singular proper name 'Susan' must be used with a third-person or a past tense verb: \"goes\", \"went\".",
        "shortMessage":"Agreement error",
        "replacements":[
            {"value":"goes"},
            {"value":"went"}
        ],
        "offset":6,
        "length":2,
        "context":{
            "text":"Susan go to the store everyday. I like to go to ...",
            "offset":6,
            "length":2
        },
        "sentence":"Susan go to the store everyday.",
        "type":{
            "typeName":"Other"
        },
        "rule":{
            "id":"HE_VERB_AGR",
            "subId":"8",
            "description":"Agreement error: Non-third person/past tense verb with 'he/she/it' or a pronoun",
            "issueType":"grammar",
            "category":{
                "id":"GRAMMAR",
                "name":"Grammar"
            }
        }
    },
    {
        "message":"'Everyday' is an adjective. Did you mean \"every day\"?",
        "shortMessage":"Commonly confused word",
        "replacements":[
            {"value":"every day"}
        ],
        "offset":22,
        "length":8,
        "context":{
            "text":"Susan go to the store everyday. I like to go to store too everyday tha...",
            "offset":22,
            "length":8
        },
        "sentence":"Susan go to the store everyday.",
        "type":{"typeName":"Other"},
        "rule":{
            "id":"EVERYDAY_EVERY_DAY",
            "subId":"3",
            "description":"everyday (every day)",
            "issueType":"misspelling",
            "category":{
                "id":"CONFUSED_WORDS",
                "name":"Commonly Confused Words"
            }
        }
    }
"""
