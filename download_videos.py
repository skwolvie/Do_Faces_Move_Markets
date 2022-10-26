#############################################################
#Author: Sachin
#Email: <sachin_srinivasamurthy@isb.edu>
#############################################################
# DOWNLOAD VIDEOS WITH PYTUBE

# IMPORT PACKAGES
import os
import re
import pandas as pd
from pytube import YouTube
from threading import Thread
import unicodedata
os.chdir("DATADIR/youtube/videos/") #here
# Read file and create a list of links to download videos
df= pd.read_csv(r"DATADIR/youtube/V3_PlaylistDetails.csv")
links=df['URL'].tolist()
print(len(links)) # i have around 1100 videos
#split it into multiple lists for parallel downloading of videos (11 equal threads)
l0=links[:100]
l1=links[100:200]
l2=links[200:300]
l3=links[300:400]
l4=links[400:500]
l5=links[500:600]
l6=links[600:700]
l7=links[700:800]
l8=links[800:900]
l9=links[900:1000]
l10=links[1000:]

# function safe file name
def safe_filename(s: str, max_length: int = 255) -> str:
    # Characters in range 0-31 (0x00-0x1F) are not allowed in ntfs filenames.
    ntfs_characters = [chr(i) for i in range(0, 31)]
    characters = [r'"',r"\#",r"\$",r"\%",r"'",r"\*",r"\,",r"\.",r"\/",r"\:",r'"',r"\;",r"\<",r"\>",r"\?",r"\\",r"\^",r"\|",r"\~",r"\\\\",r"(",r")"]
    pattern = "|".join(ntfs_characters + characters)
    regex = re.compile(pattern, re.UNICODE)
    filename = regex.sub("", s)
    return filename[:max_length].rsplit(" ", 0)[0]

# function simplify name
def simplify(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass
    text = unicodedata.normalize('NFD', text.decode('utf-8')).encode('ascii', 'ignore').decode("utf-8")
    return str(text)

# function to download videos
def downloader(lnks, threadlabel):
    failed=[]
    #holds links so that we can retry to download those we missed
    for link in lnks:
        try:
            yt = YouTube(link)
            #print(yt.title)
            name= safe_filename(yt.title)
            name= name.strip()
            name= name.encode("utf-8")
            name= simplify(name)
            name= re.sub('[^A-Za-z0-9]+', '', name)
            name= name.replace('[^\w\s]', '')
            print(name)
            if name + '.mp4' not in os.listdir(r'DATADIR/youtube/videos'):
                print(yt.streams.order_by('resolution').desc())
                print('----------------------------------------------------------------------------------------')
                print(yt.streams.filter(progressive=True, file_extension='mp4', type="video").order_by('resolution').desc().first())
                yt.streams.filter(progressive=True, file_extension='mp4', type="video").order_by('resolution').desc().first().download(output_path=r'D:\CEO_Mindset_Personality_Impact\Youtube_Cramer_Interviews\videos\VideosBackup', filename= name)
            else:
                print(name, ' done')
                pass
        except:
            print('----------------------', link, 'not downloaded','----------------------')
            failed.append(link)
            break
    if len(failed)!=0:
        print(failed)
        with open('failed_'+threadlabel+'.txt', 'w+') as f:
            f.write(failed)

PARALLE EXECUTION
t0 = Thread(target=downloader, args=(l0, 't0'))
t1 = Thread(target=downloader, args=(l1, 't1'))
t2 = Thread(target=downloader, args=(l2, 't2'))
t3 = Thread(target=downloader, args=(l3, 't3'))
t4 = Thread(target=downloader, args=(l4, 't4'))
t5 = Thread(target=downloader, args=(l5, 't5'))
t6 = Thread(target=downloader, args=(l6, 't6'))
t7 = Thread(target=downloader, args=(l7, 't7'))
t8 = Thread(target=downloader, args=(l8, 't8'))
t9 = Thread(target=downloader, args=(l9, 't9'))
t10= Thread(target=downloader, args=(l10, 't10'))

t0.start()
t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()
t9.start()
t10.start()

t0.join()
t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
t9.join()
t10.join()


#############################################################
#Author: Sachin
#Email: <sachin_srinivasamurthy@isb.edu>
#############################################################
# DOWNLOAD VIDEOS WITH YOUTUBE_DL

#all data prep steps remains the same, and also the threading execution remains the same.
#only the function changes:
def thread_downloader(urls, threadname):
    for i in urls:
        print(threadname)
        os.system("yt-dlp {0} --extractor-args youtube:player_client=android --throttled-rate 1000K".format(i))