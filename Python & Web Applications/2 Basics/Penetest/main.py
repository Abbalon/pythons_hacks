import requests

response = requests.get('https://web.whatsapp.com/')

if(response.status_code == 200):
    print("ok")
else:
    print(response.text)
