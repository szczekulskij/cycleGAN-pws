import matplotlib.pyplot as plt
import os
import cv2
import numpy as np




PWS_POSITION_DICT = {
    '1': ['right', 'middle'],
    '2': ['left', 'middle'], 
    '4': ['left'],
    '7': ['right', 'middle'],    
    '8': ['left','middle'], 
    '12': ['left', 'middle'],
    '11': ['left', 'middle'], 
    '13': ['right','middle'],
    '14': ['left', 'right', 'middle'], 
    '15': ['left', 'middle'],
    '16': ['right', 'middle'],  #Kid
    '17': ['left', 'middle'],
    '18': ['left', 'middle'], 
    '19': ['right'], 
    '20': ['left', 'middle'],
    '21': ['left', 'middle'], 
    '24': ['middle'],
    '25': ['left', 'middle'],  
    '26': ['left'],  
    '27': ['middle'],
    '28': ['middle', 'right'],  
    '31': ['middle', 'left', 'right'],
    '32': ['middle', 'left'], 
    '33': ['middle'],  
    '34': ['left', 'middle'], 
    '35': ['left', ], 
    '37': ['right', 'middle'], 
    '38': ['right', 'middle'], 
    '39': ['left', 'middle'], 
    '41': ['left', 'middle'], 
    '44': ['left', 'middle'], 
    '45': ['right', 'middle'], 
    '47': ['left', 'middle'], 
    '49': ['left', 'middle'], 
    '50': ['left', 'middle'], 
    '52': ['left', 'middle'], 
    '57': ['left', 'middle'], 
    '63': ['left', ], 
    '67': ['left', 'middle'], 
    '69': ['right', 'middle'], 
}

IMAGE_PATH = f"../../../data/PatientsPhotos/"

PWS_KIDS_LIST = [

]

PWS_WEIRD_PATIENT_LIST = [
    
]


def pretty_print_dict(dictionary):
    import json
    print(json.dumps(dictionary, sort_keys=True, indent=4))

def save_remove_from_list(list, value):
    '''
    A bit of a weird function. Implemented because I want this data `pipeline` to work with both dataset (non-updated & updated)
    '''
    try : list.remove(value)
    except: pass


def print_labels_occurence(labels):
    occurence_dict = {}
    for label in labels:
        if label not in occurence_dict.keys():
            occurence_dict[label] = 1 
        else :
            occurence_dict[label]+=1
    pretty_print_dict(occurence_dict)
    



def get_list_of_available_patient_nrs():
    '''
    does what it sounds like it does :P 
    '''

    # patient_list = os.listdir("Pacjenci/")
    patient_list = os.listdir(IMAGE_PATH)
    save_remove_from_list(patient_list, ".DS_Store")
    save_remove_from_list(patient_list, "Instrukcja.txt")
    save_remove_from_list(patient_list, "17. Gorszczak - po przerwie")
    save_remove_from_list(patient_list, "(pws za male - i tak wypelnilem tho)70. Wójcicki")
    save_remove_from_list(patient_list, "(zly pacjent - dorasta & powierzchnia sie zmienia)4. Krzyszton")
    available_patient_nrs = list(set([find_nr_in_string(x) for x in patient_list]))
    return available_patient_nrs

def find_nr_in_string(string):
        """
        Find a number in string like "1.Gasek"
        raise error if multiple or no number found (it means surnames has been somehow corrupted)
        """
        import re
        list_of_nrs = re.findall(r'\d+', string)
        if len(list_of_nrs) != 1 :
            raise Exception("Multiple nrs found in a string. Data has been corrupted!!!!")
        else :
            return list_of_nrs[0]

def get_surname_withour_nr(surname_string):
    """  '1. Gazek' -> 'Gazek'   """
    patient_nr = find_nr_in_string(surname_string)
    index_nr = len(patient_nr) + 2
    return surname_string[index_nr:]

def graph_multiple_images(images_array):
    assert type(images_array) == list
    length = len(images_array)
    COLUMNS = 5 # hardcode to 5 columns
    ROWS = 1 
    while ROWS * COLUMNS < length:
        ROWS+=1

    # Graph:
    fig = plt.figure(figsize=(20, 15))
    for iter, image in enumerate(images_array):
        try:
            fig.add_subplot(ROWS,COLUMNS, iter+1)
            plt.imshow(image)
            # plt.axis('off')
        except:
            print(f"failed for image iterated as :{iter}")
        


def concat_3_images(img1, img2, img3):
    # Choose minimum shape of the image
    min1, min2 = 10000, 10000
    for dim1, dim2, dim3 in [img1.shape, img2.shape, img3.shape]:
        if dim1 < min1:
            min1 = dim1
        if dim2 < min2:
            min2 = dim2
    
    # Resize images:
    dims = (min1, min2)
    img1 = cv2.resize(img1, dsize=dims, interpolation=cv2.INTER_CUBIC)
    img2 = cv2.resize(img2, dsize=dims, interpolation=cv2.INTER_CUBIC)
    img3 = cv2.resize(img3, dsize=dims, interpolation=cv2.INTER_CUBIC)

    return np.concatenate([img1, img2, img3], axis=1)