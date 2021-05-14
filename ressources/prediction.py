#!usr/bin/python3


def prediction(image, size = (96,96)):

    """
    img : path to file
    size : 
    weight : weight approx desired google only 
    height : height approx desired google only

    """
    from tensorflow import keras

    image_for_keras = keras.preprocessing.image.load_img(image, target_size=size)
    image_for_keras = keras.preprocessing.image.img_to_array(image_for_keras)
    
    
    import numpy as np
    image_for_keras = np.expand_dims(image_for_keras, axis = 0)

    model = keras.models.load_model('models/model-prototype')
    prediction = model.predict(image_for_keras)

    
    y_classes = prediction.argmax(axis=-1)

    if y_classes == 0 :
        result = "Pomme"
    elif y_classes == 1:
        result = "Banane"
    else : 
        result = "erreur"
        

    return result

    """
    from os import listdir
    mapping = []
    for x in listdir("DL/TRAIN") :
        mapping.append(x)

    try  :
        return mapping[int(y_classes)]#
    except :    
        return "erreur"
    """


#print(prediction("static/image/21-05-14_01-04-11.jpg"))