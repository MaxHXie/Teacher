import requests

url = "https://grammarbot.p.rapidapi.com/check"

payload = "language=en-US&text=Susan%20go%20to%20the%20store%20everyday.%20I%20like%20to%20go%20to%20store%20too%20everyday%20that%20is%20my%20favourite%20activity.%20Me%20and%20Bob%20are%20best%20friends%20that%20play%20baseball%20on%20the%20evenings%20but%20only%20on%20wensdays."
headers = {
    'x-rapidapi-host': "grammarbot.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)


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
    ,{"message":"'Everyday' is an adjective. Did you mean \"every day\"?","shortMessage":"Commonly confused word","replacements":[{"value":"every day"}],"offset":58,"length":8,"context":{"text":"...ore everyday. I like to go to store too everyday that is my favourite activity. Me and B...","offset":43,"length":8},"sentence":"I like to go to store too everyday that is my favourite activity.","type":{"typeName":"Other"},"rule":{"id":"EVERYDAY_EVERY_DAY","subId":"3","description":"everyday (every day)","issueType":"misspelling","category":{"id":"CONFUSED_WORDS","name":"Commonly Confused Words"}}},{"message":"Possible spelling mistake found","shortMessage":"Spelling mistake","replacements":[{"value":"favorite"}],"offset":78,"length":9,"context":{"text":"... to go to store too everyday that is my favourite activity. Me and Bob are best friends t...","offset":43,"length":9},"sentence":"I like to go to store too everyday that is my favourite activity.","type":{"typeName":"Other"},"rule":{"id":"MORFOLOGIK_RULE_EN_US","description":"Possible spelling mistake","issueType":"misspelling","category":{"id":"TYPOS","name":"Possible Typo"}}},{"message":"When referring to yourself and somebody else, put their name first. Also check whether the nominative form \"I\" is required here.","shortMessage":"","replacements":[{"value":"I"}],"offset":98,"length":2,"context":{"text":"...everyday that is my favourite activity. Me and Bob are best friends that play base...","offset":43,"length":2},"sentence":"Me and Bob are best friends that play baseball on the evenings but only on wensdays.","type":{"typeName":"Other"},"rule":{"id":"CONFUSION_OF_ME_I","subId":"6","description":"me (I)","issueType":"misspelling","category":{"id":"TYPOS","name":"Possible Typo"}}},{"message":"Possible spelling mistake found","shortMessage":"Spelling mistake","replacements":[{"value":"wens days"}],"offset":173,"length":8,"context":{"text":"...ay baseball on the evenings but only on wensdays.","offset":43,"length":8},"sentence":"Me and Bob are best friends that play baseball on the evenings but only on wensdays.","type":{"typeName":"Other"},"rule":{"id":"MORFOLOGIK_RULE_EN_US","description":"Possible spelling mistake","issueType":"misspelling","category":{"id":"TYPOS","name":"Possible Typo"}}}]}
