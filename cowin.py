import requests
import linecache
import json
import time
target = linecache.getline('cnfg.cfg',1)
limit = int(linecache.getline('cnfg.cfg',2))
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
successCount = 0
for x in range(limit):
    responseStatus = sendPostRequest()
    if responseStatus == "Success":
        successCount = successCount + 1
        print("Success Count ", successCount)
    else:
        print("Unsuccessful")
    time.sleep(180)
