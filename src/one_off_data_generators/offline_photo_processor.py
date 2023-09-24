import numpy as np
import pandas as pd 
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import os
from one_off_data_generators.utils import find_nr_in_string, get_surname_withour_nr, get_list_of_available_patient_nrs, save_remove_from_list


# IMAGE_PATH = f"Pacjenci/"
# IMAGE_PATH = f"../PatientsPhotos/"
IMAGE_PATH = f"../../data/PatientsPhotos/"

def get_image(patient_nr, image_type = "2d_snapshots", only_face = True, before = True, photo_nr = 1, additional_pixels = 200):
    """
    patient_nr: int
    image_type: str 
        "2d_snapshots" - snapshots of 3d rotating image
        "3d" - 3d image
        "2d_source" - source images that construct 3d image
    only_face: boolean
        if True - detect and return only the face
        if False - return entire pic
    before: boolean
        if True - return photos before treatment
        if False - return photos after treatment

    photo_nr: int
        nr of photo in the subdirectory
        Format as follows:
            For 2d_source (entire person w. background):
                1/2 - front
                3/4 - left side (entire length of person)
                5/6 - right side (entire length of person)
            For 2d_snapshot:
                1. - right side
                2. - right side tilted 45 degrees
                3. - left side tilted 45 degrees
                4. - left side 
                5. - top view
                6. - front (best photo)
                7. - chin view

    additional_pixels: int 
        how many pixels to include around initial face position
    """
    # Run input checks
    assert photo_nr > 0
    if image_type=="2d_snapshots":
        assert photo_nr <= 7
    elif image_type=="2d_source":
        assert photo_nr <= 6
    elif image_type == "3d":
        assert photo_nr == 1
    else : 
        raise Exception(f"image type has to be one of: ['2d_snapshots', '2d_source', '3d']. It was: {image_type}")



    
    # append given patient_nr
    STR_PATIENT_FOLDER = find_patient_folder_given_patient_nr(patient_nr)
    IMAGE_PATH+=STR_PATIENT_FOLDER + "/"

    if before:
        IMAGE_PATH+="przed (pierwsza wziyta)/"
    else : 
        IMAGE_PATH+="po (ostatnia wizyta)/"

    if image_type=="2d_snapshots":
        IMAGE_PATH+= "2d/"
    elif image_type=="2d_source":
        IMAGE_PATH+= "2d zdrodlowe/"
    elif image_type=="3d":
        IMAGE_PATH+= "3d/"

    list_of_photos = os.listdir(IMAGE_PATH)
    list_of_photos.sort()

    # Hardcoded fix for lost data:

    # print("\n\nphoto_nr:", photo_nr)
    # print("patient_nr:", patient_nr)
    # print("IMAGE_PATH:", IMAGE_PATH)
    # print("\n\n")


    IMAGE_PATH+=list_of_photos[photo_nr-1]

    # A lil hack till we sort out 3d data reading
    if image_type=="3d":
        return IMAGE_PATH
    
    image = cv2.imread(IMAGE_PATH)

    if only_face : 
        try:
            # return(detect_face_deprecated)
            return detect_face(image, IMAGE_PATH, additional_pixels)
        except:
            print("Failed to correctely detect the face. Returning null! Handle this in data processing!")
            print(f"IMAGE_PATH:{IMAGE_PATH}\n")
            return None
    else :
        return image


def find_patient_folder_given_patient_nr(patient_nr):
    """
    1 -> '1. Gasek'
    2 -> '2. Kolodziejska'
    etc. 
    """


    # patient_list = os.listdir("../Pacjenci/")
    patient_list = os.listdir(IMAGE_PATH)
    save_remove_from_list(patient_list, ".DS_Store")
    save_remove_from_list(patient_list, "Instrukcja.txt")
    save_remove_from_list(patient_list, "17. Gorszczak - po przerwie")
    save_remove_from_list(patient_list, "(pws za male - i tak wypelnilem tho)70. Wójcicki")
    save_remove_from_list(patient_list, "(zly pacjent - dorasta & powierzchnia sie zmienia)4. Krzyszton")
    available_patient_nrs = list([find_nr_in_string(x) for x in patient_list])
    try : 
        list_index = available_patient_nrs.index(str(patient_nr))
    except : 
        raise Exception(f"No patient found for patient numbered : {patient_nr}")
    return patient_list[list_index]


def detect_face_deprecated(image, photo_path = None):
    """
    Old deprecated face detector
    """
    faceCascade = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # plt.imshow(image)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=4,
        # minSize=(30, 30), # Might need to toy around with this one
        flags = cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces) !=1:
        raise Exception(f"Error while cropping faces. In the image w. photo path: {photo_path}, there were {len(faces)} faces found, instead of 1")
    x, y, w, h = faces[0]
    # plt.imshow(image[y:y+h, x:x+w])
    return image[y:y+h, x:x+w]



def detect_face(image, photo_path = None, additional_pixels = 100):
    '''
    additional_pixels: int -> how many pixels to include around initial face position
        Default 100 comes from experimenting on the size
    '''

    # temp = image.copy()
    Y_SIZE, X_SIZE, _ = np.array(image).shape
    faces = face_recognition.face_locations(image)
    if len(faces) !=1:
        raise Exception(f"Error while cropping faces. In the image w. photo path: {photo_path}, there were {len(faces)} faces found, instead of 1")
    y1, x2, x1, y2 = faces[0]
    if not additional_pixels :
        image = image[y1:y2, x1:x2]
    else :
        i = additional_pixels
        y1 = max(y1-i,0)
        y2 = min(y2+i,Y_SIZE-1)
        x1 = max(x1-i,0)
        x2 = min(x2+i,X_SIZE-1)
        image = image[y1:y2, x1:x2]
    return image