from tensorflow.keras.models import model_from_json



def init():
    with open('./model_cifal_10/cifal_10_model_config.json') as json_file:
        json_config_loaded = json_file.read()
    model_loaded = model_from_json(json_config_loaded)
    # load weights into new model
    model_loaded.load_weights('./model_cifal_10/cifal_10_model_weights.h5')
    # print("Loaded Model from disk")
    # compile and evaluate loaded model
    model_loaded.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
    return model_loaded
