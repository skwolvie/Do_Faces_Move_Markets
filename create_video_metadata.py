
#############################################################
#Author: Sachin
#Email: <sachin_srinivasamurthy@isb.edu/ sachinsm2022@gmail.com>
#############################################################

#1. DOWNLOAD DETAILS OF VIDEOS IN A PLAYLIST


#Imports
#pip install google-api-python-client #run this if you dont have google-api-python-client
import os
import pandas as pd
import numpy as np
from googleapiclient.discovery import build

#My google API Keys
api_key= 'YOUR YOUTUBE API KEY' #add here
youtube= build('youtube', 'v3', developerKey=api_key)
print(os.getcwd())
os.chdir(r"YOUR DATADIR/ youtube/") #add here
print(os.getcwd())
import string
punc= string.punctuation

def remove_punc(text):
    """custom function to remove the frequent words"""
    return " ".join([word for word in str(text).split() if word not in punc])
    
def remove_blanks(text):
    """custom function to remove the frequent words"""
    return " ".join([word for word in str(text).split()])

#literal_eval function
from ast import literal_eval
def f(x):
    try:
        return literal_eval(str(x))   
    except:
        print('---------------------llllllllllllllllllllllllllllllllllllllllllllllllll---------------------------')
        return []


# Function to extract playlist details with given Playlist-ID input
def playlist(playlistid):
    nextPageToken = None
    snips = []
    df1 = pd.DataFrame()
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlistid,
            maxResults=90,
            pageToken=nextPageToken)

        response = request.execute()

        for i in response['items']:
            snips.append(i['snippet'])

        df = pd.DataFrame.from_dict(f(snips))
        df1 = pd.concat([df1, df], axis=0)

        nextPageToken = response.get('nextPageToken')
        if not nextPageToken:
            break
    df1 = df1[df1.title != 'Private video']
    df1.drop_duplicates(
        subset=['publishedAt', 'channelId', 'title', 'description', 'channelTitle', 'playlistId', 'position',
                'videoOwnerChannelTitle', 'videoOwnerChannelId'], inplace=True)
    df1['resourceId'] = df1['resourceId'].apply(lambda x: f(x))
    df1.reset_index(inplace=True, drop=True)
    dff = pd.json_normalize(df1['resourceId'])
    df1 = pd.concat([df1, dff], axis=1)
    df1.drop('resourceId', axis=1, inplace=True)
    return df1


df= playlist('YOUTUBE PLAYLIST ID') #add here
df.to_csv("V1_PlaylistDetails.csv",index=False)
df= pd.read_csv('V1_PlaylistDetails.csv')
print(df.shape)



# EDA & Cleaning
df.columns
df['publishedAt']= pd.to_datetime(df['publishedAt'])
df['date']= df['publishedAt'].dt.date
df.drop(columns=['kind', 'videoOwnerChannelId', 'videoOwnerChannelTitle', 'playlistId', 'channelTitle', 'channelId', 'thumbnails'], inplace=True)
df= df[['publishedAt', 'date', 'title', 'description', 'position', 'videoId']]
df['url']= 'https://www.youtube.com/watch?v='+df['videoId']

# feature engineering
durations=[]
definitions=[]
videoIds= df['videoId'].tolist()

for id in videoIds:
    vid_response= youtube.videos().list(part="contentDetails",id= id).execute()
    for item in vid_response['items']:
        durations.append(item['contentDetails']['duration'])

    for item in vid_response['items']:
        definitions.append(item['contentDetails']['definition'])

df['quality']= definitions
df['length_seconds']= durations
df['length_seconds']= df['length_seconds'].str.replace('PT', '')
df['min']= df['length_seconds'].str.split('M').str.get(0)
df['sec']= df['length_seconds'].str.split('M').str.get(1)
df['min']= df['min'].str.strip()
df['sec']= df['sec'].str.strip()
df['sec']= df['sec'].str.replace('S', '')

df1= df[df['sec']=='']
df2= df[df['sec']!='']

df= pd.concat([df2, df1], axis=0)
df['min']= df['min'].astype(int)
df['sec']= df['sec'].astype(int)
df['min']= df['min'].apply(lambda x: x*60)
df['length_seconds']= df['min']+df['sec']
df.drop(columns=['min', 'sec'], axis=1, inplace=True)
df.sort_values(by='position', ignore_index=True, inplace=True)

df['video_title']= df['title']+df['videoId']
df['video_title']= df['video_title'].str.replace(r"\s+",'')
df['video_title']= df['video_title'].str.replace(r"[^\w\s]",'')
df['video_title']= df['video_title'].apply(lambda x: remove_punc(x))
df['video_title']= df['video_title'].str.replace(r"_",'')
df['video_title']= df['video_title'].str.replace(r"ó",'o')

df['title']= df['title'].str.lower()
df['title']= df['title'].str.replace('\n', ' ')
df['title']= df['title'].str.replace('\t', ' ')
df['title']= df['title'].str.strip()
df['title']= df['title'].apply(lambda x: remove_punc(x))
df["title"] = df['title'].str.replace('[^\w\s]','')
df['title']=df['title'].str.replace('mad money cnbc', '')
df['title']=df['title'].str.replace('mad', '')
df['title']=df['title'].str.replace('money', '')
df['title']=df['title'].str.replace('cnbc', '')
df['title']= df['title'].apply(lambda x: remove_blanks(x))
df['title']= df['title'].str.strip()

df['description']= df['description'].str.split('»').str.get(0)
df['description']= df['description'].str.replace('\r', '')
df['description']= df['description'].str.replace('\n', '')
df['description']= df['description'].str.strip()

df['text']= df['title']+ ' ' + df['description']
df['text']= df['text'].str.lower()
df['text']= df['text'].str.replace('\n', ' ')
df['text']= df['text'].str.replace('\t', ' ')
df['text']= df['text'].str.replace('\r', ' ')
df['text']= df['text'].str.strip()
df['text']= df['text'].apply(lambda x: remove_punc(x))
df["text"] = df['text'].str.replace('[^\w\s]','')
df['text']= df['text'].str.strip()
df['text']= df['text'].apply(lambda x: remove_blanks(x))

df= df[['publishedAt', 'date', 'position', 'quality', 'length_seconds', 'url', 'videoId', 'title', 'description', 'video_title', 'text']]
df.to_csv('V2_PlaylistDetails.csv', index=False)


# FEATURE BASED FILTERING
for i in df['text'].tolist():
    print(i)
    print()

#let go of non-ceo interviews
df1= df[~df['text'].str.contains('ceo')] 
for i in df1['text'].tolist():
    print(i)
    print()
df1.to_csv('DATA DIR/backup/NONCEO_interviews.csv', index=False)
del df1

df= df[df['text'].str.contains('ceo')]
df.sort_values(by='position', ignore_index=True, inplace=True)


#let go of non-hd videos and short videos
print(df['quality'].value_counts())
print(df[df['length_seconds']<300])
df.iloc[[337, 469, 924, 1105, 1111, 1141, 1307, 1522, 1646]].to_csv('DATADIR/backup/ShortInterviews.csv', index=False)
df.drop(df.index[[337, 469, 924, 1105, 1111, 1141, 1307, 1522, 1646]], inplace=True)
df.sort_values(by='position', ignore_index=True, inplace=True)
df.shape

low = pd.read_csv('DATADIR/backup/videos360p.csv') #found out by using ffmpeg. Contibution of Intern Anshu Sharma
df= df[~df['video_title'].isin(low['video_title'])]
df.sort_values(by='position', ignore_index=True, inplace=True)

#find cname from title
df['cname_title']= df['title'].str.split('ceo').str.get(0)
df['cname_title'].value_counts()
df.to_csv("V3_PlaylistDetails.csv", index=False)


#reading and mapping CEO Name, Company Name with the help of AWS NER, and manual human validators.
#mapped features includes useful Flags which can be automated with OpenCV if required.
ref1= pd.read_csv('DATADIR/backup/V4_NER_mapped_results.csv')
ref1.rename(columns={'URL':'url'}, inplace=True)

df= pd.merge(df, ref1[['position', 'url', 'cname', 'CEO', 
                     'Flag_video_call', 'Flag_Multiple', 'Flag_multiple_CEO', 'CEO_1', 'CEO_2', 'Other_CNAME_1', 'Other_CNAME_2', 'comments']], 
                     left_on=['position', 'url'], 
                     right_on=['position', 'url'])

df.to_csv('DATADIR/youtube/Final_PlaylistDetails.csv', index=False)
df['date']= pd.to_datetime(df['date'])




# ADDING BASIC CEO AND FIRM IDENTIFIERS TO THE DATASET
dff= pd.read_stata("DATADIR/WRDS/LISTED_COMPANIES_ALLDATA_2013_2020.dta")
dff= dff[dff['CEOANN']=='CEO']
dff.reset_index(inplace=True, drop=True)
dff['CEO']= dff['EXEC_FULLNAME'].str.split(',').str.get(0)
df['CEO']= df['CEO'].str.split(',').str.get(0)
df[~df['CEO'].isin(dff['CEO'])]['CEO'].unique()

df['CEO']= df['CEO'].str.replace('Kevin R. Sayer', 'Kevin Ronald Sayer')
df['CEO']= df['CEO'].str.replace('Sheryl D. Palmer', 'Sheryl Denise Palmer')
df['CEO']= df['CEO'].str.replace('Hassane El-Khoury', 'Hassane S. El-Khoury')
df['CEO']= df['CEO'].str.replace('Michael S. Dell', 'Michael Saul Dell')
df['CEO']= df['CEO'].str.replace('Kevin R. Sayer', 'Geoffrey A. Ballotti')
df['CEO']= df['CEO'].str.replace('Scott W. Wine', 'Scott Wellington Wine')
df['CEO']= df['CEO'].str.replace('Andrew Liveris', 'Andrew N. Liveris')


df= df[df['url']!='https://www.youtube.com/watch?v=oJaDUf4-a3w']
df.sort_values(by='position', inplace=True, ignore_index=True)

df= df[df['cname']!='WYNDHAM DESTINATIONS INC']
df.sort_values(by='position', inplace=True, ignore_index=True)

df['cname']= df['cname'].str.upper()

dff['cname']= dff['CONAME'].str.replace("-CL A",'')
dff['cname']= dff['cname'].str.replace("HLDGS",'')
dff['cname']= dff['cname'].str.replace("CO/DE",'')
dff['cname']= dff['cname'].str.replace("INC/DE",'')

dff['cname']= dff['cname'].str.replace(r"[^\w\s]",'')
dff['cname']= dff['cname'].apply(lambda x: remove_blanks(x))
dff['cname']= dff['cname'].str.strip()

dff['cname']= dff['cname'].str.replace("RH",'RESTORATION HARDWARE')
dff['cname']= dff['cname'].str.replace("CHARLES RIVER LABS INTL INC",'CHARLES RIVER LABS INC')
dff['cname']= dff['cname'].str.replace('JOHNSON CONTROLS INTL PLC', 'JOHNSON CONTROLS PLC')
dff['cname']= dff['cname'].str.replace('DONNELLEY R R SONS CO', 'DONNELLEY RR SONS CO')

dff['cname']= dff['cname'].str.replace(r"[^\w\s]",'')
dff['cname']= dff['cname'].apply(lambda x: remove_blanks(x))
dff['cname']= dff['cname'].str.strip()

df['cname']= df['cname'].str.replace("J2 GLOBAL INC",'ZIFF DAVIS INC')
df['cname']= df['cname'].str.replace("TRINSEO SA",'TRINSEO PLC')
df['cname']= df['cname'].str.replace("CHUBB",'CHUBB LTD')
df['cname']= df['cname'].str.replace("MILLER HERMAN INC",'MILLERKNOLL INC')
df['cname']= df['cname'].str.replace("ALCOA INC",'ALCOA CORP')
dff['cname']= dff['cname'].str.replace('DONNELLEY R R SONS CO', 'DONNELLEY RR SONS CO')

dff['cname']= dff['cname'].str.replace(r"[^\w\s]",'')
dff['cname']= dff['cname'].apply(lambda x: remove_blanks(x))
dff['cname']= dff['cname'].str.strip()
dff.drop_duplicates(subset=['CEO', 'cname'], inplace=True)

df= pd.merge(df, dff[['EXEC_FULLNAME', 'CO_PER_ROL', 'CONAME', 'CEOANN', 'AGE', 'GVKEY',
       'EXECID', 'TITLE', 'EXEC_LNAME', 'EXEC_FNAME', 'EXEC_MNAME',
       'GENDER', 'NAMEPREFIX', 'CUSIP', 'CITY', 'STATE', 'ZIP', 'TICKER',
       'NAICS', 'SIC', 'CEO', 'cname']], 
       
       left_on=['CEO', 'cname'], 
       right_on=['CEO', 'cname'], 
       how='inner')
    
df.sort_values(by='position', inplace=True, ignore_index=True)

dff[(dff['cname'].isin(df['cname'])) & (dff['CEO'].isin(df['CEO']))].to_csv(
    'DATADIR/WRDS/simplified_infer.csv', index=False)

# FINAL DESCRIPTIVES
df['length_seconds'].describe()
(df['length_seconds'].sum()/60)/60
df['date'].value_counts()
df['CEO'].value_counts()
df['cname'].value_counts()
df.to_csv('DATADIR/YOUTUBE/FINAL_YOUTUBE_SUBSET.csv', index=False)