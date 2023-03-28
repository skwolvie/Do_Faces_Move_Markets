#############################################################
#Author: Sachin
#Email: <sachin_srinivasamurthy@isb.edu>
#############################################################

import tensorflow as tf
print(tf.test.is_gpu_available())
tf.config.list_physical_devices('GPU')
from tensorflow.python.client import device_lib 
print(device_lib.list_local_devices())
from keras_facenet import FaceNet
import dlib
import os, glob
import cv2 
from sklearn.cluster import KMeans
from time import time
import matplotlib.pyplot as plt

embedder = FaceNet()

frames_folder_path = r'DATADIR/youtube/frames/'
faceclusters_folder_path = 'DATADIR/youtube/face_clusters/'
os.chdir(frames_folder_path)
frames_folders=os.listdir()
len(frames_folders)

# photo=r"D:\31405_CEO_Project\CEO_Mindset_Personality_Impact\Youtube_Cramer_Interviews\frames\frames720p\ChipotleMexicanGrillCEOandCFOEngagingwithMillennialsMadMoneyCNBCEO3A9pT3RvQ\frame_6583.jpg"
# img=dlib.load_rgb_image(photo)
# detections= embedder.extract(img, threshold=0.95)
# for i in detections:
#     cv2.imshow(i)


hog_face_detector = dlib.get_frontal_face_detector()
def hogDetectFaces(image, hog_face_detector, display = True):

    height, width, _ = image.shape

    output_image = image.copy()

    imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    start = time()

    results = hog_face_detector(imgRGB, 0)

    end = time()

    for bbox in results:

        x1 = bbox.left()
        y1 = bbox.top()
        x2 = bbox.right()
        y2 = bbox.bottom()

        cv2.rectangle(output_image, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=width//200)  

    if display:

        cv2.putText(output_image, text='Time taken: '+str(round(end - start, 2))+' Seconds.', org=(10, 65),
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=width//700, color=(0,0,255), thickness=width//500)

        plt.figure(figsize=[15,15])
        plt.subplot(121);plt.imshow(image[:,:,::-1]);plt.title("Original Image");plt.axis('off');
        plt.subplot(122);plt.imshow(output_image[:,:,::-1]);plt.title("Output");plt.axis('off');

    else:

        return output_image, results


# hogDetectFaces(cv2.imread(r"D:\OneDrive - Indian School of Business\Desktop\all ceo\images.jpg"), hog_face_detector, display=True)
# hogDetectFaces(cv2.imread(r"D:\OneDrive - Indian School of Business\Desktop\all ceo\jim.png"), hog_face_detector, display=True)
# hogDetectFaces(cv2.imread(photo), hog_face_detector, display=True)


def cluster_faces(frames_folders):
    start=time.time()
    for frames_folder in frames_folders:
        print('working on', frames_folder)
        images = []
        faces = 0 
        delstore = []
        facedet = []

        for f in glob.glob(os.path.join(frames_folder_path+ f'/{frames_folder}/', "*.jpg")):
            try:
                img = dlib.load_rgb_image(f)
                detections = embedder.extract(img, threshold=0.95)
                images.append(img)
                faces = faces + len(detections)

                for i in range(len(detections)):
                    #print(detections[i]['box'])
                    w= detections[i]['box'][3]
                    h= detections[i]['box'][2]
                    if(w<=10 or h<=10):
                        #print('small')
                        w= detections[i]['box'].pop(3)
                        h= detections[i]['box'].pop(2)
                        y= detections[i]['box'].pop(1)
                        x= detections[i]['box'].pop(0)
                        if x-10<0 or y-10<0:
                            detections[i]['box'].append(x)
                            detections[i]['box'].append(y)
                            detections[i]['box'].append(h)
                            detections[i]['box'].append(w)
                            
                        else:
                            detections[i]['box'].append(x-10)
                            detections[i]['box'].append(y-10)
                            detections[i]['box'].append(h+20)
                            detections[i]['box'].append(w+20)
                    elif (11>w<=25 or 11>h<=50):
                        #print('medium')
                        w= detections[i]['box'].pop(3)
                        h= detections[i]['box'].pop(2)
                        y= detections[i]['box'].pop(1)
                        x= detections[i]['box'].pop(0)
                        if x-15<0 or y-15<0:
                            detections[i]['box'].append(x)
                            detections[i]['box'].append(y)
                            detections[i]['box'].append(h)
                            detections[i]['box'].append(w)
                            
                        else:
                            detections[i]['box'].append(x-15)
                            detections[i]['box'].append(y-15)
                            detections[i]['box'].append(h+30)
                            detections[i]['box'].append(w+30)
                    else:
                        #print('large')
                        #print(detections[i]['box'])
                        w= detections[i]['box'].pop(3)
                        h= detections[i]['box'].pop(2)
                        y= detections[i]['box'].pop(1)
                        x= detections[i]['box'].pop(0)
                        if x-25<0 or y-25<0:
                            detections[i]['box'].append(x)
                            detections[i]['box'].append(y)
                            detections[i]['box'].append(h)
                            detections[i]['box'].append(w)
                            
                        else:
                            detections[i]['box'].append(x-25)
                            detections[i]['box'].append(y-25)
                            detections[i]['box'].append(h+50)
                            detections[i]['box'].append(w+50)
                
                for i in range(len(detections)):
                    delstore.append(detections[i]['embedding']) #generating 512d vectors for each detected face
                    facedet.append((img,detections[i]['box']))  #storing the bounding box of each detected face

            except:
                print('dlib read error')
            
        delstorevec = []
        for i in delstore:
            delstorevec.append(dlib.vector(i))

        #chinese whispher graph clustering
        labels = dlib.chinese_whispers_clustering(delstorevec, 0.9)
        num_classes = len(set(labels)) # Total number of clusters
        print("Number of clusters: {}".format(num_classes))

        #creating output directories for clusters
        output_folder = faceclusters_folder_path +"/"+ frames_folder
        for i in range(0, num_classes):
            output_folder_path = output_folder + '/output' + str(i)
            os.path.normpath(output_folder_path)
            try:
                os.makedirs(output_folder_path)
            except:
                print('path exists')
        for i in range(len(labels)):
            t = labels[i] 
            output_folder_path = output_folder + '/output' + str(t) # Output folder for each cluster
            img = facedet[i][0]
            face = img[facedet[i][1][1]:(facedet[i][1][1]+facedet[i][1][3]),facedet[i][1][0]:(facedet[i][1][0]+facedet[i][1][2])]
            #please name facial boxes extracted accordingly
            file_path = os.path.join(output_folder_path,"face_"+str(t)+"_"+str(i))+".jpg"
            try:
                cv2.imwrite(file_path,cv2.cvtColor(face, cv2.COLOR_RGB2BGR))
            except:
                print(file_path, ' write error')
        print('time:', time.time()- start)




cluster_faces(frames_folders)
