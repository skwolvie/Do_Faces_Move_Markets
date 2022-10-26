#############################################################
#Author: Arjun Sharma
#Email: <arjun_sharma123@outlook.com>
#############################################################
import os, glob, shutil
import pandas as pd
os.chdir(r"DATADIR/youtube/faceclusters/")
print(len(os.listdir()))
dirs=os.listdir(os.getcwd())

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
len(dir_lens)

dfi= pd.DataFrame(list(zip(dirs, dir_lens)))
dfi.columns=['dirs', 'lengths']
dfi['lengths'].describe()
dfi[dfi['lengths']==7]
count=0

for i in dirs:
    try:
        os.chdir(i)
    except:
        break
    for j in os.listdir():
        try:
            jdir= os.listdir(j)
            if len(jdir)<=30:
                count= count+1
                shutil.rmtree(j)
            else:
                pass
                #print(j, len(jdir))
        except:
            print(j, 'eno idu')
            os.remove(j)
            pass
    os.chdir('..')

print(count)

a= dfi[dfi['lengths']>=3]['dirs'].tolist()

from distutils.dir_util import copy_tree
for i in os.listdir():
    if i in a:
        print(i)
        try:
            os.mkdir(r"DATADIR/test/imgs_manual/"+i)
            shutil.copytree(i, r"DAADIR/test/imgs_manual/"+i+'/', dirs_exist_ok=True, symlinks=True)
        except:
            # shutil.rmtree(i)
            print('dir exists')
            pass

for i in os.listdir():
    if i in a:
        print(i)
        shutil.rmtree(r"DATADIR/youtube/faceclusters/"+i)
len(os.listdir())

os.chdir(r"DATADIR/test/imgs_manual/")
for i in os.listdir():
    os.chdir(r"DATADIR/test/imgs_manual/"+i)
    for i in os.listdir():
        if 'desktop' in i:
            os.remove(i)
            print(i)
# os.chdir('..')

len(os.listdir())
os.chdir(r"DATADIR/test/imgs_manual/")
b= os.listdir()
os.chdir(r"DATADIR/youtube/faceclusters/")
count=0
for i in os.listdir():
    if i in b:
        count=count+1
        #shutil.rmtree()
        os.system('rmdir /S /Q "{}"'.format(r"DATADIR/youtube/faceclusters/"+i))
        print(i)
print(count)
len(os.listdir())
510+165
