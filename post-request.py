import requests
import json

url = 'http://localhost:8000/quiz'

data = {'questions_num': 3}
headers = {'Content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.content)