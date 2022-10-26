#############################################################
#Author: Sachin
#Email: <sachin_srinivasamurthy@isb.edu>
#############################################################

# {
# 	"AadClientId": "",
# 	"AadSecret": "",
# 	"AadTenantDomain": "",
# 	"AadTenantId": "",
# 	"AccountName": "",
# 	"ResourceGroup": "",
# 	"SubscriptionId": "",
# 	"ArmAadAudience": "https://management.core.windows.net",
# 	"ArmEndpoint": "https://management.azure.com"
# }

# https://cramer.cognitiveservices.azure.com/

RESOURCE = "https://management.core.windows.net/" #RESOURCE
TENANT_ID = "" #AadTenantId
CLIENT = "" #AadClientId
ACCOUNT_NAME = "" #Media Service account name
RESOUCE_GROUP_NAME = "" #Resource group
KEY = "" #AadSecret
SUBSCRIPTION_ID = "" #SubscriptionId

import adal
from azure.mgmt.media import AzureMediaServices
from msrestazure.azure_active_directory import AdalAuthentication
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD

import pandas as pd
import requests
import json
import os
from threading import Thread


os.chdir(r"DATADIE/youtube/faceclusters")
print(len(list(set(os.listdir()) - {'desktop.ini', 'whatever.ini'})))
lst=list(set(os.listdir()) - {'desktop.ini', 'whatever.ini'})
lst1=lst[:100]
lst2=lst[100:200]
lst3=lst[200:300]
#... create lists

LOGIN_ENDPOINT = AZURE_PUBLIC_CLOUD.endpoints.active_directory
RESOURCE = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id

context = adal.AuthenticationContext(LOGIN_ENDPOINT + "/" + TENANT_ID)
credentials = AdalAuthentication(context.acquire_token_with_client_credentials, RESOURCE, CLIENT, KEY)
client = AzureMediaServices(credentials, SUBSCRIPTION_ID) # The AMS Client

print(client.assets.list(RESOUCE_GROUP_NAME, ACCOUNT_NAME))
help(client)

#FACE API CREDS
subscription_key = ''
uri_base = 'https://cramer.cognitiveservices.azure.com/'


#******************* Azure Config ***********************#
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': 'age, gender, headPose, smile, emotion',
}
try:      
    body = open(r"test_humanface.jpg",'rb').read()
    response = requests.request('POST', uri_base + '/face/v1.0/detect', data=body, headers=headers, params=params)
    parsed = json.loads(response.text)
except:
    print('Error:')
    
print(parsed)


def face_analyze(dirlist, name):
    print(name)
    for i in dirlist:
        df= pd.DataFrame()
        print('working on ', i)
        face_folders=list(set(os.listdir(i)) - {'desktop.ini', 'whatever.ini'})
        face_folders.remove('jim')
        print(face_folders[0], ' has ', len(os.listdir(i+'/'+face_folders[0]+'/')), 'faces')
        images_found=len(os.listdir(i+'/'+face_folders[0]+'/'))
        images_analyzed=len(os.listdir(i+'/'+face_folders[0]+'/'))
        for img in os.listdir(i+'/'+face_folders[0]+'/'):
            try:      
                body = open(r"D:/CEO_Mindset_Personality_Impact/Youtube_Cramer_Interviews/faceclusters_720p/"+i+'/'+face_folders[0]+'/'+img,'rb').read()
                response = requests.request('POST', uri_base + '/face/v1.0/detect', data=body, headers=headers, params=params)
                parsed = json.loads(response.text)
                dfi=pd.json_normalize(parsed)
                dfi['image_name']= img
                df= pd.concat([df, dfi], axis=0)
            except:
                images_analyzed= images_analyzed-1
                print('Error:')     
        df['videoName']= i
        df['faces_captured']=images_found
        df['faces_analyzed']= images_analyzed
        print(df.shape)
        df.to_csv(r"D:/CEO_Mindset_Personality_Impact/Youtube_Cramer_Interviews/face_analysis/"+i+'.csv', index=False)
df
t1 = Thread(target=face_analyze, args=(lst1, 'first'))
t2 = Thread(target=face_analyze, args=(lst2, 'second')) 
t3 = Thread(target=face_analyze, args=(lst3, 'third'))

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()