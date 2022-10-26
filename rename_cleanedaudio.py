#############################################################
#Author: Anshu Sharma
#Email: <anshu_sharma@isb.edu>
#############################################################
# the output of cleaning audio file results in creation of folders with vocals and noise.
# this script renames the vocals.wav file as the input file name and stores it to a new dir "DATADIR/youtube/audio/cleaned/cleaned_renamed/"

import os, shutil, glob
os.chdir(r"DATADIR/youtube/audio/cleaned/")
os.mkdir('cleaned_renamed/')
os.getcwd()

print(len(os.listdir()))
print(len(list(set(os.listdir()) - {'desktop.ini', '.ipynb_checkpoints'})))

for i in list(set(os.listdir()) - {'desktop.ini', '.ipynb_checkpoints'}):
    try:
        os.chdir(i)
        print(i, os.listdir())
        os.remove("accompaniment.wav")
        os.chdir('..')
        print()
    except:
        print(i, 'what is this?')
        os.chdir('..')


extn='.wav'


for i in list(set(os.listdir()) - {'desktop.ini', '.ipynb_checkpoints'}):
    try:
        os.chdir(i)
        os.rename("vocals.wav", f'{i}{extn}')
        shutil.copy(os.listdir()[0], '../cleaned_renamed/')
        os.chdir('..')
    except:
        print(i, 'what is this?')
        os.chdir('..')

glob.glob()
for i in list(set(os.listdir()) - {'desktop.ini', '.ipynb_checkpoints'}):
    if i+'.wav' not in os.listdir('../cleaned_renamed/'):
        try:
            os.chdir(i)
            shutil.copy(r"{0}".format(os.getcwd()+'\\'+os.listdir()[0]), '../../cleaned_renamed/'+os.listdir()[0])
            #shutil.copy(os.listdir()[0], '../clean_renamed/')
            os.chdir('..')
        except:
            print(i, 'what is this?')
            os.chdir('..')

os.chdir('../')
os.getcwd()
os.chdir('../clean/')
print(len(os.listdir()))
