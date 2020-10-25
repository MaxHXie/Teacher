import requests
import json

url = "https://grammarbot.p.rapidapi.com/check"

payload = "language=en-US&text=Susan%20go%20to%20the%20store%20everyday.%20I%20like%20to%20go%20to%20store%20too%20everyday%20that%20is%20my%20favourite%20activity.%20Me%20and%20Bob%20are%20best%20friends%20that%20play%20baseball%20on%20the%20evenings%20but%20only%20on%20wensdays."
headers = {
    'x-rapidapi-host': "grammarbot.p.rapidapi.com",
    'x-rapidapi-key': "7968ecd538msh6231460df8f412ap1f8fe2jsn50cd990fd870",
    'content-type': "application/x-www-form-urlencoded"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
json_text = json.loads(response.text)

print('-----------------------------------')
print(json_text['software'])
