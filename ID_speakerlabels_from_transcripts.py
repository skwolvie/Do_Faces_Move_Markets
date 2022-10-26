#############################################################
#Author: Sachin
#Email: <sachin_srinivasamurthy@isb.edu>
#############################################################
import sys
import json
import datetime
import os
import json
import pandas as pd
import time as t

os.chdir(r"DATADIR/youtube/transcripts/transcript json/") #edit here

# transcripts = ''
# with open(os.listdir()[0]) as f:
#     text = json.load(f)
# for i in text['results']['transcripts']:
#     transcripts += i['transcript']
# print(transcripts)

def write_transcripts(transcript_filename, transcripts):
    f = open(transcript_filename, "w+")
    f.write(transcripts)
    f.close()

def convert_to_text(name):
    if name[:-5]+'.txt' not in os.listdir('../transcript text/'):
        print(name[:-5]+'.txt', 'illa')
        transcripts = ''
        with open(name, encoding='utf-8', errors='ignore') as f:
            text = json.load(f,strict=False)
        for i in text['results']['transcripts']:
            transcripts += i['transcript']
        write_transcripts('../transcript text/'+name[:-5]+ '.txt', transcripts)

for i in os.listdir():
    convert_to_text(i)

def segments(raw):     
    filename2=raw
    with open(filename2) as f:
        data=json.loads(f.read())
        labels = data['results']['speaker_labels']['segments']
        speaker_start_times={}
        for label in labels:
            for item in label['items']:
                speaker_start_times[item['start_time']] =item['speaker_label']
        items = data['results']['items']
        finaldict=[]
        lines=[]
        line=''
        time=0
        speaker='null'
        i=0
        for item in items:
            i=i+1
            content = item['alternatives'][0]['content']
            if item.get('start_time'):
                current_speaker=speaker_start_times[item['start_time']]
            elif item['type'] == 'punctuation':
                line = line+content
            if current_speaker != speaker:
                if speaker:
                    lines.append({'speaker':speaker, 'line':line, 'time':time})
                line=content
                speaker=current_speaker
                time=item['start_time']
            elif item['type'] != 'punctuation':
                line = line + ' ' + content
            lines.append({'speaker':speaker, 'line':line,'time':time})
            sorted_lines = sorted(lines,key=lambda k: float(k['time']))
            sorted_lines[:] = [d for d in sorted_lines if d.get('speaker') != 'null']
        df= pd.DataFrame(sorted_lines)
        print(df.shape)
        df.drop_duplicates(inplace=True)
        df.reset_index(inplace=True,drop=True)
        print(df.shape)
        return df


convos=[]
for i in sorted(os.listdir('../transcript text')):
    convos.append('../transcript text/'+i)

raws=[]
for i in sorted(os.listdir()):
    raws.append(i)

ref=pd.DataFrame(list(zip(convos, raws)), columns=['convos', 'raws'])


# lst=[]
# for i in range(0, len(df)-1):
#     if df['speaker'][i] != df['speaker'][i+1]:
#         lst.append(df.iloc[i])
# lst
# final.reset_index(inplace=True, drop=True)
# final


if __name__ == '__main__':
    for obs in range(len(ref)):
        df=segments(ref['raws'][obs])
        df.reset_index(inplace=True, drop=True)
        df.drop_duplicates(subset=['speaker', 'time'], keep='last', inplace=True)
        df.reset_index(inplace=True, drop=True)
        df.to_csv('../transcript conversation tree/'+ref['raws'][obs][:-5]+'.csv', index=False)
        print(df.shape)




# determining unique speakers in the video, and MANUALLY eleminating heterogenous cases from analysis.
# IGNORE THIS PART. ADDED IT ONLY FOR REFERENCE.
os.chdir('../transcript conversation tree')
count=0
count2=[]
for i in os.listdir():
    if i.startswith('trans'):
        os.rename(i, i[11:])
        df= pd.read_csv(i[11:])
        if len(df['speaker'].unique())==2:
            count=count+1
            count2.append(i[11:])
    else:
        df= pd.read_csv(i)
        if len(df['speaker'].unique())==2:
            count=count+1
            count2.append(i)


import shutil
for i in count2:
    shutil.copy(i, 'len2/'+i)
count=0
count3=[]
for i in os.listdir():
    #print(i)
    if i.endswith('.csv'):
        df= pd.read_csv(i)
        if len(df['speaker'].unique())==3:
            count=count+1
            count3.append(i)

count
703+223
import shutil
for i in count3:
    shutil.copy(i, 'len3/'+i)
count=0
count4=[]
for i in os.listdir():
    #print(i)
    if i.endswith('.csv'):
        df= pd.read_csv(i)
        if len(df['speaker'].unique())>3:
            count=count+1
            count4.append(i)

count
import shutil
for i in count4:
    shutil.copy(i, 'len4/'+i)
