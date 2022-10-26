#############################################################
#Author: Arjun Sharma
#Email: <arjun_sharma123@outlook.com>
#############################################################

#pip install spleeter-gpu
# for i in *.wav; do spleeter separate -o "../clean/${i%.wav}/" -i "$i"; done
 for i in *.wav; do spleeter separate -o "../" "$i" -p spleeter:5stems; done
