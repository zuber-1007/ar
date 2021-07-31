import requests
import linecache
import json
import time
def sendPostRequest():
    response = requests.post('https://affiliate.flipkart.com/loginWithOtp',json={'inputREmail':'fiplar@email.com','countryCode':'+91','contactNumber':'8498808803'})
    #print("Status code: ", response.status_code)
    #print("Printing Entire Post Request")
    #response.encoding = 'utf-8'
    return response.json()
print(sendPostRequest())