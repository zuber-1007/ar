import requests
import linecache
import json
import time
target = linecache.getline('phn.cfg',1)
def sendPostRequest():
    response = requests.post('https://cdn-api.co-vin.in/api/v2/auth/public/generateOTP', json={'mobile': target})
    #print("Status code: ", response.status_code)
    #print("Printing Entire Post Request")
    str = json.dumps(response.json())
    substr = "txn"
    if substr in str:
        return "Success"
    else:
        return response.json()
print(sendPostRequest())
    
    
