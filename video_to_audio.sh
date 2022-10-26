#############################################################
#Author: Arjun Sharma
#Email: <arjun_sharma123@outlook.com>
#############################################################

# run line below for mp4 to mp3
for i in *.mp4; do ffmpeg -i "$i" -ab 160k -ac 2 -ar 44100 -vn "/home/ubuntu/s3-drive/audios/raw/${i%.mp4}.wav"; done
#run line below for mp4 to wav [preffered]
for i in *.mp4; do ffmpeg -i "$i" -ac 2 -f wav -vn "/home/ubuntu/s3-drive/audios/raw/${i%.mp4}.wav"; done