#############################################################
#Author: Sachin
#Email: <sachin_srinivasamurthy@isb.edu>
#############################################################

import os, glob, shutil
import pandas as pd
import numpy as np
import os, glob
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
from deepface import DeepFace
os.chdir(r"DATADIR/youtube/faceclusters/")
print(len(list(set(os.listdir()) - {'desktop.ini', 'whatever.ini'})))
dirs=list(set(os.listdir()) - {'desktop.ini', 'whatever.ini'})

try:
    dirs.remove('desktop.ini')
    print('done')
except:
    pass
len(dirs)

dir_lens=[]
for i in dirs:
    if i!='desktop.ini':
        dir_lens.append(len(os.listdir(i)))
    else:
        print(i)

len(dirs)
dfi= pd.DataFrame(list(zip(dirs, dir_lens)))
dfi.columns=['dirs', 'lengths']
dfi['lengths'].describe()

DeepFace.verify(r"DATADIR/JIM/jimcramer.jpg", r"DATADIR/JIM/jim.png")

recheck=[]
for i in list(set(os.listdir(r"DATADIR/youtube/faceclusters/"))-{'desktop.ini', 'whatever.ini'}):
    #print(i)
    aggs=[]
    js=[]
    for j in list(
        set(
            os.listdir(r"DATADIR/youtube/faceclusters/"+i))-{'desktop.ini', 'whatever.ini'}):
        js.append(j)
        #print(j)
        list_of_files = filter( os.path.isfile, glob.glob(r"DATADIR/youtube/faceclusters/"+i+"/"+j+"/"+ '*'))
        list_of_files = sorted(list_of_files, key =  lambda x: os.stat(x).st_size)
        count=0
        result=[]
        confidence=[]
        for k in list_of_files[-50:]:
            try:
                a= DeepFace.verify(k, r"C:/Users/31405.ISBDOMAIN1/Desktop/jim.png", enforce_detection=False, detector_backend='dlib', distance_metric='euclidean_l2')
                if a:
                    #print(a)
                    count= count+1
                    #print(count, j, 'analysed', result)
                    result.append(a['verified'])
                    confidence.append(a['distance'])
                if count==10:
                    break
                #print(i, j, set(result))
            except:
                print('some dlib err')
                pass
        aggs.append(np.mean(confidence))
        nearest=aggs.index(min(aggs))
    print(i, js[nearest], min(aggs), nearest)
    try:
        os.rename(r"DATADIR/youtube/faceclusters/"+i+'/'+js[nearest], r"DATADIR/youtube/faceclusters/"+i+'/jim')
    except:
        print('jim exists')
        recheck.append(i)

count=0
for i in list(set(os.listdir(r"DATADIR/youtube/faceclusters/"))-{'desktop.ini', 'whatever.ini'}):
    for j in list(set(os.listdir(r"DATADIR/youtube/faceclusters/"+i))-{'desktop.ini', 'whatever.ini'}):
        if j=='jim':
            count=count+1
print(count)
# import pandas as pd
# recheck_df=pd.DataFrame(list(zip(recheck)))
# recheck_df.to_csv('recheck.csv', index=False)
# recheck_df
