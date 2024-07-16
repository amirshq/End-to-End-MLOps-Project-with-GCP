
import requests

file_path = r'D:\End to End Mlops using GCP\End-to-End-MLOps-Project-with-GCP\three.png'
with open(file_path, 'rb') as file:
    resp = requests.post(" https://getprediction-ytxqog5dha-ue.a.run.app", files={'file': file})

print(resp.json())
