import tensorflow as tf
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import glob
import os
import sys

def load_image(img_path, show=False):

    img = image.load_img(img_path, target_size=(300, 300))
    img_tensor = image.img_to_array(img)                    
    img_tensor = np.expand_dims(img_tensor, axis=0)        
    img_tensor /= 255.             
    return img_tensor


if __name__ == "__main__":

    filename =sys.argv[1]
    r = open(filename, 'r')
    w = open("classification.txt", 'w+')
    model = load_model("309505018_VGG16pttbeauty.h5")
    for img in r:
        img = img.split("\n")[0]
        pred = model.predict([load_image(img)])
        #print(pred)
        if pred[0][0] >= 0.5017:
            w.writelines("1")
        else:
            w.writelines("0")

    r.close()
    w.close()