import requests
import json


API_ENDPOINT = "http://127.0.0.1:5000/work-input"


payload = {'lesson_id': 1,
           'student_id': 1,
           'work': "#"}


r = requests.post(url=API_ENDPOINT, data=payload, verify=False)

status = r.text
print("status: " + status)
