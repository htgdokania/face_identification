import os
import cv2
from PIL import Image
import numpy as np
import pickle

recognizer = cv2.face.LBPHFaceRecognizer_create()
face_cascade =cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
image_dir=os.path.join(BASE_DIR,"images")
current_id =0
label_ids={}
y_labels=[]
x_train =[]
for root,dirs,files in os.walk(image_dir):
    
    for file in files:
        
        if(file.endswith("jpeg") or file.endswith("jpg") or file.endswith("png")):
            
            path=os.path.join(root,file)
            label=os.path.basename(os.path.dirname(path)).replace(" ","-").lower()
           # print(label,path)
            if label in label_ids:
                
                pass
            else:
                
                label_ids[label]=current_id
                current_id+=1

            id_=label_ids[label]
            print(label_ids)
            #y_labels.append(label1)#some number
            #x_train.append(path)#verify this image,turn it into a NUMPY array,gray
            pil_image =Image.open(path).convert("L") #convert to gray
            image_array=np.array(pil_image,"uint8")
            #print(image_array)
            faces=face_cascade.detectMultiScale(image_array,1.5,5)

            for(x,y,w,h) in faces:
                
                roi=image_array[y:y+h,x:x+w]
                x_train.append(roi)
                y_labels.append(id_)
#print(y_labels)
#print(x_train)
with open("labels.pickle",'wb') as f:
    pickle.dump(label_ids,f)
    
recognizer.train(x_train,np.array(y_labels))
recognizer.save("trainner.yml")
