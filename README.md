# Do_Faces_Move_Markets

## This is a code repository that can be used to replicate the methodology of our paper.

### Flow (not entirely linear, some scripts have some dependency datafiles which cant be shared):

- create_video_metadata.py
- download_videos.py
- video_to_audio.sh
- clean_audio.sh
- rename_cleanedaudio.py
- transcribe.sh #cheaper with clean audio as input.
- ID_speakerlabels_from_transcripts.py
- extract_frames.py
- cluster_frames.py
- clean_clusters.py
- jim_catcher.py
- azure_face_api.py

# ADD MORE
1. Emotion Feature Mining
2. Details of WRDS dataset
3. Data concatenation script (useless if we dont give WRDS dataset details and .do files of prof. Anand)
4. Final Reg.do file with stage1, stage2 analysis

