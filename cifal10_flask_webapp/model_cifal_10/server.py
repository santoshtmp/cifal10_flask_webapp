from model_cifal_10.model_load import *
import numpy as np
from skimage import io
from skimage.transform import resize

# initialize these variables
model = init()

def predict(imgData):
    #my_image=io.imread(imgData)
    my_image=imgData
    img_resize=resize(my_image, (32, 32, 3))
    probabilities = model.predict(np.array([img_resize]))
    index = np.argsort(probabilities[0, :])
    number_to_class = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
    img_class = number_to_class[index[9]]
    probability = probabilities[0, index[9]]
    # print('the output is :: ')
    # print(img_class)
    # print(probability)
    # print("sucess output")
    return img_class,probability


#predict()