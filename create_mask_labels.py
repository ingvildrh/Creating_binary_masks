import numpy as np
import cv2
import json
import os
from PIL import Image
import shutil

'''
This program reads a JSON file with annotations of desired regions created with this annotation tool:
 https://www.robots.ox.ac.uk/~vgg/software/via/via_demo.html
The file is saved as a JSON file which can be properly shown in a JSON viewer:
 http://jsonviewer.stack.hu/
This file needs a JSON file made with Annotation->Export annotations as Json 
The YOUTUBE guide followed to create theese masks is here: https://www.youtube.com/watch?v=AYLJ3YC07oI&t=1398s

'''

JSON_FILE_PATH = 'wounds_113_0329_json.json'

#The directory to the images which have been annotated
IMG_DIR = "C:/Users/ingvilrh/OneDrive - NTNU/IMAGE_ACQUISITION/113_0329" 

#The directory where the mask labels will be saved
MSK_DIR = "C:/Users/ingvilrh/OneDrive - NTNU/MASTER_CODE23/CREATING MASKS/mask_labels_113_0329/"

#Reading JSON file
f = open(JSON_FILE_PATH) 
data = json.load(f)


#Loop over the data and save the masks
# for file_name in os.listdir(IMG_DIR):
#     image = Image.open(IMG_DIR+"/"+file_name)
#     image.show()
#     print(file_name)

'''
This function creates the masks from the JSON file
Input: JSON file
'''
def create_masks(annotation_data):
    for key, value in annotation_data.items():
        filename = value["filename"]

        img_path = IMG_DIR + "/" + filename
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        h, w, _= img.shape
        
        mask = np.zeros((h,w))

        regions = value["regions"]
        for region in regions:
            shape_attribues = region["shape_attributes"]
        
            x_points = shape_attribues["all_points_x"]
            y_points = shape_attribues["all_points_y"]

            contours = []
            for x,y in zip(x_points, y_points):
                contours.append((x,y))
            contours = np.array(contours)
            

            cv2.drawContours(mask, [contours],-1, 255, -1) #if last -1 is changed, the number is a line width

        cv2.imwrite(MSK_DIR+filename, mask)
            

        cv2.imwrite("mask_dir.png", mask)

'''
This function removes the duplicates from the images directory file and copy all images that have annotations to a new directory
'''
def remove_duplicates(annotations, oldImgPath, newImgPath):
    for image in annotations.items():
        filename = image[1]['filename']
        if os.path.isfile(oldImgPath + "/" + filename):
            shutil.copy2((oldImgPath + "/" + filename), (newImgPath + "/" + filename))


def main():
    create_masks(data)
    remove_duplicates(data, IMG_DIR, "annotated_images_113_0329/")


if __name__ == "__main__":
    main()


