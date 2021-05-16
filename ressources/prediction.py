#!usr/bin/python3


def prediction(image, model = 1, size = (96,96), user = False):

    """
    img : path to file
    size : 
    weight : weight of model
    height : height of model
    model : 1 = Binary Apple and Banane
    model : 2 = 130 class

    """
    from tensorflow import keras

    image_for_keras = keras.preprocessing.image.load_img(image, target_size=size)
    image_for_keras = keras.preprocessing.image.img_to_array(image_for_keras)
    
    import numpy as np
    image_for_keras = np.expand_dims(image_for_keras, axis = 0)
    
    if model == 1:
        model_choose = 'models/model-prototype'
        class_model = open("models/modele-prototype-2.pkl", "rb")
    elif model == 2 :
        model_choose = 'models/modele-prototype-131-2'
        class_model = open("models/modele-prototype-131.pkl", "rb")
    
    model = keras.models.load_model(model_choose)
    
    prediction = model.predict(image_for_keras)

    
    y_classes = prediction.argmax(axis=-1)

    import pickle

    
    dict_class = pickle.load(class_model)

    class_model.close()

    for keys, values in dict_class.items():
        if values == y_classes:
            result = keys
            
    return result

#print(prediction("static/image/21-05-14_01-04-11.jpg"))