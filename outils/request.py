import requests

url = 'http://127.0.0.1:8080/saves/post/120'
files = {'file': open('twitter2.py')}
response = requests.post(url, files=files)
print(response.text)