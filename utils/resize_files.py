import os
import cv2

collection = "data/alphapose_set/000_lightweight_n195"

for i, filename in enumerate(os.listdir(collection)):
    print(filename)

    img = cv2.imread(collection + '/' + filename) 
    resized_image = cv2.resize(img,(224,224)) 
    print(filename)
    cv2.imwrite("data/alphapose_set/000_lightweight_n195_xsmall/"+filename, resized_image)